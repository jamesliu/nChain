from nchain.pipeline import DataPipeline
from nchain.loaders import ArxivLoader, PdfLoader, SQLiteLoader
from nchain.chunkers import TextChunker
from nchain.vectordb import SQLiteVectorDB
from nchain.utils.detection import detect_data_type
from nchain.utils.sqlite_logger import logger
from nchain.embedders import SentenceTransformersEmbedder
from nchain import user_dir
from time import time
import sqlite_utils

class App:
    def __init__(self, db_path=":memory:", vectordb_path: str = str(user_dir() / "embeddings.db"), indexdb_path: str = str(user_dir() / "index.ann")):
        self.db_path = db_path
        self.db = sqlite_utils.Database(db_path)
        self.db["query_results"].create({
            "query": str,
            "data_type": str,
            "embedding_id": int,
            "score": float,
            "content": str,
            "metadata": str,
            "created": int
        }, pk=("query", "data_type", "embedding_id"), if_not_exists=True)
        self.vectordb_path = vectordb_path
        self.embedder = SentenceTransformersEmbedder()
        # Loaders
        self.loaders = {
            "ARXIV_PAPER": ArxivLoader(self.db_path),
            "PDF_FILE": PdfLoader(),
            "SQLITE_DATA": SQLiteLoader(self.db_path)
        }

        self.vectordbs = {
            "ARXIV_PAPER": SQLiteVectorDB(dimension=self.embedder.dimension, indexdb_path=indexdb_path, db_path=vectordb_path, collection="axiv_paper")
        }
        self.chunkers = {
            "ARXIV_PAPER": TextChunker(max_chars=1000)
        }

    def add(self, source: str, data_type: str = None):
        """Adds a new source to the database."""
        if data_type is None:
            data_type = detect_data_type(source)

        loader = self.loaders.get(data_type)
        if not loader:
            raise ValueError(f"Unsupported data type: {data_type}", f"Supported data types: {self.loaders.keys()}")
        chunker = self.chunkers.get(data_type)
        if not chunker:
            raise ValueError(f"Unsupported data type: {data_type}", f"Supported data types: {self.chunkers.keys()}")
        vectordb = self.vectordbs.get(data_type)
        if not vectordb:
            raise ValueError(f"Unsupported data type: {data_type}", f"Supported data types: {self.vectordbs.keys()}")

        # Create a DataPipeline instance
        pipeline = DataPipeline(loader=loader, embedder=self.embedder, chunker=chunker, vectordb=vectordb)
        # Process the source using the pipeline
        pipeline.process(source)
        logger.info(f"Added source: {source} to the database.")

    def query(self, user_query: str, top_k: int = 5):
        """Query the database for similar embeddings."""
        query_embedding = self.embedder.embed(user_query)  # Use the correct method

        results = []
        for data_type, vectordb in self.vectordbs.items():
            #Search for similar embeddings in the SQLiteVectorDB
            similar_entries = vectordb.search_vectors(query_embedding, top_k)

            # Store Query Result
            for entry in similar_entries:
                self.db['query_results'].upsert(
                     {"query": user_query, "data_type": data_type, "embedding_id": entry.id, "score": entry.score, 
                      "content":entry.content, "metadata": entry.metadata,
                      "created": int(time())}, pk=("query", "data_type", "embedding_id"))

            results.extend(similar_entries)
        
        return results

from nanochain.pipeline import DataPipeline
from nanochain.loaders import ArxivLoader, PdfLoader, SQLiteLoader
from nanochain.vectordb import SQLiteVectorDB
from nanochain.utils.detection import detect_data_type
from nanochain.utils.sqlite_logger import logger
from nanochain.embedders import SentenceTransformersEmbedder
from nanochain import user_dir

class App:
    def __init__(self, db_path=":memory:", vectordb_path: str = str(user_dir() / "embeddings.db")):
        self.db_path = db_path
        self.vectordb_path = vectordb_path
        self.embedder = SentenceTransformersEmbedder()
        self.vectordb = SQLiteVectorDB(dimension=self.embedder.dimension, db_path=vectordb_path)
        # Loaders
        self.loaders = {
            "ARXIV_PAPER": ArxivLoader(self.db_path),
            "PDF_FILE": PdfLoader(),
            "SQLITE_DATA": SQLiteLoader(self.db_path)
        }

    def add(self, source: str, data_type: str = None):
        """Adds a new source to the database."""
        if data_type is None:
            data_type = detect_data_type(source)

        loader = self.loaders.get(data_type)
        if not loader:
            raise ValueError(f"Unsupported data type: {data_type}")

        # Create a DataPipeline instance
        pipeline = DataPipeline(loader=loader, embedder=self.embedder, vectordb=self.vectordb)
        # Process the source using the pipeline
        pipeline.process(source)
        logger.info(f"Added source: {source} to the database.")

    def query(self, user_query: str, top_k: int = 5):
        # 1. Convert user query into an embedding
        query_embedding = self.embedder.embed_text(user_query)

        # 2. Search for similar embeddings in the SQLiteVectorDB
        similar_ids = self.vector_db.search(query_embedding, top_k)

        # 3. Fetch and return results
        results = []
        for idx in similar_ids:
            data = self.vector_db.get_vector_data(idx)
            results.append(data)
        
        return results

from nanochain.loaders import BaseLoader
from nanochain.chunkers import BaseChunker, TextChunker
from nanochain.embedders import BaseEmbedder
from nanochain.embedders import SentenceTransformersEmbedder
from nanochain.vectordb.sqlite_vectordb import SQLiteVectorDB
from nanochain.utils.sqlite_logger import logger

class DataPipeline:
    def __init__(self, 
                 loader: BaseLoader,
                 embedder: BaseEmbedder,
                 vectordb_path: str,
                 chunker: BaseChunker = TextChunker(),
                 ):
        self.loader = loader
        self.chunker = chunker
        self.embedder = embedder
        self.vectordb = SQLiteVectorDB(dimension=embedder.dimension, db_path=vectordb_path)
        
    def process(self, source: str, metadata: dict = None):
        """
        Processes the data source, chunks it, embeds it, and stores the embeddings.
        
        :param source: The data source, e.g., a URL or a file path.
        :param metadata: Additional metadata to store alongside the embeddings.
        """
        # Load data
        data = self.loader.load_data(source)
        
        # Chunk data
        chunks = self.chunker.chunk(data)
        
        # Embed chunks
        embeddings = [self.embedder.embed(chunk) for chunk in chunks]
        
        # Store embeddings and metadata
        for embedding in embeddings:
            self.vectordb.insert(embedding, metadata=metadata)
            
        logger.info(f"Processed and stored embeddings for source: {source}")

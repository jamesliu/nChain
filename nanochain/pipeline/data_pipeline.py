from typing import List, Union
from nanochain.loaders import BaseLoader
from nanochain.chunkers import BaseChunker, TextChunker
from nanochain.embedders import BaseEmbedder
from nanochain.vectordb import VectorDatabase
from nanochain.utils.sqlite_logger import logger

class DataPipeline:
    def __init__(self, 
                 loader: BaseLoader,
                 embedder: BaseEmbedder,
                 vectordb: VectorDatabase,
                 chunker: BaseChunker = TextChunker()):
        self.loader = loader
        self.chunker = chunker
        self.embedder = embedder
        self.vectordb = vectordb
        
    def process(self, source: str, metadata: dict = None, store_text: bool = True, detail: bool = False) -> Union[None, List[dict]]:
        """
        Processes the data source, chunks it, embeds it, and stores the embeddings.
        
        :param source: The data source, e.g., a URL or a file path.
        :param metadata: Additional metadata to store alongside the embeddings.
        :param store: Flag to indicate if the original text chunk should be stored. Default is True.
        """
        # Load data
        data = self.loader.load_data(source)
        
        # Chunk data
        chunks = self.chunker.chunk(data)
        chunk_indices = list(range(len(chunks)))
        
        # Embed chunks
        embeddings = self.embedder.embed(chunks)

        # Store embeddings and metadata
        if metadata is None:
            metadata = {}
        
        if store_text:
            metadatas = [{"chunk": chunk, "chunk_idx": idx, **metadata} for idx, chunk in zip(chunk_indices, chunks)]
        else:
            metadatas = [{"chunk_idx": idx, **metadata} for idx in chunk_indices]
                
        self.vectordb.store_vectors(embeddings, metadata_list=metadatas)
        
        #logger.info(f"Processed and stored embeddings for source: {source}")

        if detail:
            processed_data = [
                {"embedding": embedding, "metadata": meta}
                for embedding, meta in zip(embeddings, metadatas)
            ]
            return processed_data
        return None


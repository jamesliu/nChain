from typing import List, Union
from nchain.loaders import BaseLoader
from nchain.chunkers import BaseChunker, TextChunker
from nchain.embedders import BaseEmbedder
from nchain.vectordb import VectorDatabase
from nchain.utils.sqlite_logger import logger

class DataPipeline:
    def __init__(self, 
                 loader: BaseLoader,
                 embedder: BaseEmbedder,
                 vectordb: VectorDatabase,
                 chunker: BaseChunker):
        self.loader = loader
        self.chunker = chunker
        self.embedder = embedder
        self.vectordb = vectordb

    def process_data(self, data: dict, store: bool = True, detail: bool = False) -> Union[None, List[dict]]:
        content = data["content"]
        metadata = data["meta_data"]
        # Chunk data
        chunks = self.chunker.chunk(content)
        chunk_indices = list(range(len(chunks)))
        
        # Embed chunks
        embeddings = self.embedder.embed(chunks)

        # Store embeddings and metadata
        if metadata is None:
            metadata = {}
        
        metadatas = [{"chunk_idx": idx, **metadata} for idx in chunk_indices]
                
        self.vectordb.store_vectors(embeddings, metadata_list=metadatas, chunks=chunks, store=store)
        
        #logger.info(f"Processed and stored embeddings for source: {source}")

        if detail:
            processed_data = [
                {"embedding": embedding, "meta_data": meta}
                for embedding, meta in zip(embeddings, metadatas)
            ]
            return processed_data
        return []
       
    def process(self, source: str, store: bool = True, detail: bool = False) -> List[dict]:
        """
        Processes the data source, chunks it, embeds it, and stores the embeddings.
        
        :param source: The data source, e.g., a URL or a file path.
        :param store: Flag to indicate if the original text chunk should be stored. Default is True.
        """
        embeddings = []
        # Load data
        res = self.loader.load_data(source)
        doc_id = res['doc_id'] 
        data = res['data']
        if isinstance(data, List):
            for d in data:
                embeddings.extend(self.process_data(d, store=store, detail=detail))
        else:
            embeddings.extend(self.process_data(data, store=store, detail=detail))
        return embeddings

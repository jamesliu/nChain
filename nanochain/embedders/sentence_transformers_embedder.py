from typing import Iterable, List
from .base_embedder import BaseEmbedder
from sentence_transformers import SentenceTransformer

embedder_models = {
    "all-MiniLM-L6-v2": 384,  # Assuming this model produces embeddings of size 384
    "all-mpnet-base-v2": 768,  # Assuming this model produces embeddings of size 768
    "paraphrase-MiniLM-L6-v2": 384  # Assuming this model produces embeddings of size 384
}

class SentenceTransformersEmbedder(BaseEmbedder):
    """
    Embedder using Sentence Transformers to convert text data into embeddings.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def embed(self, chunks: Iterable[List[str]]) -> Iterable[List[float]]:
        """
        Convert chunks of text data into embeddings using Sentence Transformers.
        
        :param chunks: Chunks of text data.
        :return: An iterable of embeddings.
        """
        for chunk in chunks:
            embeddings = self.model.encode(chunk)
            yield embeddings

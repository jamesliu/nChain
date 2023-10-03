from typing import Iterable, List, Union
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

    def embed(self, data: Union[List[List[str]], Iterable[List[str]]]) -> Iterable[List[List[float]]]:
        """
        Generate embeddings for the input data using the SentenceTransformer model.

        :param data: List of chunks where each chunk is a list of sentences.
        :return: Iterable of lists where each list represents embeddings for a chunk.
        """
        for chunk in data:
            yield self.model.encode(chunk, convert_to_numpy=True, show_progress_bar=False).tolist()

from typing import List, Union
from .base_embedder import BaseEmbedder
from sentence_transformers import SentenceTransformer
from nchain.utils.sqlite_logger import logger

embedder_models = {
    "all-MiniLM-L6-v2": 384,  # Assuming this model produces embeddings of size 384
    "all-mpnet-base-v2": 768,  # Assuming this model produces embeddings of size 768
    "paraphrase-MiniLM-L6-v2": 384  # Assuming this model produces embeddings of size 384
}

class SentenceTransformersEmbedder(BaseEmbedder):
    """
    Embedder using Sentence Transformers to convert text data into embeddings.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        #logger.info(f"Initializing Sentence Transformers with model: {model_name}.")
        try:
            self.model = SentenceTransformer(model_name, device=device)
            #logger.info(f"Model {model_name} loaded successfully on device {device}.")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}. Error: {e}")

    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for the given text(s).

        :param text: A single string or a list of strings.
        :return: Embedding(s) for the given text(s).
        """
        try:
            embeddings = self.model.encode(text, convert_to_numpy=True, show_progress_bar=False)
            logger.debug(f"Generated embeddings for input text.")
        except Exception as e:
            logger.error(f"Error during embedding generation. Error: {e}")
            return []

        if isinstance(text, str):
            return embeddings.tolist()
        return [embedding.tolist() for embedding in embeddings]

    @property
    def dimension(self) -> int:
        dimension = self.model.get_sentence_embedding_dimension()
        logger.debug(f"Embedding dimension for model is {dimension}.")
        return dimension


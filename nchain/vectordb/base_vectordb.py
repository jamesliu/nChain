from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Union
import hashlib

class VectorDatabase(ABC):

    @abstractmethod
    def store_vectors(self, vectors: List[List[float]], metadata_list: List[dict], chunks: List[Union[str, bytes]], store:bool) -> None:
        """
        Store vectors along with associated metadata.

        :param vectors: List of embeddings (dense vectors) to store.
        :param metadata: List of metadata associated with each vector.
        """
        pass

    @abstractmethod
    def search_vectors(self, query_vector: List[float], top_k: int = 5) -> List[Tuple[int, float, dict]]:
        """
        Perform a similarity search and retrieve the top_k most similar vectors to the query_vector.

        :param query_vector: The vector for which similar vectors need to be found.
        :param top_k: Number of top similar vectors to return.
        :return: List of tuples with (index, similarity_score, metadata).
        """
        pass

    @abstractmethod
    def update_vector(self, index: int, new_vector: List[float], new_metadata: Optional[dict] = None) -> None:
        """
        Update a vector in the database.

        :param index: The index of the vector to be updated.
        :param new_vector: The new vector.
        :param new_metadata: The new metadata. If None, the metadata remains unchanged.
        """
        pass

    @abstractmethod
    def delete_vector(self, index: int) -> None:
        """
        Remove a vector from the database.

        :param index: The index of the vector to be removed.
        """
        pass

    @staticmethod
    def content_hash(input: Union[str, bytes]) -> bytes:
        "Hash content for deduplication. Override to change hashing behavior."
        if isinstance(input, str):
            input = input.encode("utf8")
        return hashlib.sha256(input).digest()

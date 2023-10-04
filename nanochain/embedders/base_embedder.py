from abc import ABC, abstractmethod
from typing import Any, Iterable, List

class BaseEmbedder(ABC):
    """
    Abstract base class for all embedders. Defines the basic interface that every embedder should have.
    """

    @abstractmethod
    def embed(self, chunks: Iterable[Any]) -> Iterable[List[float]]:
        """
        Convert data chunks into embeddings.

        :param chunks: Data chunks to be converted.
        :return: An iterable of embeddings.
        """
        pass

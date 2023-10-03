from abc import ABC, abstractmethod
from typing import Any, Iterable

class BaseChunker(ABC):
    """
    Abstract base class for all chunkers. Defines the basic interface that every chunker should have.
    """
    def __init__(self, max_chunk_size: int = 512):
        self.max_chunk_size = max_chunk_size

    @abstractmethod
    def chunk_data(self, data: Any) -> Iterable[Any]:
        """
        Given some data, divide it into chunks.
        
        :param data: Data to be chunked.
        :return: An iterable of data chunks.
        """
        pass

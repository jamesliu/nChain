from abc import ABC, abstractmethod
from typing import List

class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Return the dimensionality of the embeddings produced by the embedder.
        """
        pass

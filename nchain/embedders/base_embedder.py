from abc import ABC, abstractmethod
from typing import List, Union

class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Return the dimensionality of the embeddings produced by the embedder.
        """
        pass

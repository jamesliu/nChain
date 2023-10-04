from abc import ABC, abstractmethod
from typing import List
import textwrap

class BaseChunker(ABC):
    """ Abstract base class for all chunkers """

    @abstractmethod
    def chunk(self, data: str) -> List[str]:
        pass


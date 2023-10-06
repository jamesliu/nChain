from abc import ABC, abstractmethod
from typing import Any

class BaseLoader(ABC):

    @abstractmethod
    def load_data(self, source: str) -> Any:
        """
        Abstract method to load data from the provided source.
        
        :param source: The source (could be a URI, path, etc.) from which data should be loaded.
        :return: Data loaded from the source.
        """
        pass

from .base_loader import BaseLoader

class TextLoader(BaseLoader):

    def load_data(self, source: str) -> str:
        """
        Load plain text data.

        :param source: Plain text data.
        :return: Provided text data (unchanged).
        """
        return source

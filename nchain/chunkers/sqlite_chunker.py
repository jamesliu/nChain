from typing import Iterable, List, Dict
from .base_chunker import BaseChunker

class SQLiteChunker(BaseChunker):
    """
    Chunker for SQLite data. Divides data into chunks based on rows.
    """

    def __init__(self, chunk_size: int = 100):
        self.chunk_size = chunk_size

    def chunk(self, data: List[Dict]) -> Iterable[List[Dict]]:
        """
        Given a list of dictionary rows from SQLite, divide it into chunks.
        
        :param data: List of dictionary rows from SQLite.
        :return: An iterable of data chunks.
        """
        for i in range(0, len(data), self.chunk_size):
            yield data[i:i + self.chunk_size]

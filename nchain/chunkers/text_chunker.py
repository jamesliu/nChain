from .base_chunker import BaseChunker
from typing import List
import textwrap

class TextChunker(BaseChunker):
    """ Primary chunker for handling most textual data """

    def __init__(self, max_chars: int = 500):
        self.max_chars = max_chars

    def chunk(self, data: str) -> List[str]:
        # Use textwrap to break the text into chunks without breaking words
        chunks = textwrap.wrap(data, width=self.max_chars, break_long_words=False)
        #logger.info(f"Chunked data into {len(chunks)} chunks using TextChunker.")
        return chunks

from typing import List, Iterable
from .base_chunker import BaseChunker
import nltk
nltk.download('punkt')


class SentenceChunker(BaseChunker):
    """
    The SentenceChunker splits texts into individual sentences using NLTK's sent_tokenize function.
    This is useful when the goal is to embed individual sentences rather than entire paragraphs or documents.
    """

    def __init__(self, max_chunk_size: int = 512):
        """
        Initialize the SentenceChunker.

        :param max_chunk_size: The maximum number of tokens in a chunk. This is especially useful when certain
                               embedding models have a token limit.
        """
        super().__init__(max_chunk_size)

    def chunk_data(self, data: List[str]) -> Iterable[List[str]]:
        """
        Chunk the input data into sentences.

        :param data: List of texts to be chunked.
        :return: Iterable containing chunks of sentences.
        """
        for text in data:
            yield nltk.sent_tokenize(text)

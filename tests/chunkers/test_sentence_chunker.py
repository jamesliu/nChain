import pytest
from nanochain.chunkers.sentence_chunker import SentenceChunker

@pytest.fixture
def sentence_chunker():
    return SentenceChunker()

def test_single_sentence(sentence_chunker):
    """Test chunking a single sentence."""
    text = "This is a single sentence."
    chunks = list(sentence_chunker.chunk_data([text]))
    assert len(chunks) == 1
    assert chunks[0] == [text]

def test_multiple_sentences(sentence_chunker):
    """Test chunking multiple sentences."""
    text = "This is the first sentence. Here's the second. And now the third."
    chunks = list(sentence_chunker.chunk_data([text]))
    assert len(chunks) == 1
    assert chunks[0] == [
        "This is the first sentence.",
        "Here's the second.",
        "And now the third."
    ]

def test_multiple_texts(sentence_chunker):
    """Test chunking multiple texts."""
    texts = [
        "First text with a single sentence.",
        "Second text. It has two sentences!"
    ]
    chunks = list(sentence_chunker.chunk_data(texts))
    assert len(chunks) == 2
    assert chunks[0] == ["First text with a single sentence."]
    assert chunks[1] == ["Second text.", "It has two sentences!"]

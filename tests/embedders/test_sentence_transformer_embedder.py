import pytest
from nanochain.embedders.sentence_transformer_embedder import SentenceTransformerEmbedder

@pytest.fixture
def embedder():
    """Fixture to initialize the SentenceTransformerEmbedder."""
    return SentenceTransformerEmbedder()

def test_initialization(embedder):
    """Test that the embedder initializes without errors."""
    assert embedder is not None
    assert embedder.model is not None

def test_embedding_generation(embedder):
    """Test that the embedder produces non-empty embeddings for given inputs."""
    text = "This is a sample sentence."
    embedding = embedder.embed(text)
    assert embedding is not None
    assert len(embedding) > 0

def test_embedding_dimension(embedder):
    """Test that the embeddings' dimensions match the expected size."""
    text = "Another sample sentence."
    embedding = embedder.embed(text)
    # Assuming the default model 'paraphrase-MiniLM-L6-v2' produces embeddings of size 384
    assert len(embedding) == 384

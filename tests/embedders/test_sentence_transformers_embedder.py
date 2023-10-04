import pytest
from nanochain.embedders.sentence_transformers_embedder import SentenceTransformersEmbedder, embedder_models


@pytest.fixture
def embedder():
    """Fixture to initialize the SentenceTransformerEmbedder."""
    return SentenceTransformersEmbedder()


def test_sentence_transformers_embedder(embedder):
    """
    Test the Sentence Transformers embedder's ability to convert text chunks into embeddings.
    """
    data = ["This is a sample sentence.", "Embedding works fine!"]  # 2 sentences as a chunk
    
    embeddings = embedder.embed(data)
    
    assert len(embeddings) == 2  # One chunk of embeddings
    assert len(embeddings[0]) == 384  # Two embeddings for two sentences

@pytest.mark.parametrize("model_name, embedding_size", embedder_models.items())
def test_embedding_dimension(model_name, embedding_size):
    """Test that the embeddings' dimensions match the expected size."""
    data = "This is a sample sentence." # 1 sentence
    embedder = SentenceTransformersEmbedder(model_name)
    embeddings = embedder.embed(data)
    assert len(embeddings) == embedding_size
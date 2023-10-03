from nanochain.models.core import Chunk, Embedding

def test_chunk_model():
    data = {"id": 1, "content": "Sample content"}
    chunk = Chunk(**data)
    assert chunk.id == 1
    assert chunk.content == "Sample content"

def test_embedding_model():
    data = {"id": 1, "vector": [0.1, 0.2, 0.3]}
    embedding = Embedding(**data)
    assert embedding.id == 1
    assert embedding.vector == [0.1, 0.2, 0.3]

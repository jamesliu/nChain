import pytest
from nanochain.vectordb.faiss_vectordb import FaissVectorDB

def test_vector_storage_and_search():
    db = FaissVectorDB(dimension=2)
    
    # Storing a single vector
    vector = [1.0, 2.0]
    metadata = {"info": "sample_vector"}
    db.store_vectors([vector], [metadata])
    
    # Searching the vector itself should return the same vector as the most similar one
    results = db.search_vectors(vector, top_k=1)
    assert len(results) == 1
    index, distance, metadata = results[0]
    assert metadata["info"] == "sample_vector"
    assert distance == 0.0 # distance to itself should be 0
"""
TODO: Fix this test
def test_vector_update():
    db = FaissVectorDB(dimension=2)
    
    # Storing a single vector
    vector = [1.0, 2.0]
    metadata = {"info": "sample_vector"}
    db.store_vectors([vector], [metadata])

    # Update the vector
    updated_vector = [2.0, 3.0]
    updated_metadata = {"info": "updated_vector"}
    db.update_vector(0, updated_vector, updated_metadata)

    # Searching the updated vector should now return the updated vector
    results = db.search_vectors(updated_vector, top_k=1)
    assert len(results) == 1
    assert results[0][2]["info"] == "updated_vector"

TODO: Fix this test
def test_vector_deletion():
    db = FaissVectorDB(dimension=2)

    # Storing two vectors
    vectors = [[1.0, 2.0], [2.0, 3.0]]
    metadata_list = [{"info": "first_vector"}, {"info": "second_vector"}]
    db.store_vectors(vectors, metadata_list)
    
    first_id, distance, meta = db.search_vectors(vectors[1], top_k=1)[0]
    # Delete the first vector
    db.delete_vector(first_id)

    # Searching the deleted vector should now return the second vector
    results = db.search_vectors(vectors[0], top_k=1)
    assert len(results) == 1
    second_id, distance, metadata = results[0]
    assert metadata["info"] == "second_vector"
"""
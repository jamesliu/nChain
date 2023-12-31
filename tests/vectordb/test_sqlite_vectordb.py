import pytest
from nchain.vectordb.sqlite_vectordb import SQLiteVectorDB
import os

DB_PATH = "tests/resources/vector.db"
INDEXDB_PATH = "tests/resources/index.ann"

#@pytest.fixture(scope="module")
@pytest.fixture(scope="function")
def db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    database = SQLiteVectorDB(dimension=2, indexdb_path=INDEXDB_PATH, db_path=DB_PATH)
    #yield database
    #os.remove(DB_PATH)
    return database

def test_vector_storage_and_search(db:SQLiteVectorDB):
    # Storing a single vector
    vector = [1.0, 2.0]
    metadata = {"info": "sample_vector"}
    db.store_vectors([vector], [metadata], [b"sample_content"], True)

    other_vector = [3.0, 3.0]
    other_metadata = {"info": "sample_vector 2"}
    db.store_vectors([other_vector], [other_metadata], [b"sample_content_other"], True)
    # Searching the vector itself should return the same vector as the most similar one
    results = db.search_vectors(vector, top_k=1)
    assert len(results) == 1
    entry = results[0]
    assert entry.metadata["info"] == "sample_vector"
"""
def test_vector_update(db:SQLiteVectorDB):
    # Storing a single vector
    vector = [1.0, 2.0]
    metadata = {"info": "sample_vector"}
    db.store_vectors([vector], [metadata], [b"sample_content"], True)

    idx, _, _ = db.search_vectors(vector, top_k=1)[0]

    # Update the vector
    updated_vector = [2.0, 3.0]
    updated_metadata = {"info": "updated_vector"}
    db.update_vector(idx, updated_vector, updated_metadata)

    # Searching the updated vector should now return the updated vector
    results = db.search_vectors(updated_vector, top_k=1)
    assert len(results) == 1
    _, _, meta = results[0]
    assert meta["info"] == "updated_vector"

def test_vector_deletion():
    db = SQLiteVectorDB(dimension=2, db_path=DB_PATH)
    # Storing two vectors
    vectors = [[1.0, 2.0], [2.0, 3.0]]
    metadata_list = [{"info": "first_vector"}, {"info": "second_vector"}]
    db.store_vectors(vectors, metadata_list, [b"sample_content"] * len(vectors), True)

    idx0, disntace0, meta0 = db.search_vectors(vectors[0], top_k=1)[0]
    # Delete the first vector
    db.delete_vector(idx0)

    # Searching the deleted vector should now return the second vector
    results = db.search_vectors(vectors[0], top_k=1)
    assert len(results) == 1
    _, _, meta = results[0]
    assert meta["info"] == "second_vector"
"""

#def teardown_module():
def teardown_function():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

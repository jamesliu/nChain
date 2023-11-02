import pytest

def ensure_db_exists(db_path):
    """
    Ensure the SQLite database exists at the specified path.
    If it does not exist, create an empty database at that location.

    :param db_path: Path to the SQLite database.
    """
    import os
    import sqlite3
    # Check if the directory exists, if not create it
    directory = os.path.dirname(db_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Check if the database file exists, if not create it
    if not os.path.exists(db_path):
        # This will create an empty database file
        conn = sqlite3.connect(db_path)
        conn.close()

@pytest.fixture(scope="module")
def test_db_path():
    """
    Fixture to provide the path to the sample SQLite database for testing.

    :return: Path to the sample SQLite database.
    """
    db_path = "tests/resources/test.db"
    ensure_db_exists(db_path)
    return db_path

@pytest.fixture(scope="module")
def test_embedding_path():
    """
    Fixture to provide the path to the sample SQLite database for testing.

    :return: Path to the sample SQLite database.
    """
    db_path = "tests/resources/embedding.db"
    ensure_db_exists(db_path)
    return db_path

@pytest.fixture(scope="module")
def test_indexdb_annoy_path():
    """
    Fixture to provide the path to the sample Annoy database for testing.

    :return: Path to the sample Annoy database.
    """
    return "tests/resources/test_index.ann"

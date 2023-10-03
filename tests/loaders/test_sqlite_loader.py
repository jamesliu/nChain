import pytest
from nanochain.loaders.sqlite_loader import SQLiteLoader

@pytest.fixture
def sample_db_path():
    """
    Fixture to provide the path to the sample SQLite database for testing.

    :return: Path to the sample SQLite database.
    """
    # Assuming you have the test.db setup in the mentioned path
    return "tests/resources/test.db"

def test_table_names_retrieval(sample_db_path):
    """
    Test to verify that the SQLiteLoader correctly retrieves table names from the database.

    :param sample_db_path: Path to the sample SQLite database provided by the fixture.
    """
    loader = SQLiteLoader(sample_db_path)
    tables = loader.get_table_names()
    
    # Assert that the expected table name "SampleTableName" is present in the retrieved list of tables.
    assert "SampleTableName" in tables

def test_fetch_all_data(sample_db_path):
    """
    Test to verify that the SQLiteLoader fetches data rows from a specified table in the database and structures them
    using dynamically generated Pydantic models.

    :param sample_db_path: Path to the sample SQLite database provided by the fixture.
    """
    loader = SQLiteLoader(sample_db_path)
    data = loader.fetch_all_data("SampleTableName")
    
    # Validate the data based on what you know is in the test.db
    # Here, we're checking the attributes of the dynamically generated Pydantic model instances.
    assert data[0].id == 1
    assert data[0].name == "Sample"

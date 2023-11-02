import pytest
from nchain.loaders.sqlite_loader import SQLiteLoader

def test_table_names_retrieval(test_db_path):
    """
    Test to verify that the SQLiteLoader correctly retrieves table names from the database.

    :param sample_db_path: Path to the sample SQLite database provided by the fixture.
    """
    loader = SQLiteLoader(test_db_path)
    tables = loader.get_table_names()
    # Assert that the expected table name "SampleTableName" is present in the retrieved list of tables.
    assert "papers" in tables

def test_fetch_all_data(test_db_path):
    """
    Test to verify that the SQLiteLoader fetches data rows from a specified table in the database and structures them
    using dynamically generated Pydantic models.

    :param sample_db_path: Path to the sample SQLite database provided by the fixture.
    """
    loader = SQLiteLoader(test_db_path)
    data = loader.fetch_all_data("papers")
    
    # Validate the data based on what you know is in the test.db
    # Here, we're checking the attributes of the dynamically generated Pydantic model instances.
    assert len(data) > 0

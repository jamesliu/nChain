import pytest

@pytest.fixture(scope="module")
def test_db_path():
    """
    Fixture to provide the path to the sample SQLite database for testing.

    :return: Path to the sample SQLite database.
    """
    return "tests/resources/test.db"

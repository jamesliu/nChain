import pytest
from nchain.app import App

def test_app_add_and_query(test_db_path, test_indexdb_annoy_path):
    app = App(db_path=test_db_path, indexdb_path=test_indexdb_annoy_path)

    # Test add method
    sample_url = "https://arxiv.org/abs/2010.14701"
    app.add(sample_url)

    # Test query method
    query_str = "sample query"
    result = app.query(query_str)
    assert result, "Query result should not be empty"

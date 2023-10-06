import pytest
from nchain.models.dynamic_model_generator import DynamicModelGenerator
from pydantic import BaseModel

@pytest.fixture
def sample_db_path():
    """
    Fixture to provide the path to the sample SQLite database for testing.

    :return: Path to the sample SQLite database.
    """
    # Assuming you have the test.db setup in the mentioned path
    return "tests/resources/test.db"

def test_dynamic_model_generation(sample_db_path):
    """
    Test to verify that the DynamicModelGenerator correctly creates a Pydantic model 
    based on the schema of a table in the SQLite database.

    :param sample_db_path: Path to the sample SQLite database provided by the fixture.
    """
    generator = DynamicModelGenerator(sample_db_path)
    SampleModel = generator.generate_model("SampleTableName")
    
    # Validate that the generated model is indeed a subclass of Pydantic's BaseModel
    assert issubclass(SampleModel, BaseModel)

    # You can add more specific tests based on known schema of "SampleTableName" if desired

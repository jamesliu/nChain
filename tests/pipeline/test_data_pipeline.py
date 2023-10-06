import pytest
from nchain.pipeline.data_pipeline import DataPipeline
from nchain.loaders.arxiv_loader import ArxivLoader
from nchain.chunkers.text_chunker import TextChunker
from nchain.embedders.sentence_transformers_embedder import SentenceTransformersEmbedder
from unittest.mock import patch
from arxiv import Search

"""
def mock_arxiv_search(*args, **kwargs):
    class MockAuthor:
        def __init__(self, name):
            self.name = name

    class MockResult:
        title = "Mock Title"  # Add mock title attribute
        authors = [MockAuthor("Author1"), MockAuthor("Author2")]  # Mock authors list with name attribute

        # Define the attributes and methods you need from the real Arxiv result here
        def download_pdf(self, directory):
            # Mock the download_pdf method. If you need to simulate a PDF download,
            # you can add logic here. For now, just pass to do nothing.
            pass
    
    # Yield the result to make this function a generator
    yield MockResult()
"""

@pytest.fixture
def setup_data_pipeline(test_db_path):
    loader = ArxivLoader(db_path=test_db_path)
    chunker = TextChunker()
    embedder = SentenceTransformersEmbedder()
    pipeline = DataPipeline(loader=loader, embedder=embedder, chunker=chunker, vectordb_path = test_db_path)
    return pipeline

# Use this patch in your test
#@patch.object(Search, 'results', mock_arxiv_search)
def test_data_pipeline_processing(setup_data_pipeline):
    pipeline = setup_data_pipeline
    source_url = "https://arxiv.org/abs/2309.12307"
    
    # Testing the process method of DataPipeline
    embeddings = pipeline.process(source_url, detail=True)
    
    # Basic checks to ensure the pipeline processed the data correctly
    assert embeddings is not None
    assert isinstance(embeddings, list)
    # You can add more checks here based on your needs

def test_data_pipeline_other_methods(setup_data_pipeline):
    pipeline = setup_data_pipeline
    # Add more tests for other methods of the DataPipeline if applicable

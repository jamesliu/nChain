import pytest
from nanochain.pipeline.data_pipeline import DataPipeline
from nanochain.loaders.arxiv_loader import ArxivLoader
from nanochain.chunkers.text_chunker import TextChunker
from nanochain.embedders.sentence_transformers_embedder import SentenceTransformersEmbedder

@pytest.fixture
def setup_data_pipeline(test_db_path):
    loader = ArxivLoader(db_path=test_db_path)
    chunker = TextChunker()
    embedder = SentenceTransformersEmbedder()
    pipeline = DataPipeline(loader, chunker, embedder)
    return pipeline

def test_data_pipeline_processing(setup_data_pipeline):
    pipeline = setup_data_pipeline
    source_url = "https://arxiv.org/abs/sample_paper_id"
    
    # Testing the process method of DataPipeline
    embeddings = pipeline.process(source_url)
    
    # Basic checks to ensure the pipeline processed the data correctly
    assert embeddings is not None
    assert isinstance(embeddings, list)
    # You can add more checks here based on your needs

def test_data_pipeline_other_methods(setup_data_pipeline):
    pipeline = setup_data_pipeline
    # Add more tests for other methods of the DataPipeline if applicable

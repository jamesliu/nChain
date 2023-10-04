import pytest
import os
from nanochain.loaders.arxiv_loader import ArxivLoader
from nanochain import user_dir
from pathlib import Path

# Constants
SAMPLE_PAPER_ID = "2310.01425"
SAMPLE_DOWNLOAD_DIR = Path(user_dir()) / "Documents" / "paper" 

# Setup and teardown functions for the test database and download directory
@pytest.fixture(scope="module")
def setup_teardown(test_db_path):
    # Setup: Create a test ArxivLoader instance
    loader = ArxivLoader(test_db_path)
    yield loader

    # Teardown: Remove test database and downloaded PDF
    os.remove(test_db_path)
    #pdf_path = Path(SAMPLE_DOWNLOAD_DIR) / f"{SAMPLE_PAPER_ID}.pdf"
    #if pdf_path.exists():
    #    os.remove(pdf_path)

def test_load_data(setup_teardown):
    loader = setup_teardown
    metadata = loader.load_data(SAMPLE_PAPER_ID, download_dir=SAMPLE_DOWNLOAD_DIR)

    # Check if the expected keys are present in the metadata
    expected_keys = ["paper_id", "title", "authors", "summary", "pdf_path"]
    for key in expected_keys:
        assert key in metadata

    # Check if the PDF was downloaded to the expected directory
    pdf_path = Path(metadata["pdf_path"])
    assert pdf_path.exists()
"""
def test_extract_pdf_content(setup_teardown):
    loader = setup_teardown
    pdf_path = Path(SAMPLE_DOWNLOAD_DIR) / f"{SAMPLE_PAPER_ID}.pdf"
    content = loader.extract_pdf_content(str(pdf_path))

    # Basic check to see if content was extracted
    assert isinstance(content, str)
    assert len(content) > 0
"""

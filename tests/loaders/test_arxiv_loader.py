import pytest
import os
from nchain.loaders.arxiv_loader import ArxivLoader
from nchain import user_dir
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

"""
def test_load_data(setup_teardown):
    loader = setup_teardown
    data = loader.load_data(SAMPLE_PAPER_ID, download_dir=SAMPLE_DOWNLOAD_DIR)
    content = data["content"]
    metadata = data["metadata"]

    # Check if the expected keys are present in the metadata
    expected_keys = ["paper_id", "title", "authors", "summary", "pdf_path"]
    for key in expected_keys:
        assert key in metadata

    # Check if the PDF was downloaded to the expected directory
    pdf_path = Path(metadata["pdf_path"])
    assert pdf_path.exists()

    pdf_content = loader.extract_pdf_content(metadata["pdf_path"])

    # Basic check to see if content was extracted
    assert isinstance(pdf_content, str)
    assert len(pdf_content) > 0
"""

import re

def detect_data_type(source: str) -> str:
    """
    Detect the type of data based on the provided source.

    :param source: The source (typically a URL) of the data.
    :return: A string indicating the type of data.
    """

    # Check for arXiv papers
    if re.match(r'^https?://arxiv\.org/abs/\d+\.\d+', source):
        return "ARXIV_PAPER"
    
    # Check for PDF files
    if source.endswith('.pdf'):
        return "PDF_FILE"
    
    # Check for SQLite data (using a custom URI scheme)
    if source.startswith('sqlite:///'):
        return "SQLITE_DATA"
    
    raise ValueError(f"Unsupported source: {source}")

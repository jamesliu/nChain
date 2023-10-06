import pytest
from nchain.chunkers.sqlite_chunker import SQLiteChunker

def test_sqlite_chunker():
    """
    Test the SQLite chunker's ability to divide data into proper chunks.
    """
    data = [{"id": i, "name": f"Sample_{i}"} for i in range(500)]
    chunker = SQLiteChunker(chunk_size=100)
    
    chunks = list(chunker.chunk_data(data))
    
    assert len(chunks) == 5  # 500 rows, 100 rows per chunk
    assert all(len(chunk) == 100 for chunk in chunks)  # Each chunk should have 100 rows

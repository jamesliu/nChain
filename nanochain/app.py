from nanochain.loaders import ArxivLoader, PdfLoader, SQLiteLoader
from nanochain.utils.detection import detect_data_type
from nanochain.embedders import SentenceTransformersEmbedder

class App:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.embedder = SentenceTransformersEmbedder()

        # Loaders
        self.loaders = {
            "ARXIV_PAPER": ArxivLoader(self.db_path),
            "PDF_FILE": PdfLoader(),
            "SQLITE_DATA": SQLiteLoader(self.db_path)
        }

    def add(self, source: str, data_type: str = None):
        if data_type is None:
            data_type = detect_data_type(source)
        loader = self.loaders.get(data_type)
        if not loader:
            raise ValueError(f"Unsupported data type: {data_type}")
        data = loader.load_data(source)
        embedded_data = self.embedder.embed(data)
        # Store embedded_data in the database (this part would need further implementation)

    def query(self, query_str: str):
        embedded_query = self.embedder.embed(query_str)
        # Search the database for relevant data (this part would need further implementation)
        return "Sample result based on query"  # Placeholder

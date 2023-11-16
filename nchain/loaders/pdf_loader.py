from pypdf import PdfReader
from .base_loader import BaseLoader

class PdfLoader(BaseLoader):

    def load_data(self, source: str) -> str:
        """
        Load and extract text from a PDF file.

        :param source: Path to the PDF file.
        :return: Extracted text from the PDF.
        """
        with open(source, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

if __name__ == "__main__":
    loader = PdfLoader()
    print(loader.load_data("paper.pdf"))
import arxiv
import sqlite_utils
import os
from .base_loader import BaseLoader
from .pdf_loader import PdfLoader
from nchain import user_dir
from typing import Optional

class ArxivLoader(BaseLoader):

    def __init__(self, db_path: str):
        """
        Initialize the ArxivLoader with a path to the SQLite database.

        :param db_path: Path to the SQLite database file.
        """
        self.db = sqlite_utils.Database(db_path)
        # Ensure the 'papers' table exists
        self.db["papers"].create({
            "paper_id": str,
            "entry_id": str,
            "title": str,
            "authors": str,
            "summary": str,
            "pdf_path": str,
            "url": str,
            "published": str,
            "updated": str
        }, pk="paper_id", if_not_exists=True)

    def load_data(self, source: str, download_dir: Optional[str] = None) -> dict:
        """
        Load and extract metadata and content from an arXiv paper.
        :source: The arXiv paper ID or URL.
        :param paper_id: The arXiv paper ID.
        :param download_dir: Optional directory path to save the downloaded PDF.
        :return: A dictionary with metadata and content of the paper.
        """
        paper_id = source.split("/")[-1]
        paper = next(arxiv.Search(id_list=[paper_id]).results())
        
        if not download_dir:
            download_dir = str(user_dir() / 'Documents' / 'paper')
        os.makedirs(download_dir, exist_ok=True)
        # Construct the filename based on the paper_id and title
        pdf_filename = f"{paper.entry_id.split('/')[-1]}.{paper.title.replace(' ', '_').replace('/', '_')}.pdf"
        pdf_path = os.path.join(download_dir, pdf_filename)
        if not os.path.exists(pdf_path):
            pdf_path = paper.download_pdf(download_dir)
        else:
            print(f"PDF for {paper_id} already exists at {pdf_path}. Skipping download.")
        metadata = {
            "paper_id": paper_id,
            "entry_id": paper.entry_id,
            "title": paper.title,
            "authors": ", ".join([author.name for author in paper.authors]),
            "summary": paper.summary,
            "pdf_path": str(pdf_path),
            "url": f"https://arxiv.org/abs/{paper_id}",
            "published": paper.published.strftime('%Y-%m-%d %H:%M:%S'),
            "updated": paper.updated.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Save metadata to the database
        self.db["papers"].upsert(metadata, pk="paper_id")

        content = self.extract_pdf_content(pdf_path)
        
        return {"content":content, "metadata":metadata}

    def extract_pdf_content(self, pdf_path: str) -> str:
        """
        Use the PdfLoader to extract the actual content of the provided PDF.

        :param pdf_path: Path to the PDF file.
        :return: Extracted text content of the PDF.
        """
        loader = PdfLoader()
        return loader.load_data(pdf_path)

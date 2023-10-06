import requests
from bs4 import BeautifulSoup
from .base_loader import BaseLoader

class SitemapLoader(BaseLoader):

    def load_data(self, source: str) -> str:
        """
        Load and extract content from a sitemap URL.

        :param source: Sitemap URL.
        :return: Extracted content from the sitemap.
        """
        response = requests.get(source)
        soup = BeautifulSoup(response.content, 'xml')
        return str(soup)

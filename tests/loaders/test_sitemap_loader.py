from nchain.loaders.sitemap_loader import SitemapLoader

# Sample paths and URLs for testing purposes
SAMPLE_SITEMAP_URL = 'https://blog.bayjarvis.com/sitemap.xml'

def test_sitemap_loader():
    loader = SitemapLoader()
    content = loader.load_data(SAMPLE_SITEMAP_URL)
    assert isinstance(content, str)
    assert '<urlset' in content


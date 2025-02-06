import os
import unittest
from tempfile import NamedTemporaryFile

from gscholar.scraping.cache.GoogleScholarCacheSQLite import GoogleScholarCacheSQLite
from gscholar.scraping.crawler.GoogleScholarCrawler import GoogleScholarCrawler, FakeDriver


class GoogleScholarCrawlerTestCase(unittest.TestCase):
    """
     We limit our test to the cache usage
    """

    def setUp(self):
        # Create Fake SQL Cache
        self.tmp_file = NamedTemporaryFile(delete=False)
        if os.path.exists(self.tmp_file.name):
            self.tmp_file.close()
            os.remove(self.tmp_file.name)
        self.sql_cache = GoogleScholarCacheSQLite(self.tmp_file.name)
        self.gsc = GoogleScholarCrawler(cache=self.sql_cache, driver=FakeDriver())

    def tearDown(self) -> None:
        self.gsc.terminate()

    def test_cache_use(self):
        # Fill Fake SQL Cache
        source = self.sql_cache
        source.clear()
        source.add_author_page("aid", "page_content")
        source.add_author_page("aid2", "page_content2")
        source.add_publication_page("aid", "pid", "page_content3")
        source.add_citations_page("9894327834646363633", 0, "page_content4")
        source.add_versions_page("9894327834646363633", 0, "page_content5")

        self.assertEqual("page_content", self.gsc.get_author_page("aid"))
        self.assertEqual("page_content2", self.gsc.get_author_page("aid2"))
        self.assertEqual("page_content3", self.gsc.get_publication_page("aid", "pid"))
        self.assertEqual("page_content4", self.gsc.get_citations_page("9894327834646363633", 0))
        self.assertEqual("page_content5", self.gsc.get_versions_page("9894327834646363633", 0))


if __name__ == "__main__":
    unittest.main()

# End of file

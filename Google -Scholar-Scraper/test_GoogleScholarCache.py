import os
import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory

from gscholar.scraping.cache.GoogleScholarCacheSQLite import GoogleScholarCacheSQLite
from gscholar.scraping.cache.GoogleScholarCacheFile import GoogleScholarCacheFile


class GoogleScholarCacheTestCaseTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        This function needs to be override and GSC has to be defined
        """
        raise unittest.SkipTest

    GSC = None
    cache = None

    def test_author_page(self):
        self.cache.clear()
        self.assertIsNotNone(self.cache)
        self.assertIsNone(self.cache.get_author_page("aid"))
        self.cache.add_author_page("aid", "page_content")
        self.assertEqual("page_content", self.cache.get_author_page("aid"))

    def test_publication_page(self):
        self.cache.clear()
        self.assertIsNotNone(self.cache)
        self.assertIsNone(self.cache.get_publication_page("aid", "pid"))
        self.cache.add_publication_page("aid", "pid", "page_content")
        self.assertEqual("page_content", self.cache.get_publication_page("aid", "pid"))

    def test_citations_page(self):
        self.cache.clear()
        self.assertIsNotNone(self.cache)
        self.assertIsNone(self.cache.get_citations_page("9894327834646363633", 0))
        self.cache.add_citations_page("9894327834646363633", 0, "page_content")
        self.assertEqual("page_content", self.cache.get_citations_page("9894327834646363633", 0))

    def test_versions_page(self):
        self.cache.clear()
        self.assertIsNotNone(self.cache)
        self.assertIsNone(self.cache.get_versions_page("9894327834646363633", 0))
        self.cache.add_versions_page("9894327834646363633", 0, "page_content")
        self.assertEqual("page_content", self.cache.get_versions_page("9894327834646363633", 0))


class GoogleScholarCacheSQLiteTestCase(GoogleScholarCacheTestCaseTemplate):
    @classmethod
    def setUpClass(cls):
        cls.GSC = GoogleScholarCacheSQLite

    def setUp(self):
        self.tmp_file = NamedTemporaryFile(delete=False)
        if os.path.exists(self.tmp_file.name):
            self.tmp_file.close()
            os.remove(self.tmp_file.name)
        self.cache = self.GSC(self.tmp_file.name)

    def tearDown(self):
        self.cache.clear()
        self.cache.close()
        os.remove(self.tmp_file.name)


class GoogleScholarCacheFileTestCase(GoogleScholarCacheTestCaseTemplate):
    @classmethod
    def setUpClass(cls):
        cls.GSC = GoogleScholarCacheFile

    def setUp(self):
        self.tmp_dir = TemporaryDirectory()
        self.cache = self.GSC(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()

# End of file

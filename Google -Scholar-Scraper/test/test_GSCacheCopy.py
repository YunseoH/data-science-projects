import os
import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory
from gscholar.scraping.cache.GoogleScholarCacheSQLite import GoogleScholarCacheSQLite
from gscholar.scraping.cache.GoogleScholarCacheFile import GoogleScholarCacheFile


class GoogleScholarCacheCopyTestCase(unittest.TestCase):

    def setUp(self):

        # Create SQL Cache
        self.tmp_file = NamedTemporaryFile(delete=False)
        if os.path.exists(self.tmp_file.name):
            self.tmp_file.close()
            os.remove(self.tmp_file.name)
        self.sql_cache = GoogleScholarCacheSQLite(self.tmp_file.name)

        # Create File Cache
        self.tmp_dir = TemporaryDirectory()
        self.file_cache = GoogleScholarCacheFile(self.tmp_dir.name)

    def tearDown(self) -> None:
        self.sql_cache.clear()
        self.sql_cache.close()
        self.tmp_dir.cleanup()

    def copy_source_to_target(self, source, target):
        source.clear()
        source.add_author_page("aid", "page_content")
        source.add_author_page("aid2", "page_content2")
        source.add_publication_page("aid", "pid", "page_content3")
        source.add_citations_page("9894327834646363633", 0, "page_content4")
        source.add_versions_page("9894327834646363633", 0, "page_content5")

        target.clear()

        # Check source
        self.assertEqual("page_content", source.get_author_page("aid"))
        self.assertEqual("page_content2", source.get_author_page("aid2"))
        self.assertEqual("page_content3", source.get_publication_page("aid", "pid"))
        self.assertEqual("page_content4", source.get_citations_page("9894327834646363633", 0))
        self.assertEqual("page_content5", source.get_versions_page("9894327834646363633", 0))

        # Copy Cache
        source.copy_into(target)

        # Check source
        self.assertEqual("page_content", source.get_author_page("aid"))
        self.assertEqual("page_content2", source.get_author_page("aid2"))
        self.assertEqual("page_content3", source.get_publication_page("aid", "pid"))
        self.assertEqual("page_content4", source.get_citations_page("9894327834646363633", 0))
        self.assertEqual("page_content5", source.get_versions_page("9894327834646363633", 0))

        # Check target
        self.assertEqual("page_content", target.get_author_page("aid"))
        self.assertEqual("page_content2", target.get_author_page("aid2"))
        self.assertEqual("page_content3", target.get_publication_page("aid", "pid"))
        self.assertEqual("page_content4", target.get_citations_page("9894327834646363633", 0))
        self.assertEqual("page_content5", target.get_versions_page("9894327834646363633", 0))

    def test_copy_sql_to_file(self):
        self.copy_source_to_target(self.sql_cache, self.file_cache)

    def test_copy_file_to_sql(self):
        self.copy_source_to_target(self.file_cache, self.sql_cache)


if __name__ == "__main__":
    unittest.main()

# End of file

import os
import unittest
from tempfile import NamedTemporaryFile

from gscholar.GoogleScholarDB import GoogleScholarDB
from gscholar.db.GoogleScholarDBBuilder import GoogleScholarDBBuilder
from gscholar.scraping.GoogleScholar import GoogleScholar
from gscholar.scraping.cache.GoogleScholarCacheSQLite import GoogleScholarCacheSQLite


CACHE_FILE = os.path.join(os.path.dirname(__file__), 'test_cache.sqlite')


class GoogleScholarDBBuilderTestCase(unittest.TestCase):

    test_author_id = '1TUANHcAAAAJ'

    test_author_list = ["1TUANHcAAAAJ",  # Kuba
                        "x2MfRUYAAAAJ",  # Tom
                        "ky6n3gwAAAAJ"]  # Harry
    test_author_h_index = 6

    def setUp(self):

        # Get a temporary DB filename
        self.tmp_db_file = NamedTemporaryFile(delete=False)
        if os.path.exists(self.tmp_db_file.name):
            self.tmp_db_file.close()
            os.remove(self.tmp_db_file.name)

        # Create a SQLite cache using the existing test cache file
        self.cache_file = CACHE_FILE
        self.assertTrue(os.path.exists(self.cache_file))
        self.cache = GoogleScholarCacheSQLite(self.cache_file)

        self.gs = GoogleScholar(cache=self.cache)
        self.db = GoogleScholarDB(self.tmp_db_file.name)

    def tearDown(self) -> None:

        # Here we must not delete the cache
        self.cache.close()

        # Cleaning the DB temporary File
        self.db.clean()
        self.db.close()
        os.remove(self.tmp_db_file.name)

    def test_fetch_authors_one(self):
        gsb = GoogleScholarDBBuilder(source=self.gs, target=self.db)
        gsb.fetch_authors([self.test_author_id])
        self.db.dump()

    def test_fetch_authors_three(self):
        gsb = GoogleScholarDBBuilder(source=self.gs, target=self.db)
        gsb.fetch_authors(self.test_author_list)
        self.db.dump()

    def test_h_index(self):
        gsb = GoogleScholarDBBuilder(source=self.gs, target=self.db)
        gsb.fetch_authors([self.test_author_id])
        self.assertEqual(self.test_author_h_index, self.db.get_h_index(self.test_author_id))

    def test_citation_graph(self):
        import networkx as nx
        gsb = GoogleScholarDBBuilder(source=self.gs, target=self.db)
        gsb.fetch_authors([self.test_author_id])
        graph = self.db.get_citation_graph(focus_authors=["1TUANHcAAAAJ"])
        self.assertEqual(nx.classes.digraph.Graph, type(graph))
        print(graph.nodes)


if __name__ == "__main__":
    unittest.main()

# End of file

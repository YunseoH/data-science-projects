import os
import unittest
from tempfile import NamedTemporaryFile

from gscholar.GoogleScholarDB import GoogleScholarDB


class GoogleScholarDBTestCase(unittest.TestCase):

    def setUp(self):
        self.tmp_file = NamedTemporaryFile(delete=False)
        if os.path.exists(self.tmp_file.name):
            self.tmp_file.close()
            os.remove(self.tmp_file.name)
        self.db = GoogleScholarDB(self.tmp_file.name)

    def tearDown(self) -> None:
        self.db.clean()
        self.db.close()
        os.remove(self.tmp_file.name)

    def test_add_author(self):
        self.db.add_author("aid1", "name")

    def test_add_publication(self):
        self.db.add_publication("pid1", "title1", 1, ["authors1"])
        self.db.add_publication("pid2", "title2", 2,  ["authors2"])

    def test_add_authorship(self):
        self.db.add_author("aid1", "name")
        self.db.add_publication("pid1", "title1", 1, ["authors1"])
        self.db.add_authorship("aid1", "apid1", "pid1")

    def test_add_citation(self):
        self.db.add_citation("pid1", "pid2")

    def test_get_publication(self):
        self.db.get_publications()
        self.db.add_publication("pid2", "title2", 2, ["authors2"])
        self.db.get_publications()

    def test_h_index(self):

        self.db.add_author("aid1", "name")
        self.db.add_publication("pid1", "title1", 1, ["authors1"])
        self.db.add_authorship("aid1", "apid1", "pid1")
        self.db.add_citation("pid1", "pid2")

        h_index = self.db.get_h_index("aid1")
        self.assertEqual(1, h_index)

        h_index = self.db.get_h_index("aid2")
        self.assertEqual(None, h_index)


if __name__ == "__main__":
    unittest.main()

# End of file

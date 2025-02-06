"""
The GoogleScholarCacheSQLite is a storage based on SQLite.
It stores webpages by type of data and timestamps.

TODO: Add Timestamps

"""
import os
import sqlite3
import pandas as pd

from gscholar.scraping.cache.GoogleScholarCache import GoogleScholarCache
from gscholar.utils.logger import debug_log


def build_gs_cache(cache_file):
    debug_log("Run Build DB\n")
    con = sqlite3.connect(cache_file)

    ap_request = """
        CREATE TABLE author_page (
            author_id varchar(255),
            text varchar,
            PRIMARY KEY (author_id)
        );
    """

    pp_request = """
        CREATE TABLE publication_page (
            author_id varchar(255),
            publication_id varchar(255),
            text varchar,
            PRIMARY KEY (author_id, publication_id)
        );
    """

    cp_request = """
        CREATE TABLE citations_page (
            cluster_id varchar(255),
            start int,
            text varchar,
            PRIMARY KEY (cluster_id, start)
        );
    """

    vp_request = """
        CREATE TABLE versions_page (
            cluster_id varchar(255),
            start int,
            text varchar,
            PRIMARY KEY (cluster_id, start)
        );
    """
    cursor = con.cursor()
    cursor.execute(ap_request)
    cursor.execute(pp_request)
    cursor.execute(cp_request)
    cursor.execute(vp_request)
    cursor.close()
    con.commit()
    con.close()


def check_gs_cache(cache_file):
    debug_log("Run Check DB\n")
    con = sqlite3.connect(cache_file)

    ap_request = """
        SELECT author_id, text FROM author_page LIMIT 1;
    """

    pp_request = """
        SELECT author_id, publication_id, text FROM publication_page LIMIT 1;
    """

    cp_request = """
        SELECT cluster_id, start, text FROM citations_page LIMIT 1;
    """

    vp_request = """
        SELECT cluster_id, start, text FROM versions_page LIMIT 1;
    """
    cursor = con.cursor()
    cursor.execute(ap_request)
    cursor.execute(pp_request)
    cursor.execute(cp_request)
    cursor.execute(vp_request)
    cursor.close()
    con.commit()
    con.close()


class GoogleScholarCacheSQLite (GoogleScholarCache):

    def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file
        if not os.path.exists(db_file):
            build_gs_cache(db_file)
        else:
            check_gs_cache(db_file)
        self.con = sqlite3.connect(db_file)

        cursor = self.con.cursor()
        # Cleaning of the DB -- If needed something wrong happened.
        ###############################
        # cursor.execute('DELETE FROM citations_page WHERE text LIKE \'%gs_captcha_f%\' ')
        # self.con.commit()
        cursor.execute('SELECT cluster_id,start FROM citations_page WHERE text LIKE \'%gs_captcha_f%\' ')
        items = cursor.fetchone()
        cursor.close()
        if items:
            self.con.close()
        assert (not items)

    def add_author_page(self, userid, source):
        cursor = self.con.cursor()
        cursor.execute('REPLACE INTO author_page VALUES (?,?);', (userid, source))
        cursor.close()
        self.con.commit()

    def get_author_page(self, userid):
        cursor = self.con.cursor()
        cursor.execute('SELECT text FROM author_page WHERE author_id == \'{}\' ;'.format(userid))
        items = cursor.fetchone()
        cursor.close()
        if items:
            return items[0]
        else:
            return None

    def add_publication_page(self, userid, publication_id, source):
        cursor = self.con.cursor()
        cursor.execute('REPLACE INTO publication_page VALUES (?,?,?);', (userid, publication_id, source))
        cursor.close()
        self.con.commit()

    def get_publication_page(self, userid, publication_id):
        cursor = self.con.cursor()
        cursor.execute(
            'SELECT text FROM publication_page WHERE author_id == \'{}\' AND publication_id == \'{}\' ;'.format(userid, publication_id))
        items = cursor.fetchone()
        cursor.close()
        if items:
            return items[0]
        else:
            return None

    def add_citations_page(self, cluster_id, start, source):
        cursor = self.con.cursor()
        cursor.execute('REPLACE INTO citations_page VALUES (?,?,?);', (cluster_id, start, source))
        cursor.close()
        self.con.commit()

    def get_citations_page(self, cluster, start):
        cursor = self.con.cursor()
        cursor.execute(f'SELECT text FROM citations_page WHERE start == {start} AND cluster_id == \'{cluster}\' ;')
        items = cursor.fetchone()
        cursor.close()
        if items:
            return items[0]
        else:
            return None

    def add_versions_page(self, cluster_id, start, source):
        cursor = self.con.cursor()
        cursor.execute('REPLACE INTO versions_page VALUES (?,?,?);', (cluster_id, start, source))
        cursor.close()
        self.con.commit()

    def get_versions_page(self, cluster, start):
        cursor = self.con.cursor()
        cursor.execute(f'SELECT text FROM versions_page WHERE start == {start} AND cluster_id == \'{cluster}\' ;')
        items = cursor.fetchone()
        cursor.close()
        if items:
            return items[0]
        else:
            return None

    def dump(self):
        users = list(pd.read_sql_query("SELECT * from author_page", self.con)["author_id"])
        publications = list(pd.read_sql_query("SELECT * from publication_page", self.con)["publication_id"])
        links = list(pd.read_sql_query("SELECT * from citations_page", self.con)["cluster_id"])
        versions = list(pd.read_sql_query("SELECT * from versions_page", self.con)["cluster_id"])

        print(f"GoogleScholarCacheSQLite({self.db_file})")
        print(f"Authors pages in the Cache:{users}")
        print(f"Papers pages in the Cache:{publications}")
        print(f"Citations pages in the Cache:{links}")
        print(f"Versions pages in the Cache:{versions}")

    def clear(self):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM author_page;")
        cursor.execute("DELETE FROM publication_page;")
        cursor.execute("DELETE FROM citations_page;")
        cursor.close()
        self.con.commit()

    def close(self):
        self.con.close()

    def copy_into(self, cache):
        """
        Copy the cache into a different cache object
        In case of error GSInvalidCacheException is raised.
        :param cache: destination cache to fill
        :return: None
        """

        raise NotImplementedError

# End of file

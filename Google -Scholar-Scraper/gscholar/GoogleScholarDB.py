import os
import sqlite3
from sqlite3 import IntegrityError

import pandas as pd
from gscholar.utils.logger import error_log, debug_log, warning_log


def build_gs_db(db_file):
    debug_log(f"GoogleScholar DB {db_file} does not exist, create DB")
    con = sqlite3.connect(db_file)
    cursor = con.cursor()
    request = """
        CREATE TABLE authors (
            author_id varchar,
            name varchar,
            PRIMARY KEY (author_id) );"""
    cursor.execute(request)

    # TODO: For publications, would be good to have a author_ids, with any valid googlescholar author id.
    request = """
        CREATE TABLE publications (
            publication_cluster_id varchar,
            title varchar,
            year int,
            authors varchar,
            PRIMARY KEY (publication_cluster_id)  );"""
    cursor.execute(request)
    request = """
        CREATE TABLE citations (
            publication_cluster_id varchar,
            cited_by varchar,
            PRIMARY KEY (publication_cluster_id, cited_by) );"""
    cursor.execute(request)
    request = """
        CREATE TABLE authorship (
            author_id varchar,
            author_pub_id varchar,
            publication_cluster_id varchar,
            PRIMARY KEY (author_id, author_pub_id, publication_cluster_id) );"""
    cursor.execute(request)
    cursor.close()
    con.commit()
    con.close()


class GoogleScholarDB:

    def __init__(self, db_file):
        self.db_file = db_file
        if not os.path.exists(db_file):
            build_gs_db(db_file)
        self.con = sqlite3.connect(db_file)

    def add_author(self, a_id, a_name):
        cursor = self.con.cursor()
        new_row = (a_id, a_name)
        existing = cursor.execute(f"SELECT *  FROM authors WHERE author_id == '{a_id}';").fetchone()
        if existing:
            if existing != new_row:
                error_log(f"Existing author is not the same as new_row: {existing} != {new_row}")
        else:
            cursor.execute('INSERT INTO authors VALUES (?,?);', new_row)
        cursor.close()
        self.con.commit()

    def add_publication(self, pub_id: str, title: str, year: int, authors: list):

        import numpy as np
        cursor = self.con.cursor()

        # Check input types
        # =================

        try:
            np.isnan(year)
        except TypeError:
            year = np.nan

        if type(authors) is not list:
            error_log(f"Invalid author parameter: {authors}")
        assert (type(authors) is list)
        authors = ",".join(authors)

        new_row = (pub_id, title, None if np.isnan(year) else year, authors)

        # Check existing line
        # ===================
        existing = cursor.execute(f"SELECT publication_cluster_id, title, year, authors FROM publications "
                                  f"WHERE publication_cluster_id == '{pub_id}';").fetchone()
        if existing:
            # At this point pub_id is the same.

            # Check titles and resolve
            if new_row[1].lower() != existing[1].lower():
                min_len = min(len(new_row[1].lower()), len(existing[1].lower()))
                if new_row[1].lower()[:min_len] != existing[1].lower()[:min_len]:
                    error_log(f"Existing publication is not the same as in DB, titles are different.")
                    error_log(f"   {existing}")
                    error_log(f"   {new_row}")
                elif len(new_row[1].lower()) <= len(existing[1].lower()):
                    pass
                else:
                    warning_log(f"Existing publication is not the same as in DB, Title will be updated.")
                    warning_log(f"   {existing}")
                    warning_log(f"   {new_row}")
                    cursor.execute("UPDATE publications SET title = ? "
                                   f"WHERE publication_cluster_id == '{pub_id}';", (new_row[1],))

            # Check dates and resolve
            if new_row[2] != existing[2]:
                if new_row[2] is None:
                    pass
                elif existing[2] is None or existing[2] >= new_row[2]:
                    warning_log(f"Existing publication is not the same as in DB, Date will be updated.")
                    warning_log(f"   {existing}")
                    warning_log(f"   {new_row}")
                    cursor.execute("UPDATE publications SET year = ? "
                                   f"WHERE publication_cluster_id == '{pub_id}';", (new_row[2],))
                else:
                    pass

            # Check authors and resolve
            if new_row[3].lower() != existing[3].lower():
                if len(new_row[3].lower()) <= len(existing[3].lower()):
                    pass
                else:
                    warning_log(f"Existing publication is not the same as in DB, authors will be updated.")
                    warning_log(f"   {existing}")
                    warning_log(f"   {new_row}")
                    cursor.execute("UPDATE publications SET authors = ? "
                                   f"WHERE publication_cluster_id == '{pub_id}';", (new_row[3],))
        else:
            cursor.execute('INSERT INTO publications VALUES (?,?,?,?);', new_row)

        cursor.close()
        self.con.commit()

    def add_authorship(self, a_id, a_p_id, publication_id):
        cursor = self.con.cursor()
        new_row = (a_id, a_p_id, publication_id)
        try:
            cursor.execute('INSERT INTO authorship VALUES (?,?,?);', new_row)
        except IntegrityError:
            pass
        cursor.close()
        self.con.commit()

    def add_citation(self, publication_id, cited_by):
        cursor = self.con.cursor()
        new_row = (publication_id, cited_by)
        try:
            cursor.execute('INSERT INTO citations VALUES (?,?);', new_row)
        except IntegrityError:
            pass
        cursor.close()
        self.con.commit()

    def dump(self):
        authors = int(pd.read_sql_query("SELECT COUNT(*) as count from authors", self.con).iloc[0].iloc[0])
        publications = int(pd.read_sql_query("SELECT COUNT(*) from publications", self.con).iloc[0].iloc[0])
        authorship = int(pd.read_sql_query("SELECT COUNT(*) from authorship", self.con).iloc[0].iloc[0])
        citations = int(pd.read_sql_query("SELECT COUNT(*) from citations", self.con).iloc[0].iloc[0])
        print(f"GoogleScholarDB({self.db_file})")
        print(f"Authors count: {authors}")
        print(f"Publications count: {publications}")
        print(f"Citations count: {citations}")
        print(f"Authorship count: {authorship}")

    def clean(self):
        cursor = self.con.cursor()
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM publications")
        cursor.execute("DELETE FROM authorship")
        cursor.execute("DELETE FROM citations")
        cursor.close()
        self.con.commit()

    def close(self):
        self.con.close()

    def get_authors(self):
        """
                Return the list of all authors in DB
                :return: DataFrame
                """
        request = f"""
                    SELECT authors.author_id AS id, authors.name AS name, COUNT(authors.author_id) as publications  
                    FROM authors,authorship 
                    WHERE authors.author_id == authorship.author_id
                    GROUP BY authors.author_id
                ;
                """
        try:
            authors = pd.read_sql_query(request, self.con)
            return authors
        except sqlite3.OperationalError:
            error_log("get_authors: SQL Error.")
        return None

    def get_publications(self):
        """
                Return the list of all publications in DB
                :return: DataFrame
                """
        request = f"""
                    SELECT publication_cluster_id AS id, title, year, authors 
                    FROM publications
                ;
                """
        try:
            # TODO: , dtype={"year": np.int32}
            results = pd.read_sql_query(request, self.con)
            return results
        except sqlite3.OperationalError:
            error_log("get_publications: SQL Error.")
        return None

    def get_author_details(self, author_id):
        """
        Return the citations details of the author referred as author_id
        :param author_id:
        :return: DataFrame
        """
        request = f"""
                SELECT title, year, authors, citations, cluster_id, ROW_NUMBER () OVER ( ) as num FROM (
                    SELECT publications.title, publications.year, publications.authors, 
                         publications.publication_cluster_id 
                         AS cluster_id, COUNT(*) as citations FROM publications, citations , authorship
                    WHERE publications.publication_cluster_id == citations.publication_cluster_id
                    AND citations.publication_cluster_id == authorship.publication_cluster_id
                    AND author_id == "{author_id}" GROUP BY author_pub_id ORDER BY citations DESC
            )
        ;
        """
        try:
            details = pd.read_sql_query(request, self.con)
            return details
        except sqlite3.OperationalError:
            error_log("get_author_details: SQL Error.")
        return None

    def get_citations(self):
        """
                Return the list of all citations in DB
                :return: DataFrame
                """
        request = f"""
                    SELECT publication_cluster_id AS cluster_id, cited_by AS  cite_clusters FROM citations 
                ;
                """
        try:
            citations = pd.read_sql_query(request, self.con)
            return citations
        except sqlite3.OperationalError:
            error_log("get_citations: SQL Error.")
        return None

    def get_h_index(self, author_id):
        """
        Return the H-Index of the author referred as author_id
        :param author_id:
        :return: H-Index as an integer value
        """

        raise NotImplementedError

    def get_citation_graph(self, focus_authors=None):
        """
            This function return a NetworkX graph of citation from the database.
            :return: NetworkX graph
        """

        raise NotImplementedError

# End of file

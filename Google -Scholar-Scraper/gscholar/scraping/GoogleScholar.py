from tempfile import mkdtemp

from gscholar.scraping.cache.GoogleScholarCacheFile import GoogleScholarCacheFile
from gscholar.scraping.parser.GoogleScholarParser import GoogleScholarParser
from gscholar.scraping.crawler.GoogleScholarCrawler import GoogleScholarCrawler
import pandas as pd
from gscholar.utils.logger import debug_log


class GoogleScholar:

    def __init__(self, cache=None, crawler=None, parser=None):
        """
        To initialize the GoogleScholar object, we need a cache, a crawler and a parser.
        Non of these objects need to be specified. By default we will be using default instances of
         - GoogleScholarCacheFile
         - GoogleScholarCrawler
         - GoogleScholarParser
         However, it is reasonable to specify a particular cache, if not the google scholar website
         will certainly block you.
        :param cache: GoogleScholarCache object
        :param crawler: GoogleScholarCrawler
        :param parser: GoogleScholarParser
        """
        self.gs_cache = cache
        self.gs_crawler = crawler
        self.gs_parser = parser

        if not self.gs_cache:
            self.gs_cache = GoogleScholarCacheFile(mkdtemp())

        if not self.gs_crawler:
            self.gs_crawler = GoogleScholarCrawler(self.gs_cache)

        if not self.gs_parser:
            self.gs_parser = GoogleScholarParser()

    def get_author_publications(self, author_id):
        """
        This function returns a DataFrame of publications from an author.
        :param author_id: author id
        :return: DataFrame
        """

        assert self.gs_crawler
        author_page = self.gs_crawler.get_author_page(author_id)
        publication_df = GoogleScholarParser.parse_author_page_for_publications(author_page)
        return publication_df

    def get_author_publication_ids(self, author_id):
        """
        This function returns the list of publication ids from an author.
        :param author_id: author id
        :return: list
        """

        publication_df = self.get_author_publications(author_id)
        publications_list = [x for x in publication_df["pid"]]
        return publications_list

    def get_publication_details(self, author_id, publication_id):
        """
        Return the details of a particular publication
        :param author_id:
        :param publication_id:
        :return:
        """
        assert self.gs_crawler
        publication_page = self.gs_crawler.get_publication_page(author_id, publication_id)
        publication_details = GoogleScholarParser.parse_publication_page_for_details(publication_page)

        publication_details["author_id"] = author_id
        publication_details["author_publication_id"] = publication_id

        return publication_details

    def get_author_publications_details(self, author_id):
        """
        Return a DataFrame that contains details of every publications from the author.
        :param author_id: author id
        :return: pandas.DataFrame
        """
        publications_list = self.get_author_publication_ids(author_id)
        publications = {}
        for publication_id in publications_list:
            publication_details = self.get_publication_details(author_id, publication_id)
            publications[publication_id] = publication_details

        df = pd.DataFrame.from_dict(publications, orient='index')
        return df

    def get_citations(self, cluster_id):
        assert self.gs_crawler
        pages = self.gs_crawler.get_all_citations_pages(cluster_id)
        citations = {}
        for page in pages:
            citations = {**citations, **GoogleScholarParser.parse_items_page_for_details(page)}
        debug_log("Done with {} citations.".format(len(citations)))

        df = pd.DataFrame([pd.Series(x) for x in citations.values()])
        return df

    def get_versions(self, cluster_id):
        assert self.gs_crawler
        pages = self.gs_crawler.get_all_versions_pages(cluster_id)
        versions = {}
        for page in pages:
            versions = {**versions, **GoogleScholarParser.parse_items_page_for_details(page)}
        debug_log("Done with {} versions.".format(len(versions)))

        df = pd.DataFrame([pd.Series(x) for x in versions.values()])
        return df

    def crawl_author(self, author_id, distance=0, with_versions=False):
        publications_details = self.get_author_publications_details(author_id)
        loop_cited = publications_details.copy()
        for i in range(distance):
            loop_cited = pd.concat(self.get_citations(cluster_id) for cluster_id in loop_cited["cites"].sum())
            if with_versions:
                _ = pd.concat(self.get_versions(cluster_id) for cluster_id in loop_cited["clusters"].sum())

    def get_author_details(self, author_id):
        assert self.gs_crawler
        author_page = self.gs_crawler.get_author_page(author_id)
        author_details = GoogleScholarParser.parse_author_page_for_details(author_page)
        return author_details

    def terminate_crawler(self):
        self.gs_crawler.terminate()
        self.gs_crawler = None

# End of file

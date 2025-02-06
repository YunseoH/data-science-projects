"""
The GoogleScholarCache is a cache storage used to store web page from GS.
It stores webpages by type of data.

TODO: Possible improvement, add Timestamps.
"""
from abc import ABC, abstractmethod


class GoogleScholarCache (ABC):

    def __init__(self):
        """
        The child function is expected to open or create the db,
        and making sure it is correct.
        """
        pass

    @abstractmethod
    def add_author_page(self, userid, source):
        """
        Store the unrolled author web page source for a particular userid inside the cache
        :param userid:
        :param source:
        :return: None
        """
        pass

    @abstractmethod
    def get_author_page(self, userid):
        """
        Retrieve the author web page for userid.
        :param userid:
        :return: String of the web page
        """
        pass

    @abstractmethod
    def add_publication_page(self, userid, publication_id, source):
        """
        Store the publication web page source for a particular userid+publication_id inside the cache
        :param userid:
        :param publication_id:
        :param source:
        :return: None
        """
        pass

    @abstractmethod
    def get_publication_page(self, userid, publication_id):
        """
        Retrieve the publication web page for userid+publication_id.
        :param userid:
        :param publication_id:
        :return: String of the web page
        """
        pass

    @abstractmethod
    def add_citations_page(self, cluster_id, start, source):
        """
        Store the citations web page source for a particular cluster_id+start inside the cache
        :param cluster_id:
        :param start:
        :param source:
        :return: None
        """
        pass

    @abstractmethod
    def get_citations_page(self, cluster, start):
        """
        Retrieve the citation web page for cluster+start.
        :param cluster:
        :param start:
        :return: String of the web page
        """
        pass

    @abstractmethod
    def add_versions_page(self, cluster_id, start, source):
        """
        Store the versions web page source for a particular cluster_id+start inside the cache
        :param cluster_id:
        :param start:
        :param source:
        :return: None
        """
        pass

    @abstractmethod
    def get_versions_page(self, cluster, start):
        """
        Retrieve the versions web page for cluster+start.
        :param cluster:
        :param start:
        :return: String of the web page
        """
        pass

    @abstractmethod
    def dump(self):
        """
        print the content of the cache database in any format to stdout.
        :return: None
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Empty the cache database.
        :return: None
        """
        pass

    @abstractmethod
    def copy_into(self, cache):
        """
        Copy the cache into a different cache object
        :param cache: GoogleScholarCache object
        :return: None
        """
        pass
# End of file

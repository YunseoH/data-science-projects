from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from random import randint
from time import sleep
from gscholar.utils.logger import debug_log, error_log, warning_log
from gscholar.utils.GSError import GSException

CRAWLING_MIN_SLEEP = 8
CRAWLING_MAX_SLEEP = 10

try:
    import lxml

    assert lxml
except ModuleNotFoundError:
    error_log("The package 'lxml' must be installed.")
    raise GSException("The package 'lxml' must be installed.")


def beep_me():
    try:
        import beepy
        beepy.beep(2)
    except ImportError:
        pass


def rand_sleep(min_dur=2, max_dur=4):
    sleep_time = randint(min_dur, max_dur)
    debug_log(f"**** Sleep for {sleep_time}\n")
    sleep(sleep_time)


class FakeDriver:
    page_source = None

    def get(self, url):
        debug_log(f"Fake Driver has been used: get({url}).")
        return self.page_source

    def find_element_by_id(self, eid):
        debug_log(f"Fake Driver has been used: find_element_by_id({eid}).")
        return []

    def close(self):
        debug_log("Fake Driver has been used: close().")
        return


def find_next_link(source, cluster_tag):
    import bs4
    soup = bs4.BeautifulSoup(source, features="lxml")

    all_nave = soup.find_all("div", attrs={"id": "gs_n"})
    if len(all_nave) == 0:
        return None
    nav = soup.find_all("div", attrs={"id": "gs_n"})[-1]
    last_td = nav.find_all("td")[-1]
    last_a = last_td.find_all("a")
    if last_a:
        url = last_a[-1].attrs['href']
        from urllib.parse import urlsplit, parse_qs
        query = urlsplit(url).query
        params = parse_qs(query)
        debug_log(f"next url is {url}")
        debug_log(f"next params is {params}")
        cur_cluster = params[cluster_tag][0]
        debug_log(f"next cluster is {cur_cluster}")
        return int(params["start"][0])
    else:
        return None


class GoogleScholarCrawler:
    """
    This part initialize the Crawler, Cache and Driver.
    """

    def __init__(self, cache, driver=None):
        self.db = cache
        self.driver = driver

    def get_driver(self):
        from packaging import version

        if self.driver:
            return self.driver
        try:
            # options = webdriver.FirefoxOptions()
            # executable_path="/usr/bin/flatpak-spawn", service_args=["--host", "/usr/local/bin/geckodriver"],
            try:
                from webdriver_manager.firefox import GeckoDriverManager
                if version.parse(webdriver.__version__) < version.parse("4.6.0"):
                    self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
                else:
                    self.driver = webdriver.Firefox()
            except ModuleNotFoundError as err:
                warning_log("Error with webdriver_manager, module not found, error was:" + str(err))
                error_log("Fallback to webdriver.Firefox directly")
                self.driver = webdriver.Firefox()
        except WebDriverException as err:
            error_log("Selenium webdriver did not work. Fall back to FakeDriver, error was:" + str(err))
            self.driver = FakeDriver()
        return self.driver

    """
    This function collects a page using Selenium, making sure there is no robot check before
    """

    def is_robot_page(self, page_source):

        return "Please show you're not a robot" in page_source or \
            "unusual traffic" in page_source or \
            "Prouvez que vous" in page_source or \
            "We're sorry..." in page_source

    """
    This function collects a page using Selenium, making sure there is no robot check before
    """

    def get_page_and_wait_robot(self, url):
        driver = self.get_driver()
        debug_log(f"Get page: {url}")
        driver.get(url=url)
        if not driver.page_source:
            return None
        while self.is_robot_page(driver.page_source):
            beep_me()
            rand_sleep(min_dur=CRAWLING_MIN_SLEEP, max_dur=CRAWLING_MAX_SLEEP)
        rand_sleep(min_dur=CRAWLING_MIN_SLEEP, max_dur=CRAWLING_MAX_SLEEP)
        page = driver.page_source

        return page

    """
    Author pages are stored in cache or downloaded
    """

    def get_author_page(self, userid):
        page = self.db.get_author_page(userid)
        if not page or self.is_robot_page(page):
            page = self.get_author_page_online(userid)
            if page and not self.is_robot_page(page):
                self.db.add_author_page(userid, page)
        assert page and (not self.is_robot_page(page))
        return page

    def get_author_page_online(self, user):

        from selenium.webdriver.common.by import By
        driver = self.get_driver()
        debug_log("get_author_page " + user)

        # For a while it was required to load the page twice to avoid a human test.
        # it is not the case anymore. But it is not a big deal to continue.
        _ = self.get_page_and_wait_robot("https://scholar.google.com")
        _ = self.get_page_and_wait_robot(f"https://scholar.google.com/citations?user={user}&hl=en&oi=ao")

        count = driver.find_element(By.ID, "gsc_a_nn")
        button = driver.find_element(By.ID, "gsc_bpf_more")
        if not (count and button):
            return None
        last_count = count.text
        while button.is_enabled():
            debug_log("Current count is " + count.text)
            button.click()
            rand_sleep(min_dur=CRAWLING_MIN_SLEEP, max_dur=CRAWLING_MAX_SLEEP)
            if last_count == count.text:
                break
            else:
                last_count = count.text
        debug_log("unrolled done.")
        res = driver.page_source
        debug_log("END OF get_author_page len of res " + str(len(res)))
        return res

    """
    Publication pages are stored in cache or downloaded
    """

    def get_publication_page(self, userid, pub_id):
        page = self.db.get_publication_page(userid, pub_id)
        if not page or self.is_robot_page(page):
            page = self.get_publication_page_online(userid, pub_id)
            if page and not self.is_robot_page(page):
                self.db.add_publication_page(userid, pub_id, page)
        assert page and (not self.is_robot_page(page))
        return page

    def get_publication_page_url(self, aut_code, pub_code):
        return f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={aut_code}&citation_for_view={aut_code}:{pub_code}"

    def get_publication_page_online(self, aut_code, pub_code):
        url = self.get_publication_page_url(aut_code, pub_code)
        page = self.get_page_and_wait_robot(url)
        return page

    def get_citations_page(self, cluster_id=None, start=None):

        if start and start > 0:
            url = f"https://scholar.google.com/scholar?start={start}&cites={cluster_id}&as_sdt=2005&hl=en"
        else:
            url = f"https://scholar.google.com/scholar?cites={cluster_id}&as_sdt=2005&hl=en"

        page = self.db.get_citations_page(cluster_id, start)

        # Make sure there is no crap in the DataBase
        if page and self.is_robot_page(page):
            error_log("Crap found in the DB")
            print(page)
            page = None

        if not page:
            page = self.get_page_and_wait_robot(url)
            if page:
                self.db.add_citations_page(cluster_id, start, page)

        assert page and (not self.is_robot_page(page))

        return page

    def get_versions_page(self, cluster_id=None, start=None):

        if start and start > 0:
            url = f"https://scholar.google.com/scholar?start={start}&cluster={cluster_id}&as_sdt=0,5&hl=en"
        else:
            url = f"https://scholar.google.com/scholar?cluster={cluster_id}&as_sdt=0,5&hl=en"

        page = self.db.get_versions_page(cluster_id, start)

        # Make sure there is no crap in the DataBase
        if page and self.is_robot_page(page):
            error_log("Crap found in the DB")
            page = None

        if not page:
            page = self.get_page_and_wait_robot(url)
            if not ("Please show you're not a robot" in page):
                self.db.add_versions_page(cluster_id, start, page)

        assert page and (not self.is_robot_page(page))

        return page

    def get_all_citations_pages(self, cluster_id):

        pages = []
        page = self.get_citations_page(cluster_id=cluster_id, start=0)
        pages.append(page)

        while find_next_link(page, cluster_tag="cites"):
            next_start = find_next_link(page, cluster_tag="cites")
            page = self.get_citations_page(cluster_id=cluster_id, start=next_start)
            pages.append(page)
        return pages

    def get_all_versions_pages(self, cluster_id):

        pages = []
        page = self.get_versions_page(cluster_id=cluster_id, start=0)
        pages.append(page)

        while find_next_link(page, cluster_tag="cluster"):
            next_start = find_next_link(page, cluster_tag="cluster")
            page = self.get_versions_page(cluster_id=cluster_id, start=next_start)
            pages.append(page)
        return pages

    def terminate(self):
        if self.driver:
            self.driver.close()
            self.driver = None

# End of file

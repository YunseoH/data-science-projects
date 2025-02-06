import unittest


class GoogleScholarParserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def test_parse_clusters_and_cites_simple(self):
        from gscholar.scraping.parser.GoogleScholarParser import parse_clusters_and_cites
        import bs4

        source = """
        <div class="gsc_oci_value"><div class="gsc_oci_merged_snippet"><div>
        <a href="/scholar?oi=bibs&amp;cluster=15885577448857307637&amp;btnI=1&amp;hl=en">
        Navigating the landscape for real-time localization and mapping for robotics and virtual and augmented reality
        </a></div>
        <div>S Saeedi, B Bodin, H Wagstaff, A Nisbet, L Nardi… - 
        Proceedings of the IEEE, 2018</div><div><a class="gsc_oms_link"
         href="https://scholar.google.com/scholar?oi=bibs&amp;hl=en&amp;cites=15885577448857307637&amp;as_sdt=5">
        Cited by 27</a> <a class="gsc_oms_link" 
        href="https://scholar.google.com/scholar?oi=bibs&amp;hl=en&amp;q=related:9YkYO4bodNwJ:scholar.google.com/">
        Related articles</a>
         <a class="gsc_oms_link" 
         href="https://scholar.google.com/scholar?oi=bibs&amp;hl=en&amp;cluster=15885577448857307637">
         All 10 versions</a> </div></div></div>
        """
        div = bs4.BeautifulSoup(source, features="lxml")
        result = parse_clusters_and_cites(div)
        print(result)
        self.assertEqual(result.get("clusters", []), ['15885577448857307637'])
        self.assertEqual(result.get("cites", []), ['15885577448857307637'])

    def test_parse_clusters_and_cites_hard(self):
        from gscholar.scraping.parser.GoogleScholarParser import parse_clusters_and_cites
        import bs4

        source = """
        <div class="gs_ggs gs_fl"><div class="gs_ggsd">
        <div class="gs_or_ggsm" ontouchstart="gs_evt_dsp(event)" tabindex="-1">
        <a data-clk="hl=en&amp;sa=T&amp;oi=gga&amp;ct=gga&amp;cd=1&amp;d=8375544786905858486&amp;ei=4oMpYvyWBKuM6rQPuriX8A4" 
        data-clk-atid="tgHmr5vpO3QJ" 
        href="https://deepblue.lib.umich.edu/bitstream/handle/2027.42/169877/dohypark_1.pdf?sequence=1">
        <span class="gs_ctg2">[PDF]</span> umich.edu</a></div></div></div>
        """
        div = bs4.BeautifulSoup(source, features="lxml")
        result = parse_clusters_and_cites(div)
        print(result)
        self.assertEqual(result.get("clusters", []), ['8375544786905858486'])
        self.assertEqual(result.get("cites", []), ['8375544786905858486'])

    def test_parse_author_page_for_publications(self):
        from gscholar.scraping.parser.GoogleScholarParser import GoogleScholarParser
        import pathlib
        test_folder = pathlib.Path(__file__).parent.resolve()
        with open(f"{test_folder}/author_page_sample.html") as fd:
            source = fd.read()
        df = GoogleScholarParser.parse_author_page_for_publications(source)
        print(df)

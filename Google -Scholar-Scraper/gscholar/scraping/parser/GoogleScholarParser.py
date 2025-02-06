import datetime
import bs4
from urllib.parse import urlparse, parse_qs

import pandas as pd

from gscholar.utils.logger import debug_log, warning_log, error_log


def parse_clusters_and_cites(div):
    """
    This function is HTML parse for clusters and cites
    Used twice
    """
    clusters = []
    cites = []
    for link in div.find_all("a"):
        parsed_url = urlparse(link.attrs["href"])
        parsed_qs = parse_qs(parsed_url.query)

        if "cluster" in parsed_qs:
            clusters = list(set(clusters + parsed_qs["cluster"]))
        elif "cites" in parsed_qs:
            cites = list(set(cites + parsed_qs["cites"]))
        elif "q" in parsed_qs:
            pass
        else:
            assert not ("cites" in link)
            assert not ("cluster" in link)
        if "data-clk" in link.attrs:
            parsed_data_clk = urlparse(link.attrs["data-clk"])
            parsed_qs = parse_qs(parsed_data_clk.path)
            if "d" in parsed_qs and len(clusters) == 0:
                clusters = parsed_qs["d"]
                cites = parsed_qs["d"]
    if not len(clusters) and "[CITATION]" not in div.text:
        error_log(f"Fix me, cannot find cluster identifier:\n{div}")
        raise BaseException("FIXME")
    return {"clusters": clusters,
            "cites": cites}


def get_url_from_citation_div(div):
    h3title = div.find_all("h3", attrs={"class": "gs_rt"})
    assert (len(h3title) == 1)
    h3 = h3title[0]
    title = None
    if h3.a:
        title = h3.a.href
    return title


def get_title_from_citation_div(div):
    h3title = div.find_all("h3", attrs={"class": "gs_rt"})
    assert (len(h3title) == 1)
    h3 = h3title[0]

    if h3.a:
        title = h3.a.text
        assert (h3.a.attrs['id'] == div.attrs["data-cid"])
    elif "[CITATION][C]" in h3.text:
        title = h3.text[13:]
    else:
        title = h3.text
        warning_log("Warning with h3=" + str(h3.text))
    return title


class GoogleScholarParser:

    @staticmethod
    def parse_author_page_for_publications(page_source):
        debug_log("parse_author_page_for_publications (...)")
        try:
            soup = bs4.BeautifulSoup(page_source, features="lxml")
        except BaseException:
            error_log("parse_author_page_for_publications: Failed to parse the page")
            return None

        publications = []

        tbody = soup.find_all(name="tbody", attrs={"id": "gsc_a_b"})
        assert tbody and len(tbody) == 1

        for tr in tbody[0].find_all("tr"):
            row_infos = {"title": None, "authors": None, "venue": None,
                         "citations": None, "year": None, "pid": None, "clustered": False}

            if 'gsc_a_tr' in tr.attrs.get('class', []):
                for td in tr.find_all("td"):
                    if 'gsc_a_t' in td.attrs.get('class', []):
                        assert (len(td) == 3)
                        row_infos["title"] = td.find_all()[0].getText()
                        row_infos["authors"] = td.find_all()[1].getText()
                        row_infos["venue"] = td.find_all()[2].getText()

                        parsed = urlparse(td.find_all("a")[0].attrs.get('href'))
                        tmp = parsed.query.split("&")
                        dic = dict([x.split("=") for x in tmp])
                        row_infos["pid"] = dic["citation_for_view"].split(":")[1]
                    if 'gsc_a_c' in td.attrs.get('class', []):
                        row_infos["citations"] = int(td.getText().strip("*")) if td.getText() != "" else 0
                        row_infos["clustered"] = "*" in td.getText()
                    if 'gsc_a_y' in td.attrs.get('class', []):
                        row_infos["year"] = int(td.getText()) if td.getText() != "" else None

            publications += [row_infos]

        return pd.DataFrame(publications)
        # for a in soup.find_all("a"):
        #     if 'gsc_a_at' in a.attrs.get('class', []):
        #         parsed = urlparse(a.attrs.get('href'))
        #         debug_log("Parse href url from " + str(a))
        #         splitted = parsed.query.split("&")
        #         dic = dict([x.split("=") for x in splitted])
        #         links.append(dic["citation_for_view"].split(":")[1])
        # return links

    @staticmethod
    def parse_publication_page_for_details(text):
        debug_log(f"Parse_publication_detail ({len(text)})")

        try:
            soup = bs4.BeautifulSoup(text, features="lxml")
        except BaseException:
            error_log("parse_publication_page_for_details: Page is not a valid HTML")
            return None

        title_div = soup.find_all("div", attrs={"id": "gsc_oci_title"})
        if not (len(title_div) == 1):
            error_log(f"Wrong data size : (len(title_div) == 1), title_div = {title_div}")
            return {}
        # assert (len(title_div) == 1)
        title = title_div[0].text

        items = {'title': title, 'date': None}

        #:
        #    warning_log(f"Multiple titles.")

        # for a in soup.find_all("a") :
        #    if 'gsc_vcd_title_link' in a.attrs.get('class',[]) :
        #        items["title"] = a.text
        #        title = a.text

        debug_log(f"Title is {title}")
        field = None
        for div in soup.find_all("div"):
            if 'gsc_oci_field' in div.attrs.get('class', []):
                field = div.text
            if 'gsc_oci_value' in div.attrs.get('class', []):
                assert field

                if field == "Authors":
                    items["authors"] = div.text.split(",")
                elif field == "Publication date":
                    try:
                        items["date"] = datetime.datetime.strptime(div.text, '%Y/%m/%d')
                    except ValueError:
                        try:
                            items["date"] = datetime.datetime.strptime(div.text, '%Y')
                        except ValueError:
                            try:
                                items["date"] = datetime.datetime.strptime(div.text, '%Y/%m')
                            except ValueError:
                                items["date"] = div.text
                elif field == "Total citations":
                    items["citations"] = div.a.attrs["href"]
                elif field == "Scholar articles":
                    candc = parse_clusters_and_cites(div)
                    items["clusters"] = candc["clusters"]
                    items["cites"] = candc["cites"]

                elif field is None:
                    error_log("ERROR, no field for div = " + div)
                else:
                    debug_log("UNKNOWN, no field for div = " + field)
                    items[field.lower().replace(" ", "")] = div.text
                field = None
        if not items["date"]:
            error_log(f"Date not found from paper: {title}")
        return items

    @staticmethod
    def parse_items_page_for_details(text):
        items = {}
        try:
            soup = bs4.BeautifulSoup(text, features="lxml")
        except BaseException:
            error_log("parse_items_page_for_details: Page is not a valid HTML")
            return None
        for div in soup.find_all("div", attrs={"class": "gs_scl"}):
            assert ("data-cid" in div.attrs)
            datadict = {}

            # Get Title string
            title = get_title_from_citation_div(div)
            datadict["title"] = title

            # Get URL string
            url = get_url_from_citation_div(div)
            datadict["url"] = url

            # Get Authors, Venue, Year
            gs_a = div.find_all("div", attrs={"class": "gs_a"})
            assert (len(gs_a) == 1)
            gs_a_string = gs_a[0].text
            gs_a_split = gs_a_string.split("- ")

            # CASE 1: S Saeedi, EDC Carvalho, W Li… - … on Robotics and …, 2019 - ieeexplore.ieee.org
            debug_log(f"\n{gs_a_split}\n")
            if len(gs_a_split) == 3 and len(gs_a_split[1].split(",")) >= 2:

                debug_log("\nCASE 1\n")
                datadict["venue"] = gs_a_split[1].split(",")[0:-1]
                try:
                    datadict["year"] = int(gs_a_split[1].split(",")[-1])
                except ValueError:
                    datadict["year"] = None
                datadict["authors"] = gs_a_split[0].split(",")
                datadict["server"] = gs_a_split[2]
            # CASE 2: T Beattie - 2015 - Master's thesis, The University of …,
            elif len(gs_a_split) == 3 and len(gs_a_split[1].split(",")) == 1:

                debug_log("\nCASE 2\n")
                datadict["venue"] = gs_a_split[2]
                try:
                    datadict["year"] = int(gs_a_split[1])
                except ValueError:
                    datadict["year"] = None
                datadict["authors"] = gs_a_split[0].split(",")
                datadict["server"] = None
            # Case3: M Bujanca, P Gafton, S Saeedi, A Nisbet, B Bodin… - research.manchester.ac.uk
            elif len(gs_a_split) == 2:

                debug_log("\nCASE 3\n")
                datadict["venue"] = gs_a_split[1]
                datadict["year"] = None
                datadict["authors"] = gs_a_split[0].split(",")
                datadict["server"] = None
            # Case 4: only authors
            elif (len(gs_a_split) == 1) and (len(gs_a_string.split("- ")) == 1):

                debug_log("\nCASE 4\n")
                datadict["venue"] = None
                datadict["year"] = None
                datadict["authors"] = gs_a_split[0].split(",")
                datadict["server"] = None
            # Case 5: L Luo, P West, J Nelson, A Krishnamurthy, L Ceze - Proceedings of the 3rd MLSys …, 2020,
            elif (len(gs_a_split) == 1) and (len(gs_a_string.split("- ")) > 1):
                debug_log("\nCASE 5\n")
                datadict["venue"] = None

                try:
                    datadict["year"] = int(gs_a_string.split(", ")[-1])
                except ValueError:
                    datadict["year"] = None

                datadict["authors"] = gs_a_string.split("- ")[0].split(",")
                datadict["server"] = None
            else:
                error_log(f"Unsupported case gs_a = {gs_a_string}, len = {len(gs_a_split)}")

            # Get Clusters and cites
            gs_ri = div.find_all("div", attrs={"class": "gs_ri"})
            if len(gs_ri) >= 1:  # TODO Case > 1 need to be fixed
                for part in gs_ri:
                    candc = parse_clusters_and_cites(part)
                    if candc:
                        datadict["clusters"] = candc["clusters"]
                        datadict["cites"] = candc["cites"]
            elif len(gs_ri) == 0:
                datadict["clusters"] = None
                datadict["cites"] = None
            else:
                error_log(f"Invalid HTML for {title} with len(gs_ri) = " + str(len(gs_ri)))
            datadict["raw"] = div
            items[div.attrs["data-cid"]] = datadict
            # debug_log ("\n\n", div, items)
        if len(items) > 10:
            warning_log("Warning too many citations:" + str(items))
        return items

    @staticmethod
    def parse_author_page_for_details(page_source):
        debug_log("parse_author_page_for_details (...)")
        res = {}
        try:
            soup = bs4.BeautifulSoup(page_source, features="lxml")
        except BaseException:
            error_log(f"parse_author_page_for_details: the page is not a valid HTML: {page_source}")
            return None
        profile = soup.find_all("div", attrs={"id": "gsc_prf"})
        if len(profile) == 1:
            profile = profile[0]
        else:
            return res
        author_name_div = profile.find_all("div", attrs={"id": "gsc_prf_in"})
        author_role_div = profile.find_all("div", attrs={"class": "gsc_prf_il"})
        author_homepage_div = profile.find_all("div", attrs={"id": "gsc_prf_ivh"})[0]
        author_homepage_a = author_homepage_div.find_all("a", attrs={"class": "gsc_prf_ila"})

        res["name"] = author_name_div[0].text if len(author_name_div) else None
        res["role"] = author_role_div[0].text if len(author_role_div) else None
        res["homepage"] = author_homepage_a[0].attrs["href"] if len(author_homepage_a) else None
        return res

import os.path
from bs4 import BeautifulSoup
import urllib.parse
import requests
import time

from text_maniupularion import remove_newline_characters, clean_text


def get_part_numbers_from_csv(filename):
    if os.path.exists(filename):
        f = open(filename)
        res = [remove_newline_characters(line) for line in f]
        f.close()
        return res
    else:
        return None


def get_html_from_alldatasheet(search_term):
    r = requests.get("https://www.alldatasheet.com/view.jsp?Searchword={}".format(urllib.parse.quote(search_term)))
    if r.status_code != 200:
        raise RuntimeError
    time.sleep(0.8)
    return r.content


def extract_main_table(bs_obj):
    # get first table with the class of main
    return bs_obj.find_all("table", {"class": "main"})[5]


def get_table_row(table_obj, offset=0):
    # returns the table row
    return table_obj.find_all_next("tr")[1 + offset]


def get_part_descriptions(table_obj):
    # gets a list of up to three descriptions of the part (in case one of them is for the wrong part)
    res = []
    for i in range(0, 3):
        row = get_table_row(table_obj, i)
        res.append(clean_text(row.find_all_next("td")[3].get_text().split("\n")[0]))
    return res


def get_datasheet_link(table_obj):
    row = get_table_row(table_obj)
    return "https://pdf1.alldatasheet.com/datasheet-pdf/view/" + "/".join(
        row.find_all_next("a")[0]['href'].split("/")[5:])


def get_item_table(html):
    soup = BeautifulSoup(html, "html.parser")
    return extract_main_table(soup)
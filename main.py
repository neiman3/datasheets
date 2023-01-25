import os.path
from bs4 import BeautifulSoup
import urllib.parse
import requests


def get_part_numbers_from_csv(filename):
    if os.path.exists(filename):
        f = open(filename)
        res = [remove_newline_characters(line) for line in f]
        f.close()
        return res
    else:
        return None


def remove_newline_characters(string):
    res = ""
    for c in string:
        if not (c == "\n" or c == "\r"):
            res += c
    return res


def get_html_from_octopart(search_term):
    r = requests.get("https://www.alldatasheet.com/view.jsp?Searchword={}".format(urllib.parse.quote(search_term)))
    if r.status_code != 200:
        raise RuntimeError
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
        res.append(row.find_all_next("td")[3].get_text().split("\n")[0])
    return res


def get_datasheet_link(table_obj):
    row = get_table_row(table_obj)
    return "https://pdf1.alldatasheet.com/datasheet-pdf/view/" + "/".join(
        row.find_all_next("a")[0]['href'].split("/")[5:])


def filenames():
    # returns open file, save to file
    file_in = prompt_entry("Open CSV file: > ")
    dir_in = prompt_entry("Save to directory: > ", mode='folder')
    save_as = input("Save as: > ")
    save_as = os.path.join(dir_in, save_as)
    return file_in, save_as


def prompt_entry(prompt='> ', mode='file', msg=None, count=0):
    if not (mode == 'file' or mode == 'folder'):
        raise ValueError("Mode must be \'file\' or \'folder\'")
    if count >= 5:
        raise FileNotFoundError
    if msg is not None:
        print(msg)
    filename = input(prompt)
    if mode == 'file':
        if os.path.isfile(filename):
            return filename
        else:
            if os.path.isdir(filename):
                return prompt_entry(prompt, mode, "Error: specified path is a directory", count + 1)
            return prompt_entry(prompt, mode, "Error: file does not exist", count + 1)
    else:
        if os.path.isdir(filename):
            return filename
        else:
            return prompt_entry(prompt, mode, "Error: directory does not exist", count + 1)


def main():
    (file_in, file_out) = filenames()
    return
    file_in = "/Users/neiman/Desktop/partslist1.csv"
    file_out = "/Users/neiman/Desktop/partslist2.csv"
    parts = get_part_numbers_from_csv(file_in)
    res = []
    for part in parts:
        html = get_html_from_octopart(part)
        soup = BeautifulSoup(html, "html.parser")
        main_table = extract_main_table(soup)
        descriptions = get_part_descriptions(main_table)
        url = get_datasheet_link(main_table)
        res.append(",".join([part, url] + descriptions))
    f = open(file_out, 'w')
    for line in res:
        f.write(line)
        f.write("\n")
    f.close()


main()

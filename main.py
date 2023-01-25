from datasheets import *
from file_prompt import filenames
from text_maniupularion import clean_text

if __name__ == "__main__":
    # prompt user for CSV file names- one to read from and one to write to. Can be
    (file_in, file_out) = filenames()

    # parse the file to get a list of parts
    parts = get_part_numbers_from_csv(file_in)
    res = []
    for part in parts:
        html = get_html_from_octopart(part)
        get_item_table(html)
        descriptions = get_part_descriptions(main_table)
        url = get_datasheet_link(main_table)
        res.append(",".join([clean_text(part), url] + clean_text(descriptions)))
    f = open(file_out, 'w')
    for line in res:
        f.write(line)
        f.write("\n")
    f.close()
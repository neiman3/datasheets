from datasheets import *
from file_prompt import filenames
from text_maniupularion import clean_text, print_same_line, estimated_time_completion

if __name__ == "__main__":
    # prompt user for CSV file names- one to read from and one to write to. Can be
    # (file_in, file_out) = filenames()
    file_in, file_out = './examples/input.csv', './examples/output.csv'
    # parse the file to get a list of parts
    print("\nLoading your file...")
    parts = get_part_numbers_from_csv(file_in)
    j = len(parts)
    print("Found {} parts in file.".format(j))
    print(" ")
    res = []
    for i in range(len(parts)):
        part = parts[i]
        print_same_line("Downloading data from AllDatasheet ({}/{}, {} remaining)".format(i+1,j,estimated_time_completion(i,j,avg_time=1)))
        html = get_html_from_alldatasheet(part)
        main_table = get_item_table(html)
        descriptions = get_part_descriptions(main_table)
        url = get_datasheet_link(main_table)
        res.append(",".join([clean_text(part), url] + descriptions))
    print_same_line("Downloaded {} part details.".format(j))
    print("Saving to {}...".format(file_out))
    f = open(file_out, 'w')
    for line in res:
        f.write(line)
        f.write("\n")
    f.close()
    print("Saved file.")
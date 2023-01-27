from datasheets import *
from file_prompt import filenames
from text_manipulation import *

if __name__ == "__main__":
    # prompt user for CSV file names- one to read from and one to write to. Can be
    (file_in, file_out) = filenames()

    # parse the file to get a list of parts
    print("\nLoading your file...")
    parts = get_part_numbers_from_csv(file_in)

    # some interface and formatting
    j = len(parts)
    print("Found {} parts in file.".format(j))
    print(" ")

    # look up each part
    res = []
    for i in range(len(parts)):
        part = parts[i]
        print_same_line("Downloading data from AllDatasheet ({}/{}, {} remaining)".format(i+1,j,estimated_time_completion(i,j,avg_time=1)))
        # make the request and get the HTML content
        html = get_html_from_alldatasheet(part)
        # Parse the results table from the DOM
        main_table = get_item_table(html)
        # extract the data
        descriptions = get_part_descriptions(main_table)
        url = get_datasheet_link(main_table)
        # Make a CSV formatted line with the format:
        # [part number], [url], [description 1], [description 2], [description 3]
        description = pick_best_description(part, descriptions)
        res.append(",".join([clean_text(part), '"=HYPERLINK(""{}"",""DATASHEET"")"'.format(url), description]))

    # interface
    print_same_line("Downloaded {} part details.".format(j))
    print("Optimizing descriptions...")

    print("Saving to {}...".format(file_out))

    # write to file
    f = open(file_out, 'w')
    for line in res:
        f.write(line)
        f.write("\n")
    f.close()
    print("Saved file.")
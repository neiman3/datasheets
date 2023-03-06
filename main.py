from datasheets import *
from file_prompt import filenames
from text_manipulation import *
from unidecode import unidecode
from filemanip import extract_folder
import os, csv
from nexar import NexarClient


def get_api_key(key_filename):
    if not os.path.exists(key_filename):
        print("""Warning: The API key file (\'apikey.txt\') does not exist.\nYou can create it now or manually exit the program.""")
        client_id = input("Client ID > ")
        secret_id = input("Secret ID > ")
        keys = {"client": client_id, "secret": secret_id}
        with open(key_filename, 'w') as file_obj:
            json.dump(keys, file_obj, indent=4)
    else:
        with open(key_filename, 'r') as fp:
            keys = json.load(fp)
            # print("Loaded {} with secret {}".format(keys['client'], keys['secret']))
            if not ("client" in keys and "secret" in keys):
                print("Error: malformed API key")
                raise RuntimeError
    return keys


if __name__ == "__main__":
    # auth first
    root_dir = extract_folder()
    filename = os.path.join(root_dir, 'apikey.txt')
    apikey = get_api_key(filename)

    # prompt user for CSV file names- one to read from and one to write to.
    print("Welcome to the datasheet tool.")
    (file_in, file_out) = filenames(testing=False)

    # parse the file to get a list of parts
    print("\nLoading your file...")
    parts = get_part_numbers_from_csv(file_in)

    # some interface and formatting
    j = len(parts)
    print("Found {} parts in file.".format(j))
    print(" ")

    # make the request and get the HTML content
    client = NexarClient(apikey['client'], apikey['secret'])
    results = []
    j = len(parts)
    for i in range(len(parts)):
        part = parts[i]
        print_same_line("Downloading data from Octopart ({:,}/{:,}, {} remaining)".format(i + 1, j,
                                                                              estimated_time_completion(i,
                                                                                                        j,
                                                                                                        avg_time=0.165)))
        result = query(client, part)
        results.append(clean_result(result, part))
    if results is None:
        # do nothing
        print("No matches found.")
    else:
        print("Download complete.")
        with open(file_out, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["Part Number", "Generic Part Number", "Category", "Description", "Datasheet Link"])
            for i in range(len(results)):
                each = results[i]
                print_same_line("Resolving links... ({:,}/{:,}, {} remaining)".format(i + 1, j,
                                                                                                  estimated_time_completion(
                                                                                                      i,
                                                                                                      j,
                                                                                                      avg_time=0.5)))
                hyperlink = ""
                if not each['url'] == "":
                    # no url
                    hyperlink = '=HYPERLINK("{}","{}")'.format(unshorten_url(each['url']), "DATASHEET LINK")
                    if len(hyperlink) > 255:
                        hyperlink = unshorten_url(each['url'])
                writer.writerow([each['mpn'], each['genericMpn'], each['category'], each['shortDescription'], hyperlink])
        print("Saved file {:,} parts to file '{}'.".format(j, file_out))
        #     ",".join([clean_text(part), '"=HYPERLINK(""{}"",""{}"")"'.format(url, hyperlink_text), '"{}"'.format(description)]))
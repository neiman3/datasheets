import os.path
from filemanip import extract_folder

def filenames(testing=False):
    # returns open file, save to file
    if testing:
        file_in = os.path.join(extract_folder(), 'test_in.csv')
        save_as = os.path.join(extract_folder(), 'test_out.csv')
    else:
        file_in = prompt_entry("Open CSV file (full path): > ")
        dir_in = prompt_entry("Save to directory (full path): > ", mode='folder')
        save_as = input("Save as (file name only): > ")
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
    if filename[0]== "\"" and filename[-1]== "\"":
        # remove quotes
        filename = filename[1:-1]
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


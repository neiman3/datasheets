import os.path

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
import os


def extract_folder():
    base_dir = os.path.dirname(__file__)
    check_dir = os.path.join(base_dir, '..')
    if os.path.exists(os.path.join(check_dir, 'filemanip.py')):
        # check_dir should be the project root folder
        return check_dir
    return base_dir

import os


def split_path(filepath):
    return os.path.dirname(filepath), os.path.basename(filepath)

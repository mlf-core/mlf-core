import os
from pathlib import Path


def delete_dir_tree(directory: Path) -> None:
    """
    Recursively delete a whole directory and its content.
    Since there is no built-in function for this in the pathlib API and we want to keep it consistent, we have to use a custom function.

    :param directory: The directory that should be removed
    """

    dir = directory

    for file in dir.iterdir():
        if file.is_dir():
            delete_dir_tree(file)
        else:
            file.unlink()
    dir.rmdir()


def pf(calling_class, file_path: str) -> str:
    """

    :param calling_class: the class of which this method is called
    :param file_path: path to file
    :return: joined path
    """
    return os.path.join(calling_class.path, file_path)


def find_filepath_in_dir(file_name: str, path: str, default: str = None) -> str:
    """
    Looks for a filepath in a directory and returns it.

    :param file_name: File to look for
    :param path: Start path to start looking for the file
    :default: The default expected file path
    :return: absolute file path of the desired file
    """
    result = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file_name in file:
                return os.path.join(root, file)

    if not result:
        return default

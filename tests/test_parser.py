import os

from gendiff.parser import generate_diff


def get_current_path(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_path)
    return file_path
    

def read_file(file_path):
    file_path = get_current_path(file_path)
    with open(file_path) as file:
        return file.read()


def test_generate_diff():
    file1_path = get_current_path("test_data/file1.json")
    file2_path = get_current_path("test_data/file2.json")
    result = read_file("test_data/result.txt")

    assert generate_diff(file1_path, file2_path) == result
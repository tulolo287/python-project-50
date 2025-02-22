import os

import pytest

from gendiff.parser import generate_diff


def get_current_path(file_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_path)
    return file_path


def read_file(file_path):
    file_path = get_current_path(file_path)
    with open(file_path) as file:
        return file.read()


@pytest.fixture
def fixture(request):
    file1 = get_current_path(request.param[0])
    file2 = get_current_path(request.param[1])
    return generate_diff(file1, file2)


testdata = [
    (
        ["test_data/file1.json", "test_data/file2.json"],
        "test_data/result.txt",
    ),
    (
        ["test_data/file1.yml", "test_data/file2.yml"],
        "test_data/result.txt",
    ),
    (
        ["test_data/nested1.json", "test_data/nested2.json"],
        "test_data/nested_result.txt",
    ),
    (
        ["test_data/nested1.yml", "test_data/nested2.yml"],
        "test_data/nested_result.txt",
    ),
]


@pytest.mark.parametrize("fixture, result", testdata, indirect=["fixture"])
def test_generate_diff(fixture, result):
    result = read_file(result)
    assert fixture == result

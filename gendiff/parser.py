import json


def parse_files(*file_paths):
    parsed_files = []
    for path in file_paths:
        parsed_files.append(json.load(open(path)))
    print(parsed_files)

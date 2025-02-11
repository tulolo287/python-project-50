import json

import yaml


def generate_diff(file_path1, file_path2):
    res = ["{"]

    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    file1_elements = set(file1)
    file2_elements = set(file2)

    minus_data = file1_elements - file2_elements
    plus_data = file2_elements - file1_elements
    common_data = file1_elements & file2_elements
    all_data = sorted(file1_elements | file2_elements)

    for key in all_data:
        if key in file1 and type(file1[key]) is bool:
            file1[key] = str(file1[key]).lower()
        if key in file2 and type(file2[key]) is bool:
            file2[key] = str(file2[key]).lower()

        if key in minus_data:
            res.append(f"- {key}: {file1[key]}")
        if key in plus_data:
            res.append(f"+ {key}: {file2[key]}")
        if key in common_data:
            if file1[key] == file2[key]:
                res.append(f"  {key}: {file1[key]}")
            else:
                res.append(f"- {key}: {file1[key]}")
                res.append(f"+ {key}: {file2[key]}")
    res = "\n  ".join(res) + "\n}"

    return res


def load_file(file_path):
    file_extension = file_path.split(".")[-1]
    if file_extension == "json":
        return json.load(open(file_path))
    if file_extension == "yml" or file_extension == "yaml":
        return yaml.load(open(file_path), Loader=yaml.Loader)

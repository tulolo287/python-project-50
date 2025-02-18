import json

import yaml

from gendiff.utils.utils import make_ast


def generate_diff(file_path1, file_path2):
    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    return formatter(file1, file2)


def load_file(file_path):
    file_extension = file_path.split(".")[-1]
    if file_extension == "json":
        return json.load(open(file_path))
    if file_extension == "yml" or file_extension == "yaml":
        return yaml.load(open(file_path), Loader=yaml.Loader)


def formatter(file1, file2, res=["{"], sp=""):
    ind = "    "
    minus_ind = "- "
    plus_ind = "+ "

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

        if key in file1 and file1[key] is None:
            file1[key] = "null"
        if key in file2 and file2[key] is None:
            file2[key] = "null"

        if key in minus_data:
            if isinstance(file1[key], dict):
                res.append(f"{sp}{minus_ind}{key}: {{")
                tmp = sp
                sp += ind
                formatter(file1[key], file1[key], res, sp)
                sp = tmp
                res.append(f"{sp}  }}")
                continue
            else:
                res.append(f"{sp}{minus_ind}{key}: {file1[key]}")
        if key in plus_data:
            if isinstance(file2[key], dict):
                res.append(f"{sp}{plus_ind}{key}: {{")
                tmp = sp
                sp += ind
                formatter(file2[key], file2[key], res, sp)
                sp = tmp
                res.append(f"{sp}  }}")
                continue
            else:
                res.append(f"{sp}{plus_ind}{key}: {file2[key]}")
        if key in common_data:
            if isinstance(file1[key], dict) and isinstance(file2[key], dict):
                res.append(f"{sp}  {key}: {{")
                tmp = sp
                sp += ind
                formatter(file1[key], file2[key], res, sp)
                sp = tmp
                res.append(f"{sp}  }}")
                continue
            if file1[key] == file2[key]:
                res.append(f"{sp}  {key}: {file1[key]}")
            else:
                if isinstance(file1[key], dict):
                    res.append(f"{sp}{minus_ind}{key}: {{")
                    tmp = sp
                    sp += ind
                    formatter(file1[key], file1[key], res, sp)
                    sp = tmp
                    res.append(f"{sp}  }}")
                    res.append(f"{sp}{plus_ind}{key}: {file2[key]}")
                elif isinstance(file2[key], dict):
                    res.append(f"{sp}{plus_ind}{key}: {{")
                    tmp = sp
                    sp += ind
                    formatter(file2[key], file2[key], res, sp)
                    sp = tmp
                    res.append(f"{sp}  }}")
                    res.append(f"{sp}{minus_ind}{key}: {file1[key]}")
                else:
                    if not file1[key]:
                        res.append(f"{sp}{minus_ind}{key}:")
                        res.append(f"{sp}{plus_ind}{key}: {file2[key]}")
                    elif not file2[key]:
                        res.append(f"{sp}{minus_ind}{key}: {file1[key]}")
                        res.append(f"{sp}{plus_ind}{key}:")
                    else:
                        res.append(f"{sp}{minus_ind}{key}: {file1[key]}")
                        res.append(f"{sp}{plus_ind}{key}: {file2[key]}")

    res = "\n  ".join(res) + "\n}\n"
    return res

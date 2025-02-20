import json

import yaml

from gendiff.utils.utils import make_ast


def generate_diff(file_path1, file_path2):
    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    ast = gen_ast(file1, file2)
    return formatter(ast)


def load_file(file_path):
    file_extension = file_path.split(".")[-1]
    if file_extension == "json":
        return json.load(open(file_path))
    if file_extension == "yml" or file_extension == "yaml":
        return yaml.load(open(file_path), Loader=yaml.Loader)


def gen_ast(file1, file2):
    ast = []

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

        if key in common_data:
            old_value = None
            action = "unchanged"
            if isinstance(file1[key], dict) and isinstance(file2[key], dict):
                node = gen_ast(file1[key], file2[key])
                node_type = "list"
            elif isinstance(file1[key], dict):
                node = gen_ast(file1[key], file1[key])
                node_type = "list"
                old_value = file2[key]
                action = "change"
            else:
                if file1[key] != file2[key]:
                    old_value = file1[key]
                    action = "change"
                node = file2[key]
                node_type = "node"
            ast.append(
                {
                    "name": key,
                    "node_type": node_type,
                    "value": node,
                    "old_value": old_value,
                    "action": action,
                }
            )

        elif key in minus_data:
            if isinstance(file1[key], dict):
                node = gen_ast(file1[key], file1[key])
                node_type = "list"
            else:
                node = file1[key]
                node_type = "node"
            ast.append(
                {
                    "name": key,
                    "node_type": node_type,
                    "value": node,
                    "action": "remove",
                }
            )
        elif key in plus_data:
            if isinstance(file2[key], dict):
                node = gen_ast(file2[key], file2[key])
                node_type = "list"
            else:
                node = file2[key]
                node_type = "node"
            ast.append(
                {
                    "name": key,
                    "node_type": node_type,
                    "value": node,
                    "action": "add",
                }
            )

    return ast


def formatter(ast, res=["{"], ind="  "):
    for item in ast:
        name = item["name"]
        action = item["action"]
        value = item["value"]
        old_value = item.get("old_value", None)
        node_type = item["node_type"]
        match action:
            case "remove":
                sign = "- "
            case "add":
                sign = "+ "
            case "unchanged":
                sign = "  "

        if node_type == "node":
            if action == "change":
                if not old_value:
                    res.append(f"{ind}- {name}:")
                else:
                    res.append(f"{ind}- {name}: {old_value}")
                res.append(f"{ind}+ {name}: {value}")
            else:
                res.append(f"{ind}{sign}{name}: {value}")
        elif node_type == "list":
            if action == "change":
                res.append(f"{ind}- {name}: {{")
                tmp = ind
                ind += "    "
                formatter(value, res, ind)
                ind = tmp
                res.append(f"{ind}  }}")
                res.append(f"{ind}+ {name}: {old_value}")
                continue
            res.append(f"{ind}{sign}{name}: {{")
            tmp = ind
            ind += "    "
            formatter(value, res, ind)
            ind = tmp
            res.append(f"{ind}  }}")
            continue

    res = "\n".join(res) + "\n}\n"
    return res

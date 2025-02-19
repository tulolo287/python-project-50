import json

import yaml

from gendiff.utils.utils import make_ast


def generate_diff(file_path1, file_path2):
    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    ast = gen_ast(file1, file2)
    print(formatter(ast))


def load_file(file_path):
    file_extension = file_path.split(".")[-1]
    if file_extension == "json":
        return json.load(open(file_path))
    if file_extension == "yml" or file_extension == "yaml":
        return yaml.load(open(file_path), Loader=yaml.Loader)


def gen_ast(file1, file2, ast=[]):
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

        if (
            key in file1
            and isinstance(file1[key], dict)
            and key in file2
            and isinstance(file2[key], dict)
        ):
            node = gen_ast(file1[key], file2[key])
            ast.append(
                {
                    "name": key,
                    "node_type": "list",
                    "value": node,
                    "action": "unchanged",
                }
            )

        elif key in common_data:
            ast.append(
                {
                    "name": key,
                    "node_type": "node",
                    "value": file1[key],
                    "action": "unchanged",
                }
            )

        elif key in minus_data:
            if isinstance(file1[key], dict):
                gen_ast(file1[key], file1[key])
            else:
                ast.append(
                    {
                        "name": key,
                        "node_type": "node",
                        "value": file1[key],
                        "action": "remove",
                    }
                )
        elif key in plus_data:
            if isinstance(file2[key], dict):
                gen_ast(file2[key], file2[key])
            else:
                ast.append(
                    {
                        "name": key,
                        "node_type": "node",
                        "value": file2[key],
                        "action": "add",
                    }
                )

    return ast


def formatter(ast, res=[]):
    for item in ast:
        name = item["name"]
        action = item["action"]
        value = item["value"]
        node_type = item["node_type"]
        match action:
            case "remove":
                sign = "- "
            case "add":
                sign = "+ "
            case "unchanged":
                sign = "  "

        if node_type == "node":
            res.append(f"{sign}{name}: {value}")
        else:
            formatter(ast)
        print(name)
    "\n".join(res)
    return res

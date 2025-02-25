import json

import yaml

from gendiff.formatters import format_plain, format_stylish


def generate_diff(file_path1, file_path2, format_name="stylish"):
    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    ast = generate_ast(file1, file2)
    if format_name == "stylish":
        return format_stylish(ast)
    elif format_name == "plain":
        return format_plain(ast)


def load_file(file_path):
    file_extension = file_path.split(".")[-1]
    if file_extension == "json":
        return json.load(open(file_path))
    if file_extension == "yml" or file_extension == "yaml":
        return yaml.load(open(file_path), Loader=yaml.Loader)


def generate_ast(file1, file2):
    ast = []

    file1_elements = set(file1)
    file2_elements = set(file2)

    minus_data = file1_elements - file2_elements
    plus_data = file2_elements - file1_elements
    common_data = file1_elements & file2_elements
    all_data = sorted(file1_elements | file2_elements)

    for key in all_data:
        if key in common_data:
            old_value = file1[key]
            node = file2[key]
            node_type = "node"
            action = "unchanged"
            if isinstance(file1[key], dict) and isinstance(file2[key], dict):
                node = generate_ast(file1[key], file2[key])
                node_type = "list"
            elif isinstance(file1[key], dict):
                node = generate_ast(file1[key], file1[key])
                old_value = node
                node = file2[key]
                node_type = "list"
                action = "change"
            elif file1[key] != file2[key]:
                old_value = file1[key]
                node = file2[key]
                node_type = "node"
                action = "change"
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
                node = generate_ast(file1[key], file1[key])
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
                node = generate_ast(file2[key], file2[key])
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

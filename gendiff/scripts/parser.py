import json

import yaml

from gendiff.formatters import format_json, format_plain, format_stylish


def generate_diff(file_path1, file_path2, format_name="stylish"):
    file1 = load_file(file_path1)
    file2 = load_file(file_path2)

    ast = generate_ast(file1, file2)

    if format_name == "stylish":
        return format_stylish(ast)
    elif format_name == "plain":
        return format_plain(ast)
    elif format_name == "json":
        return format_json(ast)


def load_file(file_path):
    file_extension = file_path.split(".")[-1]
    if file_extension == "json":
        return json.load(open(file_path))
    if file_extension == "yml" or file_extension == "yaml":
        return yaml.load(open(file_path), Loader=yaml.Loader)


def get_data(file1, file2):
    file1_elements = set(file1)
    file2_elements = set(file2)

    minus_data = file1_elements - file2_elements
    plus_data = file2_elements - file1_elements
    common_data = file1_elements & file2_elements
    all_data = sorted(file1_elements | file2_elements)

    return minus_data, plus_data, common_data, all_data


def get_common_node(value1, value2):
    old_value = value1
    node = value2
    node_type = "node"
    action = "unchanged"
    if isinstance(value1, dict) and isinstance(value2, dict):
        node = generate_ast(value1, value2)
        node_type = "list"
    elif isinstance(value1, dict):
        node = generate_ast(value1, value1)
        old_value = node
        node = value2
        node_type = "list"
        action = "change"
    elif isinstance(value2, dict):
        node = generate_ast(value2, value2)
        old_value = value1
        node_type = "list"
        action = "change"
    elif value1 != value2:
        old_value = value1
        node = value2
        node_type = "node"
        action = "change"
    return node, node_type, old_value, action


def get_node(value, action):
    old_value = None
    if isinstance(value, dict):
        node = generate_ast(value, value)
        node_type = "list"
    else:
        node = value
        node_type = "node"
    return node, node_type, old_value, action


def generate_ast(file1, file2):
    ast = []
    minus_data, plus_data, common_data, all_data = get_data(file1, file2)

    for key in all_data:
        old_value = None
        node = None
        node_type = "node"
        action = "unchanged"
        if key in common_data:
            node, node_type, old_value, action = get_common_node(
                file1[key], file2[key]
            )
        elif key in minus_data:
            node, node_type, old_value, action = get_node(file1[key], "remove")
        elif key in plus_data:
            node, node_type, old_value, action = get_node(file2[key], "add")
        ast.append(
            {
                "name": key,
                "node_type": node_type,
                "value": node,
                "old_value": old_value,
                "action": action,
            }
        )
    return ast

def format_plain(ast):
    res = process_ast(ast)
    return res


def process_ast(ast, prev=""):
    res = []
    for node in ast:
        line = format_line(node, prev)
        if line is not None:
            res.append(line)
    return "\n".join(res)


def format_value(value):
    result = ""
    if isinstance(value, dict | list):
        result = "[complex value]"
    elif isinstance(value, str):
        result = f"'{value}'"
    elif value is None:
        result = "null"
    elif isinstance(value, bool):
        result = str(value).lower()
    else:
        result = value
    return result


def format_line(item, prev=""):
    name = item["name"]
    node_type = item["node_type"]
    value = format_value(item["value"])
    action = item["action"]
    old_value = format_value(item.get("old_value", None))
    value_path = f"{prev}{name}"

    if action == "remove":
        return f"Property '{value_path}' was removed"
    elif action == "add":
        return f"Property '{value_path}' was added with value: {value}"
    elif action == "change":
        return (
            f"Property '{value_path}' was updated. From {old_value} to {value}"
        )

    if node_type == "list":
        list_nodes = item["value"]
        return process_ast(list_nodes, f"{value_path}.")
    return None

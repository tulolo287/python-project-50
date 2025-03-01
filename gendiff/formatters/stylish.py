def format_stylish(ast):
    res = process_ast(ast)
    res = "{\n" + res + "\n}"
    return res


def process_ast(ast, lines=[], ind="  "):
    lines = []
    for item in ast:
        lines = format_ast(item, lines, ind)
    output = "\n".join(lines)
    return output


def format_value(value):
    result = ""
    if isinstance(value, bool):
        result = str(value).lower()
    elif value is None:
        result = "null"
    else:
        result = value
    return result


def format_action_change_node(res, item, ind):
    name = item["name"]
    value = format_value(item["value"])
    old_value = format_value(item.get("old_value", None))
    if not old_value and old_value != 0:
        res.append(f"{ind}- {name}: ")
    else:
        res.append(f"{ind}- {name}: {old_value}")
    if not value and value != 0:
        res.append(f"{ind}+ {name}: ")
    else:
        res.append(f"{ind}+ {name}: {value}")


def format_action_change_list(res, item, ind):
    name = item["name"]
    value = format_value(item["value"])
    old_value = format_value(item.get("old_value", None))
    if isinstance(value, list):
        res.append(f"{ind}- {name}: {old_value}")
        format_list_item(res, item, value, ind, '+ ')
    elif isinstance(old_value, list):
        format_list_item(res, item, old_value, ind, '- ')
        res.append(f"{ind}+ {name}: {value}")


def format_list_item(res, item, value, ind, sign):
    name = item["name"]
    res.append(f"{ind}{sign}{name}: {{")
    tmp = ind
    ind += "    "
    child_nodes = process_ast(value, res, ind)
    res.append(child_nodes)
    ind = tmp
    res.append(f"{ind}  }}")


def format_list(res, item, ind, sign):
    value = format_value(item["value"])
    action = item["action"]
    if action == "change":
        format_action_change_list(res, item, ind)
    else:
        format_list_item(res, item, value, ind, sign)


def format_node(res, item, ind, sign):
    name = item["name"]
    action = item["action"]
    value = format_value(item["value"])
    if action == "change":
        format_action_change_node(res, item, ind)
    else:
        res.append(f"{ind}{sign}{name}: {value}")


def format_ast(item, res, ind):
    action = item["action"]
    node_type = item["node_type"]
    if action == "remove":
        sign = "- "
    elif action == "add":
        sign = "+ "
    else:
        sign = "  "
    if node_type == "node":
        format_node(res, item, ind, sign)
    elif node_type == "list":
        format_list(res, item, ind, sign)
    return res

def format_stylish(ast):
    res = process_ast(ast)
    res = "{\n" + res + "\n}\n"
    return res


def process_ast(ast, lines=[], ind="  "):
    lines = []
    for item in ast:
        lines = format_node(item, lines, ind)
    output = "\n".join(lines)
    return output


def format_node(item, res, ind):
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
            child_nodes = process_ast(value, res, ind)
            res.append(child_nodes)

            ind = tmp
            res.append(f"{ind}  }}")
            res.append(f"{ind}+ {name}: {old_value}")
        else:
            res.append(f"{ind}{sign}{name}: {{")
            tmp = ind
            ind += "    "
            child_nodes = process_ast(value, res, ind)
            res.append(child_nodes)
            ind = tmp
            res.append(f"{ind}  }}")
    return res

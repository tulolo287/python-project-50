import json


def format_json(ast):
    res = json.dumps(ast, indent=4)
    return res

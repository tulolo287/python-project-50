def make_ast(data, ast=[], indent=" "):
    for i, (key, val) in enumerate(data.items()):
        if isinstance(val, dict):
            ast.append({"name": key, "type": "nodeList", "value": [], "indent": indent})
            if isinstance(ast[i]["value"], dict):
                make_ast(val, ast[i]["value"], indent)
            else:
                make_ast(val, ast[len(ast) - 1]["value"], indent)
        else:
            ast.append({"name": key, "type": "node", "value": val, "indent": indent})
    return ast

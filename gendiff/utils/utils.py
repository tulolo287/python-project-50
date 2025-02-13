def make_ast(data, ast=[]):
    for i, (key, val) in enumerate(data.items()):
        if isinstance(val, dict):
            ast.append({
                "name": key,
                "type": "nodeList",
                "value": []
            })
            make_ast(val, ast[i]["value"])
        else:
            ast.append({
                "name": key,
                "type": "node",
                "value": val
            })
    return ast
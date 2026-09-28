import json
def read_json(path):
    with open(path,encoding="utf-8") as fh: value=json.load(fh)
    if isinstance(value,dict): value=value.get("findings",value.get("rows",value))
    if not isinstance(value,list) or not all(isinstance(x,dict) for x in value): raise ValueError("JSON must contain a list of finding objects, or a findings/rows list.")
    return [{str(k):"" if v is None else str(v) for k,v in row.items()} for row in value]

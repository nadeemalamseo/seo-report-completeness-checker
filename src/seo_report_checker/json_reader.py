import json


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"JSON contains duplicate object key: {key}")
        result[key] = value
    return result


def _field_value(value, row_number, key):
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return str(value)
    raise ValueError(
        f"JSON finding row {row_number}, field {key!r} must be a scalar value, not an object or array."
    )


def read_json(path):
    with open(path, encoding="utf-8") as fh:
        value = json.load(fh, object_pairs_hook=_reject_duplicate_keys)

    if isinstance(value, dict):
        if "findings" in value:
            value = value["findings"]
        elif "rows" in value:
            value = value["rows"]
        else:
            raise ValueError("JSON object must contain a 'findings' or 'rows' array.")
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise ValueError("JSON must contain a list of finding objects, or a findings/rows list.")
    if not value:
        raise ValueError("JSON contains no findings; an empty report cannot pass validation.")

    return [
        {str(key): _field_value(item, index, key) for key, item in row.items()}
        for index, row in enumerate(value, start=1)
    ]

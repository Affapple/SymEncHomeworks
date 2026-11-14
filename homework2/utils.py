import json


def read_data(filepath):
    with open(filepath, "r") as f:
        data = f.read()
    return json.loads(data)

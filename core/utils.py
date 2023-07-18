import json


def load_json(path):
    with open(path) as fh:
        return json.load(fh)

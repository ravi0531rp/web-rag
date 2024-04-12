import json

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def write_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)
import json

def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def write_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)

def json_to_text(json_path):
    json_data = load_json(json_path)
    texts = []
    for _, value in json_data.items():
        texts.extend(value)
    texts = " ; ".join(texts)
    return texts

def dict_to_text(data):
    texts = []
    for _, value in data.items():
        texts.extend(value)
    texts = " ; ".join(texts)
    return texts
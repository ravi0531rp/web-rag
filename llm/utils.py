import json
import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

def add_punctuation(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Initialize an empty list to store the tokens
    tokens = []

    # Iterate through each token in the processed text
    for token in doc:
        # Append the token's text to the list
        tokens.append(token.text)

        # Check if the token is a punctuation mark
        if token.text in [".", "!", "?"]:
            # Add a space after the punctuation mark
            tokens.append(" ")

    # Concatenate the tokens to form the modified text
    modified_text = "".join(tokens)

    return modified_text


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
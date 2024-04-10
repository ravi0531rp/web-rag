import json
import requests
from bs4 import BeautifulSoup
from loguru import logger

def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    
def write_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)
    
def get_all_links(data_dict):
    all_links = []
    for key, value in data_dict.items():
        all_links.extend(value)
        all_links.append(key)
    return list(set(all_links))

def extract_text_from_page(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text contents from the HTML
            text_blocks = []
            for element in soup.find_all(['p', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li']):
                text = element.get_text(separator=' ', strip=True)
                if text:
                    text_blocks.append(text)
            
            return text_blocks
        else:
            print(f"Failed to fetch the webpage {url}. Status code:", response.status_code)
            return []
    except Exception as e:
        print(f"Error occurred while processing the webpage {url}: {e}")
        return []

if __name__ == '__main__':
    data_dict = read_json("./urls/visited_links.json")
    all_links = get_all_links(data_dict)

    extracted_data_dict = {}
    for link in all_links:
        extracted_data_dict[link] = extract_text_from_page(link)
    
    write_json(extracted_data_dict, "./datasets/extracted_data.json")

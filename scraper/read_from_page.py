import requests
from bs4 import BeautifulSoup
from loguru import logger

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
    url = "https://ravi0531rp.github.io/web-rag/services/ai_models.html"
    text_blocks = extract_text_from_page(url)
    for item in text_blocks:
        logger.success(item)
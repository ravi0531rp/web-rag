import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from loguru import logger


def get_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <a> tags (links) in the HTML
        links = soup.find_all('a')
        
        # Extract the href attribute from each <a> tag and prepend the base URL
        base_url = url
        link_list = [urljoin(base_url, link.get('href')) for link in links]
        
        return link_list
    else:
        print("Failed to fetch the webpage. Status code:", response.status_code)
        return []

# Main function
if __name__ == "__main__":
    url = "https://ravi0531rp.github.io/web-rag/index.html"
    links = get_links(url)
    
    if links:
        logger.info("Links found on the webpage:")
        for link in links:
            logger.success(link)
    else:
        logger.info("No links found on the webpage.")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from loguru import logger
import re
from collections import deque
import json

def write_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile, indent = 4)

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
        logger.error("Failed to fetch the webpage. Status code:", response.status_code)
        return []

def is_github_io_link(url):
    return re.match(r'^https?://.*\.github\.io/.*', url) is not None

def crawl_page(homepage_url):
    visited_links = {}
    queue = deque([homepage_url])
    
    while queue:
        current_url = queue.popleft()
        
        if current_url in visited_links:
            continue
        
        logger.info(f"Visiting webpage: {current_url}")
        
        links_on_page = get_links(current_url)
        logger.info(f"Links found on the webpage {current_url}: {links_on_page}")
        
        visited_links[current_url] = links_on_page
        
        if links_on_page:
            for link in links_on_page:
                logger.success(link)
                if is_github_io_link(link) and link not in visited_links:
                    queue.append(link)
        else:
            logger.info(f"No links found on the webpage {current_url}.")
    
    return visited_links


# Main function
if __name__ == "__main__":
    homepage_url = "https://ravi0531rp.github.io/web-rag/index.html"
    visited_links = crawl_page(homepage_url)
    logger.info(visited_links)
    write_json(visited_links, "./urls/visited_links.json")

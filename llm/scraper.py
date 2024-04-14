import os
import re
from collections import deque
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from loguru import logger
from utils import load_json, write_json

def is_github_io_link(url):
    return re.match(r"^https?://.*\.github\.io/.*", url) is not None

def get_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        base_url = url
        link_list = [urljoin(base_url, link.get("href")) for link in links]
        final_list = []
        for ll in link_list:
            if is_github_io_link(ll):
                final_list.append(ll)
        return final_list
    else:
        logger.error("Failed to fetch the webpage. Status code:", response.status_code)
        return []



def crawl_page(homepage_url, scrape_depth=1):
    visited_links = {}
    queue = deque([(homepage_url, 0)])  # Each item in the queue is a tuple: (url, depth)

    while queue:
        current_url, current_depth = queue.popleft()

        if current_url in visited_links:
            continue

        if current_depth > scrape_depth:
            break


        links_on_page = get_links(current_url)
        logger.info(f"Links found on the webpage {current_url}: {links_on_page}")

        visited_links[current_url] = links_on_page

        if links_on_page:
            for link in links_on_page:
                if is_github_io_link(link) and link not in visited_links:
                    queue.append((link, current_depth + 1))

        else:
            logger.info(f"No links found on the webpage {current_url}.")

    return visited_links



def get_all_links(data_dict):
    all_links = []
    for key, value in data_dict.items():
        all_links.extend(value)
        all_links.append(key)
    return list(set(all_links))


def extract_text_from_page(url):
    try:
        response = requests.get(url)
        content_type = response.headers.get('content-type', '').lower()

        if 'html' in content_type:
            # Parse HTML content
            soup = BeautifulSoup(response.text, "html.parser")
            text_blocks = []
            for element in soup.find_all(
                ["p", "table", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li"]
            ):
                text = element.get_text(separator=" ", strip=True)
                if text:
                    text_blocks.append(text)
            return text_blocks

        elif 'xml' in content_type:
            # Parse XML content
            soup = BeautifulSoup(response.text, "xml")
            text_blocks = []
            for element in soup.find_all():
                text = element.get_text(separator=" ", strip=True)
                if text:
                    text_blocks.append(text)
            return text_blocks

        else:
            logger.error(
                f"Unsupported content type for the webpage {url}: {content_type}"
            )
            return []

    except Exception as e:
        logger.error(f"Error occurred while processing the webpage {url}: {e}")
        return []



def run_complete(
    homepage_url,
    project_name,
    scrape_fresh=True,
    read_fresh=True,
    scrape_depth=None,
):
    visited_links = None
    if scrape_fresh:
        visited_links = crawl_page(homepage_url, scrape_depth)
        os.makedirs(f"./assets/{project_name}/urls/", exist_ok=True)
        write_json(visited_links, f"./assets/{project_name}/urls/visited_links.json")
    else:
        visited_links = load_json(f"./assets/{project_name}/urls/visited_links.json")

    all_links = get_all_links(visited_links)

    extracted_data_dict = {}
    if read_fresh:
        for link in all_links:
            extracted_data_dict[link] = extract_text_from_page(link)
        os.makedirs(f"./assets/{project_name}/datasets/", exist_ok=True)
        write_json(
            extracted_data_dict, f"./assets/{project_name}/datasets/extracted_data.json"
        )
    else:
        extracted_data_dict = load_json(
            f"./assets/{project_name}/datasets/extracted_data.json"
        )

    logger.debug(extracted_data_dict)

    return extracted_data_dict


if __name__ == "__main__":
    homepage_url = "https://colah.github.io/posts/2015-08-Understanding-LSTMs/"
    extracted_data_dict = run_complete(
        homepage_url,
        "WEB_RAG_DEMO",
        scrape_fresh=True,
        read_fresh=True,
        scrape_depth=1,
    )



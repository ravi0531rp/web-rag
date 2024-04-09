import urllib.robotparser
from urllib.parse import urljoin, urlparse

def get_all_links(base_url, path):
  """Recursively crawls a website and extracts all internal links.

  Args:
    base_url: The base URL of the website (e.g., "file:///home/ravi0531rp/Desktop/CODES/p-projects/web-rag/website/services/").
    path: The path of the current page relative to the base URL.

  Returns:
    A list of all internal links found on the website.
  """
  # Combine base URL and path to get the full URL of the current page.
  url = urljoin(base_url, path)

  # Create a RobotParser object to check for crawl restrictions.
  robots = urllib.robotparser.RobotFileParser()
  robots.set_url(urljoin(base_url, "robots.txt"))
  robots.read()

  # Check if crawling is allowed according to robots.txt.
  if not robots.can_fetch("*", url):
    return []

  # Open the current page and extract links.
  try:
    with urllib.request.urlopen(url) as response:
      html = response.read().decode()
  except urllib.error.URLError:
    # Handle potential errors gracefully, e.g., page not found.
    return []

  # Parse the HTML content to find links.
  links = []
  base_url_parsed = urlparse(base_url)
  for link in html.split('href="'):
    if link.startswith('"'):
      link = link[1:].split('"')[0]
      # Check if the link is internal (relative to the base URL).
      if not link.startswith("http") and not link.startswith("#"):
        # Handle relative paths by joining with base URL.
        link = urljoin(url, link)
        # Parse the joined URL.
        parsed_link = urlparse(link)
        # Check if the scheme and netloc (domain) match the base URL.
        if parsed_link.scheme == base_url_parsed.scheme and parsed_link.netloc == base_url_parsed.netloc:
          # Extract the path portion of the internal link.
          links.append(parsed_link.path)
      else:
        # Handle absolute links or links to external websites.
        links.append(link)

  # Recursively crawl linked pages.
  for linked_path in links:
    links.extend(get_all_links(base_url, linked_path))

  return links

# Example usage:
base_url = "file:///home/ravi0531rp/Desktop/CODES/p-projects/web-rag/website/"
internal_links = get_all_links(base_url, "ai_models.html")

print("Internal links found:")
for link in internal_links:
  print(link)

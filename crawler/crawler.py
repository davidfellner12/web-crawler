import requests
import urllib.robotparser
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for tag in soup.find_all('a', href=True):
            href = tag['href']
            full_url = urljoin(base_url. href)
            links.add(full_url)
    return links

def is_allowed(url, user_agent="MyCrawler"):
    parsed_url = requests.utils.urlparse(url)
    base = f"{parsed_url.scheme}://{parsed_url.netloc}"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{base}/robots.txt")
    rp.read()
    return rp.can_fetch(user_agent, url)


url ="https://example.com"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
print("Page title:", soup.title.text)
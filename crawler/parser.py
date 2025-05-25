from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_links(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        link = urljoin(base_url,a['href'])
        links.add(link)
    return links
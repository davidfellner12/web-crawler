from crawler.fetcher import fetch_page
from crawler.parser import extract_links
from crawler.robots import is_allowed
from crawler.storage import save_page
from urllib.parse import urlparse
import time

visited = set()
domain = "example.com"

def crawl(url):
    if url in visited or not is_allowed(url):
        return
    visited.add(url)
    print(f"Crawling: {url}")

    html = fetch_page(url)
    if html:
        save_page(url, html)
        for link in extract_links(url,html):
            if domain in urlparse(link).netloc:
                time.sleep(1)
                crawl(link)

if __name__ == "__main__":
    seed = "https://example.com"
    domain = urlparse(seed).netloc
    crawl(seed)

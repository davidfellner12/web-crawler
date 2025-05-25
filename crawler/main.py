from crawler.fetcher import fetch_page
from crawler.parser import extract_links, extract_metadata
from crawler.robots import is_allowed
from crawler.storage import save_page, save_metadata
from urllib.parse import urlparse
from collections import deque
import time

visited = set()
domain = "example.com"


def crawl(url):
    queue = deque([url])

    while queue:
        url = queue.popleft()
        if url in visited or not is_allowed(url):
            continue
        visited.add(url)
        print(f"Crawling: {url}")

        try:
            html = fetch_page(url)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue
        if html:
            save_page(url, html)
            metadata = extract_metadata(html,url)
            save_metadata(url, metadata)

            for link in extract_links(url, html):
                if domain in urlparse(link).netloc and link not in visited:
                    queue.append(link)
            time.sleep(1)


if __name__ == "__main__":
    seed = "https://example.com"
    domain = urlparse(seed).netloc
    crawl(seed)

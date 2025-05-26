import redis
from crawler.fetcher import fetch_page
from crawler.parser import extract_links, extract_metadata
from crawler.robots import is_allowed
from crawler.storage import save_page, save_metadata
from urllib.parse import urlparse
from collections import deque
import time

domain = "example.com"
r = redis.Redis(host='localhost', port=6379, db=0)
QUEUE_KEY = "url_queue"
VISITED_KEY = "visited_urls"


def enque_url(url):
    if not r.sismember(VISITED_KEY, url):
        r.lpush(QUEUE_KEY, url)


def deque_url():
    _, url = r.brpop(QUEUE_KEY)
    return url.decode('utf-8')


def crawl_worker():
    while True:
        url = deque_url()

        if r.sismember(VISITED_KEY, url):
            continue

        if not is_allowed(url):
            print(f"Disallowed by robots.txt: {url}")
            continue

        print(f"Crawling: {url}")
        try:
            html = fetch_page(url)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue
        if html:
            save_page(url, html)
            metadata = extract_metadata(html, url)
            save_metadata(url, metadata)

            r.sadd(VISITED_KEY, url)

            for link in extract_links(url, html):
                if domain in urlparse(link).netloc and not r.sismember(VISITED_KEY, link):
                    enque_url(link)
            time.sleep(1)


if __name__ == "__main__":
    seed_url = "https://example.com"
    domain = urlparse(seed_url).netloc
    enque_url(seed_url)
    crawl_worker()

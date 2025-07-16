import os
import redis
import time
from urllib.parse import urlparse

from .fetcher import fetch_page
from .parser import extract_links, extract_metadata
from .robots import is_allowed
from .storage import save_page_to_db


class CrawlerWorker:
    redis_host = os.environ.get("REDIS_HOST", "localhost")

    def __init__(self, domain, redis_host=None, redis_port=6379):
        self.domain = domain
        redis_host = redis_host or os.environ.get("REDIS_HOST", "localhost")
        self.r = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.queue_key = "url_queue"
        self.visited_key = "visited_urls"
        print(f"CrawlerWorker initialized with queue_key={self.queue_key} and visited_key={self.visited_key}")

        # Test Redis connection
        try:
            self.r.ping()
            print("[REDIS] Connected successfully.")
        except redis.exceptions.ConnectionError as e:
            print(f"[REDIS] Connection error: {e}")
            raise

    def enque_url(self, url):
        if not self.r.sismember(self.visited_key, url):
            print(f"[QUEUE] Pushing URL to queue: {url}")
            self.r.lpush(self.queue_key, url)

    def deque_url(self, timeout=10):
        item = self.r.brpop(self.queue_key, timeout=timeout)
        if item is None:
            return None
        _, url = item
        url = url.decode('utf-8')
        print(f"[QUEUE] Popped URL from queue: {url}")
        return url

    def crawl(self, max_pages=100):
        crawled_count = 0
        while crawled_count < max_pages:
            url = self.deque_url()

            if self.r.sismember(self.visited_key, url):
                print(f"[CRAWL] URL already visited: {url}")
                continue

            if not is_allowed(url):
                print(f"[CRAWL] Disallowed by robots.txt: {url}")
                continue

            print(f"[CRAWL] Crawling URL: {url}")
            try:
                html = fetch_page(url)
            except Exception as e:
                print(f"[CRAWL] Failed to fetch {url}: {e}")
                continue

            if html:
                metadata = extract_metadata(html, url)
                save_page_to_db(url, html, metadata)

                self.r.sadd(self.visited_key, url)
                print(f"[CRAWL] Saved and marked visited: {url}")
                crawled_count += 1

                for link in extract_links(url, html):
                    if self.domain in urlparse(link).netloc and not self.r.sismember(self.visited_key, link):
                        self.enque_url(link)

                time.sleep(1)

        print(f"[CRAWL] Finished crawling. Total pages crawled: {crawled_count}")

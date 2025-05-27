import os

import redis
import time
from urllib.parse import urlparse

from crawler.fetcher import fetch_page
from crawler.parser import extract_links, extract_metadata
from crawler.robots import is_allowed
from crawler.storage import save_page, save_metadata


class CrawlerWorker:
    redis_host = os.environ.get("REDIS_HOST", "localhost")

    def __init__(self, domain, redis_host='localhost', redis_port=6379):
        self.domain = domain
        if redis_host is None:
            redis_host = self.redis_host
        self.r = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.queue_key = "url_queue"
        self.visited_key = "visited_urls"
        print(f"CrawlerWorker initialized with queue_key={self.queue_key} and visited_key={self.visited_key}")

    def enque_url(self, url):
        if not self.r.sismember(self.visited_key, url):
            self.r.lpush(self.queue_key, url)

    def deque_url(self):
        _, url = self.r.brpop(self.queue_key)
        return url.decode('utf-8')

    def crawl(self):
        while True:
            url = self.deque_url()

            if self.r.sismember(self.visited_key, url):
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

                self.r.sadd(self.visited_key, url)

                for link in extract_links(url, html):
                    if self.domain in urlparse(link).netloc and not self.r.sismember(self.visited_key, link):
                        self.enque_url(link)

                time.sleep(1)

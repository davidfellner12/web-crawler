import argparse

import redis
from crawler.fetcher import fetch_page
from crawler.parser import extract_links, extract_metadata
from crawler.robots import is_allowed
from crawler.storage import save_page, save_metadata
from urllib.parse import urlparse
from collections import deque
import time

from crawler.worker import CrawlerWorker


def main():
    parser = argparse.ArgumentParser(description="Simple Web Crawler")
    parser.add_argument("seed_url", help="Seed URL to start crawling from")
    args = parser.parse_args()

    seed_url = args.seed_url
    domain = urlparse(seed_url).netloc

    worker = CrawlerWorker(domain)
    worker.enque_url(seed_url)
    worker.crawl()

if __name__ == "__main__":
    main()
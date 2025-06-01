import argparse
import os
from urllib.parse import urlparse

from crawler.worker import CrawlerWorker


def main():
    parser = argparse.ArgumentParser(description="Simple Web Crawler")
    parser.add_argument("seed_url", help="Seed URL to start crawling from")
    args = parser.parse_args()

    seed_url = args.seed_url
    domain = urlparse(seed_url).netloc

    redis_host = os.environ.get("REDIS_HOST", "localhost")
    print(f"[INIT] Seed URL: {seed_url}")
    print(f"[INIT] Domain: {domain}")
    print(f"[INIT] Connecting to Redis at host: {redis_host}")

    worker = CrawlerWorker(domain, redis_host=redis_host)

    print(f"[QUEUE] Enqueuing seed URL: {seed_url}")
    worker.enque_url(seed_url)

    print("[CRAWLER] Starting crawl loop...")
    worker.crawl()


if __name__ == "__main__":
    main()

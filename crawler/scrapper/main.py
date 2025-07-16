import argparse
import os
from urllib.parse import urlparse

from .worker import CrawlerWorker
from ..db.db import init_db


def main():
    parser = argparse.ArgumentParser(description="Simple Web Crawler")
    parser.add_argument("seed_url", help="Seed URL to start crawling from")
    parser.add_argument("--max-pages", type=int, default=100, help="Maximum number of pages to crawl")
    parser.add_argument(
        "--reset-redis",
        action="store_true",
        help="Clear Redis queue and visited URLs before starting crawl"
    )
    args = parser.parse_args()

    seed_url = args.seed_url
    max_pages = args.max_pages
    reset_redis = args.reset_redis
    domain = urlparse(seed_url).netloc

    redis_host = os.environ.get("REDIS_HOST", "localhost")
    print(f"[INIT] Seed URL: {seed_url}")
    print(f"[INIT] Domain: {domain}")
    print(f"[INIT] Connecting to Redis at host: {redis_host}")

    init_db()

    worker = CrawlerWorker(domain, redis_host=redis_host)

    if reset_redis:
        print("[REDIS] Clearing existing queue and visited URLs...")
        worker.r.delete(worker.queue_key)
        worker.r.delete(worker.visited_key)

    print(f"[QUEUE] Enqueuing seed URL: {seed_url}")
    worker.enque_url(seed_url)

    print(f"[CRAWLER] Starting crawl loop (max_pages={max_pages})...")
    worker.crawl(max_pages=max_pages)

if __name__ == "__main__":
    main()

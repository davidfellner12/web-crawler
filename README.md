🕷️ Python Web Crawler
A simple and extensible Python web crawler that:
Scrapped content will be used for rag refinement later on.

✅ Recursively crawls pages within a single domain

✅ Respects robots.txt

✅ Follows a polite crawling policy (1 second delay)

✅ Uses Redis to manage a distributed URL queue and visited set

✅ Extracts and stores page content and metadata

🚀 Quickstart
1. 📦 Clone the Repository
git clone https://github.com/davidfellner12/web-crawler.git
cd MY_ACTUAL_CRAWLER
cd crawler

3. 🧠 Run Redis (Required)
This crawler uses Redis for managing its queue and state. Make sure Redis is running locally.

Option A: Run Redis using Docker (Recommended)
docker run -d -p 6379:6379 --name redis redis

Option B: Install Redis manually
Follow instructions at: https://redis.io/docs/getting-started/installation/

3. 🕸️ Start the Crawler
You can now start crawling by running:
python main.py https://example.com

🔧 Features
Domain-Restricted Crawling: Only follows links within the start domain.

### ⚠️ Important: Reset Redis Queue for Fresh Crawls

If you're scraping a **new website** or adding **new features**,  
**make sure to clear the Redis queue and visited URLs** to avoid re-processing old data.

Run the crawler with the `--reset-redis` flag to clear Redis before starting:

```bash
python main.py https://example.com --reset-redis

Robots.txt Compliance: Automatically parses and respects disallowed paths.

Polite Crawling: Adds delay between requests to avoid server overload.

Redis Queue: Manages crawl jobs, supports distributed or multi-worker setups.

Metadata Extraction: Captures <title>, meta tags, and more.

Content Archiving: Saves raw HTML and structured metadata.

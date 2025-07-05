🕷️ Python Web Crawler
A simple and extensible Python web crawler that:

✅ Recursively crawls pages within a single domain

✅ Respects robots.txt

✅ Follows a polite crawling policy (1 second delay)

✅ Uses Redis to manage a distributed URL queue and visited set

✅ Extracts and stores page content and metadata

🚀 Quickstart
1. 📦 Clone the Repository
bash
Kopieren
Bearbeiten
git clone https://github.com/davidfellner12/web-crawler.git
cd web-crawler
2. 🧠 Run Redis (Required)
This crawler uses Redis for managing its queue and state. Make sure Redis is running locally.

Option A: Run Redis using Docker (Recommended)
bash
Kopieren
Bearbeiten
docker run -d -p 6379:6379 --name redis redis
Option B: Install Redis manually
Follow instructions at: https://redis.io/docs/getting-started/installation/

3. 🕸️ Start the Crawler
You can now start crawling by running:

bash
Kopieren
Bearbeiten
python crawler.py --start-url https://example.com
Additional flags:

--max-pages: Limit the number of pages to crawl (default: unlimited)

--output: Save crawled content to a folder or file

--delay: Set crawl delay in seconds (default: 1)

🔧 Features
Domain-Restricted Crawling: Only follows links within the start domain.

Robots.txt Compliance: Automatically parses and respects disallowed paths.

Polite Crawling: Adds delay between requests to avoid server overload.

Redis Queue: Manages crawl jobs, supports distributed or multi-worker setups.

Metadata Extraction: Captures <title>, meta tags, and more.

Content Archiving: Saves raw HTML and structured metadata.

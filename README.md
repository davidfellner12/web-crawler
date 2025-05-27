# 🕷️ Python Web Crawler

A simple Python web crawler that recursively crawls pages within a single domain, respects `robots.txt`, extracts links and metadata, and saves page content.

## ✨ Features

- ✅ Domain-restricted recursive crawling
- ✅ `robots.txt` compliance
- ✅ Polite crawling (1s delay between requests)
- ✅ Redis-based URL queue and visited set
- ✅ Page content and metadata storage

---

## 🚀 Quickstart (with Docker)

You need **Docker** and **Docker Compose** installed.

1. **Clone the repository**:

```bash
git clone https://github.com/davidfellner12/web-crawler.git
cd my-crawler

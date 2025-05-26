import json
from datetime import datetime, timezone
from json import JSONEncoder

from bs4 import BeautifulSoup
from urllib.parse import urljoin

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def extract_links(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        link = urljoin(base_url,a['href'])
        links.add(link)
    return links

def extract_metadata(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    data = {
        "url": url,
        "title": title,
        "timestamp": datetime.now(timezone.utc),
        "status": "success"
    }
    return json.dumps(data, cls=DateTimeEncoder, indent=2)



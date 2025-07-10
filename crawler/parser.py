from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone

def extract_links(base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        link = urljoin(base_url, a['href'])
        links.add(link)
    return links

def extract_metadata(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        description = desc_tag["content"].strip()
    else:
        p = soup.find("p")
        if p:
            description = p.get_text(strip=True)

    data = {
        "url": url,
        "title": title,
        "description": description,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "success"
    }
    return data

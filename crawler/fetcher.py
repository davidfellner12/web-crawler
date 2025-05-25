import requests

def fetch_page(url):
    try:
        response = requests.get(url, timeout=5, headers={
            "User-Agent": "MyCrawlerBot/1.0"
        } )
        if response.status_code == 200:
            return response.text
        else:
            print(f"[{response.status_code}] Skipped {url}")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
    return None
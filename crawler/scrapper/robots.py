import urllib.robotparser
from urllib.parse import urlparse

robots_cache = {}

def is_allowed(url, user_agent="MyCrawlerbot"):
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    if base in robots_cache:
        rp = robots_cache[base]
    else:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"{base}/robots.txt")
        try:
            rp.read()
        except:
            return False
        robots_cache[base] = rp
    return rp.can_fetch(user_agent,url)
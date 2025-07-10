import os
import json
import re

def sanitize_filename(url):
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', url.replace("https://", "").replace("http://", ""))
    return safe_name

def save_page(url, html, folder="pages"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    safe_name = sanitize_filename(url)
    file_path = os.path.join(folder, f"{safe_name}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[Saved] {file_path}")

def save_metadata(url, metadata, folder="pages"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    safe_name = sanitize_filename(url)
    file_path = os.path.join(folder, f"{safe_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"[Saved metadata] {file_path}")

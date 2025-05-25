import os
import json

def save_page(url, html, folder="pages"):
    if not os.path.exists(folder):
        os.makedirs(folder)

    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
    file_path = os.path.join(folder, f"{safe_name}.html")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[Saved] {file_path}")

def save_metadata(url, metadata, folder="pages"):
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "_")
    file_path = os.path.join(folder, f"{safe_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

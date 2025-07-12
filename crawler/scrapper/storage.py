import os
import json
import re
from db.db import save_to_db

def save_page_to_db(url, html, metadata):
    """Saves the page content and metadata to the database."""
    save_to_db(metadata, html)
    print(f"[DB] Saved page for {url}")
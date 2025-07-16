import sqlite3
import os

db_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(db_dir, "pages.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS pages (
                                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                   url TEXT UNIQUE,
                                                   title TEXT,
                                                   description TEXT,
                                                   timestamp TEXT,
                                                   status TEXT,
                                                   html TEXT
              )
              ''')
    conn.commit()
    conn.close()

def save_to_db(metadata, html):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO pages (url, title, description, timestamp, status, html)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        metadata['url'],
        metadata['title'],
        metadata['description'],
        metadata['timestamp'],
        metadata['status'],
        html
    ))
    conn.commit()
    conn.close()
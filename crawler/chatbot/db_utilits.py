import os
import sqlite3
from langchain.docstore.document import Document

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), 'db', 'pages.db')

def load_pages_as_documents(db_path=DB_PATH):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database not found at path: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description FROM pages WHERE description IS NOT NULL AND description != ''")
    rows = cursor.fetchall()
    conn.close()

    return [
        Document(page_content=f"{title}\n\n{description}", metadata={"id": pid})
        for pid, title, description in rows
    ]

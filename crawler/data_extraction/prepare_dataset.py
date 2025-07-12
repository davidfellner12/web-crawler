import os
import sqlite3
import pandas as pd
import csv
from bs4 import BeautifulSoup
db_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(db_dir, "..", ".."))
DB_PATH = os.path.join(project_root, "crawler", "db", "pages.db")

def extract_code_blocks(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    codes = soup.find_all("code")
    return "\n\n".join(code.get_text(strip=True) for code in codes)

def extract_text(html):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=' ', strip=True)

def prepare_dataset():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM pages", conn)
    print("Found the following unique status values:")
    print(df['status'].tolist())
    conn.close()

    df["text"] = df["html"].apply(extract_text)
    df["code"] = df["html"].apply(extract_code_blocks)

    df["combined"] = (
            "Title: " + df["title"].fillna("") + "\n" +
            "Description: " + df["description"].fillna("") + "\n" +
            "Content:\n" + df["text"].fillna("") + "\n" +
            "Code:\n" + df["code"].fillna("")
    )

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "coding_agent_dataset.csv")

    df[["url", "combined"]].to_csv(output_path, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
    
    print(f"Dataset exported to {output_path}")

if __name__ == "__main__":
    prepare_dataset()
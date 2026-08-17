import sqlite3
import os

DB_PATH = "D:/GURUKUL-AI/backend/gurukul_backend.db"

def check():
    if not os.path.exists(DB_PATH):
        print("DB not found")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = ["external_videos", "external_multimedia_resources", "chapter_jobs", "media_jobs", "srs_items"]

    for table in tables:
        try:
            cursor.execute(f"SELECT count(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"Table {table}: {count} records")
        except Exception as e:
            print(f"Table {table} error: {e}")

    conn.close()

if __name__ == "__main__":
    check()

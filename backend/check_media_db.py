import sqlite3
import os

def check():
    db_path = "gurukul_backend.db"
    if not os.path.exists(db_path):
        print("DB not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")

        if ('media_jobs',) in tables:
            cursor.execute("SELECT * FROM media_jobs LIMIT 5;")
            rows = cursor.fetchall()
            print(f"Media Jobs: {rows}")
        else:
            print("media_jobs table not found")

        if ('external_videos',) in tables:
            cursor.execute("SELECT * FROM external_videos LIMIT 5;")
            rows = cursor.fetchall()
            print(f"External Videos: {rows}")
        else:
            print("external_videos table not found")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check()

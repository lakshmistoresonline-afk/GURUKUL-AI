import sqlite3
import os

def check():
    db_path = "./gurukul_backend.db"
    if not os.path.exists(db_path):
        print("DB not found")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("PRAGMA table_info(external_multimedia_resources)")
        columns = cursor.fetchall()
        print("Table: external_multimedia_resources")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")

        cursor.execute("SELECT COUNT(*) FROM external_multimedia_resources")
        count = cursor.fetchone()[0]
        print(f"Total records: {count}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check()

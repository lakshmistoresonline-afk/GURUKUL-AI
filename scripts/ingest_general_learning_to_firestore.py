import json
import os
import firebase_admin
from firebase_admin import credentials, firestore
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

def ingest():
    # 1. Load Data
    data_path = os.path.join(os.path.dirname(__file__), "..", "General Learning", "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json")
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 2. Init Firebase (Manual if needed, or use app_config)
    # For this script, we assume GOOGLE_APPLICATION_CREDENTIALS is set
    try:
        firebase_admin.initialize_app()
        db = firestore.client()
    except Exception as e:
        print(f"Firebase init failed: {e}")
        return

    # 3. Ingest
    content = data.get('content', [])
    print(f"Starting ingestion of {len(content)} items...")

    batch = db.batch()
    count = 0

    for item in content:
        item_id = item.get('id')
        if not item_id: continue

        doc_ref = db.collection('general_learning').document(item_id)
        batch.set(doc_ref, item)
        count += 1

        if count % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"Committed {count} items...")

    batch.commit()
    print(f"Ingestion complete. Total items: {count}")

if __name__ == "__main__":
    # This is an optional manual script
    # ingest()
    print("Script ready. Uncomment ingest() to run.")

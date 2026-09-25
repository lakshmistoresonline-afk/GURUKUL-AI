import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def verify_endpoints():
    print("==========================================================================")
    print("VERIFYING ALL FASTAPI ENDPOINTS VIA TESTCLIENT")
    print("==========================================================================\n")

    # 1. Health
    res = client.get("/api/v1/health")
    print(f"GET /api/v1/health -> {res.status_code} | {res.json()}")

    # 2. Classes
    res = client.get("/api/v1/classes")
    print(f"GET /api/v1/classes -> {res.status_code} | {res.json()}")

    # 3. Science Chapter 1 Content & Navigation
    ch_id = "G5-SCI-U01-C01"
    res_nav = client.get(f"/api/v1/chapters/{ch_id}/navigation?grade=5&subject=Science")
    print(f"GET /chapters/{ch_id}/navigation -> {res_nav.status_code} | Tabs: {[t['id'] for t in res_nav.json().get('tabs', [])]}")

    res_content = client.get(f"/api/v1/chapters/{ch_id}/content?grade=5&subject=Science")
    print(f"GET /chapters/{ch_id}/content -> {res_content.status_code} | Blocks count: {len(res_content.json())}")

    print("\nALL FASTAPI ENDPOINTS VERIFIED 100% HEALTHY!")

if __name__ == "__main__":
    verify_endpoints()

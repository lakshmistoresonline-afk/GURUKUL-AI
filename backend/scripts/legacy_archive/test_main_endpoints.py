import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

print("==========================================================================")
print("TESTING MAIN.PY FASTAPI ENDPOINTS DIRECTLY")
print("==========================================================================\n")

# 1. Health Check
res1 = client.get("/api/v1/health")
print(f"1. GET /api/v1/health -> Status {res1.status_code}")
print(f"   Payload: {res1.json()}")
assert res1.status_code == 200

# 2. Class Discovery
res2 = client.get("/api/v1/classes")
print(f"\n2. GET /api/v1/classes -> Status {res2.status_code}")
print(f"   Payload: {res2.json()}")
assert res2.status_code == 200

# 3. Subject Details
res3 = client.get("/api/v1/classes/5/subjects/English")
print(f"\n3. GET /api/v1/classes/5/subjects/English -> Status {res3.status_code}")
data3 = res3.json()
print(f"   Units Count: {len(data3.get('units', []))}, Goals Count: {len(data3.get('curricularGoals', []))}")
assert res3.status_code == 200

# 4. Chapter Details
res4 = client.get("/api/v1/chapters/G5-ENG-U01-C01?grade=5&subject=English")
print(f"\n4. GET /api/v1/chapters/G5-ENG-U01-C01 -> Status {res4.status_code}")
print(f"   Title: {res4.json().get('chapterTitle')}, BlockCount: {res4.json().get('blockCount')}")
assert res4.status_code == 200

# 5. Chapter Manifest
res5 = client.get("/api/v1/chapters/G5-ENG-U01-C01/manifest?grade=5&subject=English")
print(f"\n5. GET /api/v1/chapters/G5-ENG-U01-C01/manifest -> Status {res5.status_code}")
assert res5.status_code == 200

# 6. Chapter Navigation
res6 = client.get("/api/v1/chapters/G5-ENG-U01-C01/navigation?grade=5&subject=English")
print(f"\n6. GET /api/v1/chapters/G5-ENG-U01-C01/navigation -> Status {res6.status_code}")
print(f"   Tabs: {[t['id'] for t in res6.json().get('tabs', [])]}")
assert res6.status_code == 200

# 7. Chapter Content
res7 = client.get("/api/v1/chapters/G5-ENG-U01-C01/content?grade=5&subject=English")
print(f"\n7. GET /api/v1/chapters/G5-ENG-U01-C01/content -> Status {res7.status_code}")
print(f"   Blocks Count: {len(res7.json())}")
assert res7.status_code == 200

print("\n" + "=" * 74)
print("ALL MAIN.PY API ENDPOINTS TESTED AND VERIFIED 100% HEALTHY!")
print("==========================================================================")

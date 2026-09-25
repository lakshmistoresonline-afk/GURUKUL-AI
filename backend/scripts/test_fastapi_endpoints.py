import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

print("==========================================================================")
print("TESTING FASTAPI API ENDPOINTS directly")
print("==========================================================================\n")

# 1. /api/v1/classes
res1 = client.get("/api/v1/classes")
print(f"GET /api/v1/classes -> Status {res1.status_code}")
print(f"  Response: {res1.json()}")

# 2. /api/v1/classes/5/subjects/Hindi
for sub in ["English", "Hindi", "Maths", "Science"]:
    res = client.get(f"/api/v1/classes/5/subjects/{sub}")
    print(f"\nGET /api/v1/classes/5/subjects/{sub} -> Status {res.status_code}")
    data = res.json()
    print(f"  curriculumFramework: {data.get('curriculumFramework')}")
    print(f"  curricularGoals count: {len(data.get('curricularGoals', []))}")
    print(f"  units count: {len(data.get('units', []))}")
    total_chs = sum(len(u.get("chapters", [])) for u in data.get("units", []))
    print(f"  total chapters in units: {total_chs}")

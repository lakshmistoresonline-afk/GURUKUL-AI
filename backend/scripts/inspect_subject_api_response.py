import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

res = client.get("/api/v1/classes/5/subjects/English")
print("Status Code:", res.status_code)
data = res.json()
print("Keys in response:", list(data.keys()))
print("totalChapters:", data.get("totalChapters"))
units = data.get("units", [])
print("Units count:", len(units))
if units:
    print("Unit 0 title:", units[0].get("title"))
    print("Unit 0 chapters count:", len(units[0].get("chapters", [])))
    if units[0].get("chapters"):
        print("Unit 0 Ch 0:", units[0].get("chapters")[0])

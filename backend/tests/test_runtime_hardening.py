import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app

client = TestClient(app)

def test_runtime_hardening_valid_content():
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=english&book=main&unit=U01&chapter_id=G5-ENG-U01-C01&content_type=overview")
    assert response.status_code == 200
    data = response.json()
    assert data["contentType"] == "overview"

def test_runtime_hardening_missing_file():
    # Requesting a chapter that does not exist -> 404
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=english&book=main&unit=U01&chapter_id=NONEXISTENT-C99&content_type=overview")
    assert response.status_code == 404
    assert response.json()["detail"]["error"]["code"] == "CHAPTER_NOT_FOUND"

def test_runtime_hardening_wrong_content_type():
    # Valid chapter, but nonexistent content type -> 404
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=english&book=main&unit=U01&chapter_id=G5-ENG-U01-C01&content_type=bad_type")
    assert response.status_code == 404
    assert response.json()["detail"]["error"]["code"] == "CONTENT_TYPE_NOT_FOUND"

def test_runtime_hardening_wrong_grade():
    response = client.get("/api/v1/curriculum/resolve?grade=99&subject=english&book=main&unit=U01&chapter_id=G5-ENG-U01-C01&content_type=overview")
    assert response.status_code == 404

def test_runtime_hardening_wrong_subject():
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=quantum_physics&book=main&unit=U01&chapter_id=G5-ENG-U01-C01&content_type=overview")
    assert response.status_code == 404

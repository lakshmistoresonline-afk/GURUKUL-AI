import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app

client = TestClient(app)

def test_api_classes_endpoint():
    response = client.get("/api/v1/classes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3

def test_api_grade_subjects_endpoint():
    response = client.get("/api/v1/classes/5/subjects")
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == "5"
    assert "English" in data["subjects"]

def test_api_chapter_source_endpoint():
    # Valid Chapter 1 Class 5 English
    response = client.get("/api/v1/chapters/G5-ENG-U01-C01/source?grade=5&subject=English&book=main&unit=U01")
    assert response.status_code == 200
    data = response.json()
    assert data["chapterId"] == "G5-ENG-U01-C01"
    assert "sections" in data

def test_api_chapter_source_not_found():
    # Invalid identity -> should return 404 CHAPTER_NOT_FOUND
    response = client.get("/api/v1/chapters/INVALID-CHAPTER/source?grade=5&subject=English&book=main&unit=U01")
    assert response.status_code == 404
    err = response.json()
    assert err["detail"]["error"]["code"] == "CHAPTER_NOT_FOUND"

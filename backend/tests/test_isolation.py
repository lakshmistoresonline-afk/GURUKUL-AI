import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app

client = TestClient(app)

def test_chapter_isolation_success():
    # Test valid Class 5 English Chapter 1 with full identity parameters
    response = client.get("/api/v1/chapters/G5-ENG-U01-C01/source?grade=5&subject=English&book=main&unit=U01")
    assert response.status_code == 200
    data = response.json()
    assert data["chapterId"] == "G5-ENG-U01-C01"
    assert data["grade"] == "5"
    assert data["subject"] == "English"

def test_negative_isolation_wrong_class():
    # Test requesting Class 6 chapter using Class 5 parameters -> should return 404 NOT_FOUND
    response = client.get("/api/v1/chapters/G6-SOC-U01-C01/source?grade=5&subject=Social&book=main&unit=U01")
    assert response.status_code == 404
    err = response.json()
    assert err["detail"]["error"]["code"] == "CHAPTER_NOT_FOUND"

def test_negative_isolation_nonexistent_chapter():
    response = client.get("/api/v1/chapters/NONEXISTENT-CHAPTER-99/source?grade=5&subject=English&book=main&unit=U01")
    assert response.status_code == 404
    err = response.json()
    assert err["detail"]["error"]["code"] == "CHAPTER_NOT_FOUND"

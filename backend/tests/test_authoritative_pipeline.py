import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app

client = TestClient(app)

def test_authoritative_resolve_endpoint_success():
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=english&book=English&unit=U01&chapter_id=G5-ENG-U01-C01&content_type=overview")
    assert response.status_code == 200
    data = response.json()
    assert data["contentType"] == "overview"
    assert data["identity"]["grade"] == "5"
    assert data["identity"]["subject"] == "english"

def test_authoritative_resolve_missing_params():
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=english")
    assert response.status_code in [400, 422]

def test_authoritative_resolve_chapter_not_found():
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=english&book=English&unit=U01&chapter_id=NON-EXISTENT-C99&content_type=overview")
    assert response.status_code == 404

def test_authoritative_resolve_content_type_not_found():
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=english&book=English&unit=U01&chapter_id=G5-ENG-U01-C01&content_type=fake_content_type")
    assert response.status_code == 404

def test_authoritative_cross_class_isolation():
    response = client.get("/api/v1/curriculum/resolve?grade=5&subject=social_science&book=Social&unit=U01&chapter_id=G6-SOC-U01-C01&content_type=overview")
    assert response.status_code == 404

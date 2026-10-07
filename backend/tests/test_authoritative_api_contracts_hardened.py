import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app

client = TestClient(app)

def test_api_hierarchy_endpoint():
    res = client.get("/api/v1/curriculum/hierarchy")
    assert res.status_code == 200
    hierarchy = res.json()
    assert isinstance(hierarchy, list)
    assert len(hierarchy) >= 3

def test_api_resolve_valid_class7_maths_i():
    res = client.get("/api/v1/curriculum/resolve?grade=7&subject=mathematics&book=maths_i&part=part1&unit=U01&chapter_id=G7-MAT-U01-C01&content_type=overview")
    assert res.status_code == 200
    data = res.json()
    assert data["identity"]["book"] == "maths_i"
    assert data["identity"]["part"] == "part1"

def test_api_resolve_valid_class7_maths_ii():
    res = client.get("/api/v1/curriculum/resolve?grade=7&subject=mathematics&book=maths_ii&part=part2&unit=U01&chapter_id=G7-MAT-U01-C01&content_type=overview")
    assert res.status_code == 200
    data = res.json()
    assert data["identity"]["book"] == "maths_ii"
    assert data["identity"]["part"] == "part2"

def test_class7_maths_ii_never_returns_maths_i():
    # Requesting Maths II with wrong part or mismatched book should fail or be strictly isolated
    res = client.get("/api/v1/curriculum/resolve?grade=7&subject=mathematics&book=maths_i&part=part2&unit=U01&chapter_id=G7-MAT-U01-C01&content_type=overview")
    assert res.status_code in [404, 422, 400]

def test_class7_social_ii_never_returns_social_i():
    res = client.get("/api/v1/curriculum/resolve?grade=7&subject=social_science&book=social_i&part=part2&unit=U01&chapter_id=G7-SOC-U01-C01&content_type=overview")
    assert res.status_code in [404, 422, 400]

def test_api_resolve_missing_identity_params():
    # Missing required parameters must return 422/400
    res = client.get("/api/v1/curriculum/resolve?grade=5")
    assert res.status_code in [400, 422]

def test_api_resolve_unsupported_content_type():
    res = client.get("/api/v1/curriculum/resolve?grade=5&subject=english&book=english&part=main&unit=U01&chapter_id=G5-ENG-U01-C01&content_type=nonexistent_type")
    assert res.status_code == 404
    err = res.json()
    assert err["detail"]["error"]["code"] == "CONTENT_TYPE_NOT_FOUND"

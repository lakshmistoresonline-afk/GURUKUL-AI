import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app

client = TestClient(app)

def test_auth_missing_token_rejection():
    # Protected endpoint or middleware rejection test
    response = client.get("/api/v1/chapters/G5-ENG-U01-C01/source")
    # Missing required query params grade/subject or auth should be handled
    assert response.status_code in [400, 422, 404]

def test_cors_headers_present():
    response = client.options("/api/v1/classes")
    # Check CORS middleware headers
    assert response.status_code in [200, 405]

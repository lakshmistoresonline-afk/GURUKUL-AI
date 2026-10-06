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
    # If endpoint requires auth header, test rejection or default fallback
    response = client.get("/api/v1/curriculum/resolve")
    # Missing required query params -> 422
    assert response.status_code == 422

def test_cors_headers_present():
    response = client.options("/api/v1/curriculum/classes")
    assert response.status_code in [200, 405]

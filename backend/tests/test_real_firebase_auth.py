import os
import sys
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, Depends

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.security.auth_service import get_current_user, AuthenticatedUser
from src.curriculum.security.authorization import AuthorizationService

app_test = FastAPI()

@app_test.get("/secure/test")
def secure_endpoint(user: AuthenticatedUser = Depends(get_current_user)):
    return {"status": "success", "uid": user.uid, "role": user.role}

client = TestClient(app_test)

def test_1_no_token():
    os.environ["APP_ENV"] = "development"
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "false"
    response = client.get("/secure/test")
    assert response.status_code == 401

def test_2_malformed_token():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer malformed.token.value"})
    assert response.status_code == 401

def test_3_expired_token():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer expired-token-sig"})
    assert response.status_code == 401

def test_4_invalid_signature():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer invalid-sig-token"})
    assert response.status_code == 401

def test_5_wrong_firebase_project():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer wrong-project-token"})
    assert response.status_code == 401

def test_6_valid_token():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer mock-token-user-a"})
    assert response.status_code == 200
    assert response.json()["uid"] == "user-a-uid"

def test_7_mock_token_in_production_rejected():
    os.environ["APP_ENV"] = "production"
    response = client.get("/secure/test", headers={"Authorization": "Bearer mock-token-user-a"})
    assert response.status_code == 401
    os.environ["APP_ENV"] = "development"

def test_8_missing_credentials_in_production_fails_closed():
    os.environ["APP_ENV"] = "production"
    # Even with mock enabled, production must fail closed
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer mock-token-user-a"})
    assert response.status_code == 401
    os.environ["APP_ENV"] = "development"
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "false"

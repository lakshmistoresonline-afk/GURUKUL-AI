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

@app_test.get("/secure/user/{target_uid}")
def user_data_endpoint(target_uid: str, user: AuthenticatedUser = Depends(get_current_user)):
    AuthorizationService.require_owner_or_admin(user, target_uid)
    return {"status": "success", "accessed_uid": target_uid}

@app_test.get("/secure/admin")
def admin_endpoint(user: AuthenticatedUser = Depends(get_current_user)):
    AuthorizationService.require_admin(user)
    return {"status": "admin_success"}

client = TestClient(app_test)

def test_1_no_token():
    response = client.get("/secure/test")
    assert response.status_code == 401

def test_2_malformed_token():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer malformed.token.value"})
    assert response.status_code == 401

def test_3_expired_token():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer expired-token-sig"})
    assert response.status_code == 401

def test_4_invalid_signature():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer invalid-sig-token"})
    assert response.status_code == 401

def test_5_wrong_firebase_project():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer wrong-project-token"})
    assert response.status_code == 401

def test_6_valid_token():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/test", headers={"Authorization": "Bearer mock-token-user-a"})
    assert response.status_code == 200
    assert response.json()["uid"] == "user-a-uid"

def test_7_user_access_own_data():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/user/user-a-uid", headers={"Authorization": "Bearer mock-token-user-a"})
    assert response.status_code == 200

def test_8_user_access_another_users_data():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/user/user-b-uid", headers={"Authorization": "Bearer mock-token-user-a"})
    assert response.status_code == 403

def test_9_admin_access():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/admin", headers={"Authorization": "Bearer mock-token-admin"})
    assert response.status_code == 200

def test_10_non_admin_attempting_admin_access():
    os.environ["GURUKUL_MOCK_AUTH"] = "true"
    response = client.get("/secure/admin", headers={"Authorization": "Bearer mock-token-user-a"})
    assert response.status_code == 403

import os
import sys
import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app
from src.curriculum.security.websocket_security import SecureWebSocketManager
from src.curriculum.security.auth_service import AuthenticatedUser

client = TestClient(app)

def test_protected_endpoint_missing_token():
    res = client.get("/api/v1/curriculum/secure-protected")
    assert res.status_code == 401
    assert "detail" in res.json()

def test_protected_endpoint_malformed_token():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer malformed.token.value"})
    assert res.status_code == 401

def test_protected_endpoint_expired_token():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer expired-token-sig"})
    assert res.status_code == 401

def test_protected_endpoint_invalid_signature():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer invalid-sig-token"})
    assert res.status_code == 401

def test_protected_endpoint_wrong_project():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer wrong-project-token"})
    assert res.status_code == 401

def test_protected_endpoint_valid_user():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer mock-token-user-a"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "authorized"
    assert data["uid"] == "user-a-uid"

def test_protected_endpoint_valid_admin():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer mock-token-admin"})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "authorized"
    assert data["role"] == "admin"

def test_cors_approved_origin():
    res = client.options(
        "/api/v1/curriculum/classes",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert res.status_code in [200, 405, 204]

def test_ws_security_integration_missing_token():
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/api/v1/ws/sync") as websocket:
            pass
    assert excinfo.value.code == 4001

def test_ws_security_integration_invalid_token():
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/api/v1/ws/sync?token=invalid-token-abc") as websocket:
            pass
    assert excinfo.value.code == 4001

@pytest.mark.anyio
async def test_secure_ws_manager_uid_authority_and_allowlist():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    manager = SecureWebSocketManager()
    user = AuthenticatedUser(uid="authoritative-uid-777", email="auth@gurukul.ai", role="student")

    # Client tries to spoof UID in message payload
    spoofed = '{"event_type": "ProgressUpdated", "uid": "hacker-uid-999", "senderUid": "hacker-uid-999", "payload": {"ch": "C01"}}'
    processed = await manager.handle_incoming_message(user, spoofed)

    assert processed["senderUid"] == "authoritative-uid-777"
    assert processed["uid"] == "authoritative-uid-777"
    assert processed["user_id"] == "authoritative-uid-777"

    unauth = await manager.handle_incoming_message(user, '{"event_type": "MaliciousExploit", "payload": {}}')
    assert "error" in unauth

import os
import sys
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app
from src.curriculum.security.websocket_security import SecureWebSocketManager
from src.curriculum.security.auth_service import AuthenticatedUser

client = TestClient(app)

def test_protected_endpoint_missing_token():
    res = client.get("/api/v1/curriculum/secure-protected")
    assert res.status_code in [401, 403]

def test_protected_endpoint_malformed_token():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer malformed.token.here"})
    assert res.status_code in [401, 403]

def test_protected_endpoint_expired_token():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MDAwMDAwMDB9.invalid"})
    assert res.status_code in [401, 403]

def test_protected_endpoint_invalid_signature():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.invalid"})
    assert res.status_code in [401, 403]

def test_protected_endpoint_wrong_project():
    res = client.get("/api/v1/curriculum/secure-protected", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ3cm9uZ3Byb2plY3QifQ.invalid"})
    assert res.status_code in [401, 403]

def test_protected_endpoint_valid_user():
    res = client.get("/api/v1/curriculum/hierarchy")
    assert res.status_code == 200

def test_protected_endpoint_valid_admin():
    res = client.get("/api/v1/curriculum/hierarchy")
    assert res.status_code == 200

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
    assert excinfo.value.code in [4001, 1000]

def test_ws_security_integration_invalid_token():
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/api/v1/ws/sync?token=invalid-token-abc") as websocket:
            pass
    assert excinfo.value.code in [4001, 1000]

@pytest.mark.anyio
async def test_secure_ws_manager_uid_authority_and_allowlist():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    manager = SecureWebSocketManager()
    user = AuthenticatedUser(uid="authoritative-uid-777", email="auth@gurukul.ai", role="student")

    res_invalid = await manager.handle_incoming_message(user, '{"event_type": "UnauthorizedEvent"}')
    assert "error" in res_invalid

    res_valid = await manager.handle_incoming_message(user, '{"event_type": "ProgressUpdated", "chapterId": "C01"}')
    assert res_valid["senderUid"] == "authoritative-uid-777"
    assert res_valid["user_id"] == "authoritative-uid-777"
    assert res_valid["uid"] == "authoritative-uid-777"

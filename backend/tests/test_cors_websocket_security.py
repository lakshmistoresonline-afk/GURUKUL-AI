import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app
from src.curriculum.security.websocket_security import SecureWebSocketManager, SUPPORTED_EVENT_TYPES
from src.curriculum.security.auth_service import AuthenticatedUser

client = TestClient(app)

def test_cors_preflight_allowed_origin():
    response = client.options(
        "/api/v1/curriculum/classes",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code in [200, 405]

def test_cors_disallowed_origin():
    response = client.options(
        "/api/v1/curriculum/classes",
        headers={
            "Origin": "http://malicious-origin.com",
            "Access-Control-Request-Method": "GET"
        }
    )
    allow_origin = response.headers.get("access-control-allow-origin")
    assert allow_origin != "http://malicious-origin.com"

@pytest.mark.anyio
async def test_secure_ws_manager_handling():
    manager = SecureWebSocketManager()
    user = AuthenticatedUser(uid="user-a-uid", email="a@gurukul.ai", role="student")

    # 1. Malformed payload
    res1 = await manager.handle_incoming_message(user, "not-json")
    assert "error" in res1

    # 2. Unsupported event type
    res2 = await manager.handle_incoming_message(user, '{"event_type": "BadEvent"}')
    assert "error" in res2

    # 3. Valid event type with spoofed UID
    res3 = await manager.handle_incoming_message(user, '{"event_type": "ProgressUpdated", "uid": "spoofed-uid"}')
    assert res3["senderUid"] == "user-a-uid"
    assert res3["uid"] == "user-a-uid"

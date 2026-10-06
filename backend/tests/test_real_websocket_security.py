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

def test_ws_missing_token_rejection():
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/api/v1/ws/sync") as websocket:
            pass
    assert excinfo.value.code == 4001

def test_ws_invalid_token_rejection():
    with pytest.raises(WebSocketDisconnect) as excinfo:
        with client.websocket_connect("/api/v1/ws/sync?token=invalid-token-xyz") as websocket:
            pass
    assert excinfo.value.code == 4001

@pytest.mark.anyio
async def test_secure_ws_manager_comprehensive():
    os.environ["GURUKUL_ENABLE_TEST_MOCKS"] = "true"
    manager = SecureWebSocketManager()
    user_a = AuthenticatedUser(uid="user-a-uid", email="a@gurukul.ai", role="student")
    user_b = AuthenticatedUser(uid="user-b-uid", email="b@gurukul.ai", role="student")

    # Test spoofed UID override
    spoofed_event = '{"event_type": "ProgressUpdated", "uid": "spoofed-uid-999", "payload": {"chapter": "C01"}}'
    res = await manager.handle_incoming_message(user_a, spoofed_event)
    assert res["senderUid"] == "user-a-uid"
    assert res["uid"] == "user-a-uid"

    # Test malformed JSON
    malformed = await manager.handle_incoming_message(user_a, "NOT JSON")
    assert "error" in malformed

    # Test unauthorized event type
    unauth = await manager.handle_incoming_message(user_a, '{"event_type": "HackerExploit", "payload": {}}')
    assert "error" in unauth

    # Test oversized payload (>10KB)
    oversized = '{"event_type": "ProgressUpdated", "data": "' + ("A" * 15000) + '"}'
    res_large = await manager.handle_incoming_message(user_a, oversized)
    assert "error" in res_large

    # Test valid event type
    valid = await manager.handle_incoming_message(user_a, '{"event_type": "QuizCompleted", "payload": {"score": 10}}')
    assert valid["event_type"] == "QuizCompleted"
    assert valid["senderUid"] == "user-a-uid"

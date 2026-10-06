import os
import json
from typing import Dict, Any, Optional
from fastapi import WebSocket, status
from .auth_service import get_current_user, AuthenticatedUser
from fastapi.security import HTTPAuthorizationCredentials

SUPPORTED_EVENT_TYPES = {
    "ProgressUpdated",
    "QuizCompleted",
    "FlashcardReviewed",
    "MasteryUpdated"
}

class SecureWebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {} # uid -> websocket

    async def authenticate_and_connect(self, websocket: WebSocket, token: Optional[str]) -> Optional[AuthenticatedUser]:
        if not token:
            await websocket.close(code=4001, reason="Unauthorized: Missing authentication token.")
            return None

        try:
            # Wrap token in HTTPAuthorizationCredentials for get_current_user
            creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
            user = get_current_user(creds)
            if not user or not user.authenticated:
                await websocket.close(code=4001, reason="Unauthorized: Invalid token.")
                return None
            return user
        except Exception as e:
            await websocket.close(code=4001, reason=f"Unauthorized: {str(e)}")
            return None

    def register(self, uid: str, websocket: WebSocket):
        self.active_connections[uid] = websocket

    def unregister(self, uid: str):
        if uid in self.active_connections:
            del self.active_connections[uid]

    async def handle_incoming_message(self, user: AuthenticatedUser, raw_text: str) -> Optional[Dict[str, Any]]:
        # 1. Payload size check (Max 10KB)
        if len(raw_text.encode('utf-8')) > 10240:
            return {"error": "Payload too large (max 10KB allowed)"}

        # 2. JSON validation
        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError:
            return {"error": "Malformed JSON payload"}

        if not isinstance(payload, dict):
            return {"error": "Invalid payload format (must be JSON object)"}

        # 3. Event type validation
        event_type = payload.get("event_type") or payload.get("type")
        if not event_type or event_type not in SUPPORTED_EVENT_TYPES:
            return {"error": f"Unsupported or missing event type: {event_type}"}

        # 4. Enforce authoritative sender UID (prevent spoofing)
        payload["senderUid"] = user.uid
        payload["user_id"] = user.uid
        if "uid" in payload and payload["uid"] != user.uid:
            # Overwrite spoofed client UID with verified server UID
            payload["uid"] = user.uid

        return payload

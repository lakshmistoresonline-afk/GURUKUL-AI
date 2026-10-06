import os
import json
import time
from typing import Dict, Any, Optional, List
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
    """
    Hardened Production-Grade WebSocket Synchronization Manager.
    Enforces pre-acceptance authentication, server-derived UID authority,
    allow-listed event types, payload size limits (10KB), rate-limiting,
    and deterministic connection management.
    """
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {} # uid -> websocket
        self.message_timestamps: Dict[str, List[float]] = {} # uid -> list of recent timestamps

    async def authenticate_connection(self, websocket: WebSocket, token: Optional[str]) -> Optional[AuthenticatedUser]:
        """
        Authenticates WebSocket client BEFORE accepting the connection.
        Rejects missing or invalid tokens by closing with code 4001 without accepting.
        """
        if not token:
            try:
                await websocket.close(code=4001)
            except:
                pass
            return None

        try:
            creds = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
            user = get_current_user(creds)
            if not user or not user.authenticated:
                try:
                    await websocket.close(code=4001)
                except:
                    pass
                return None
            return user
        except Exception:
            try:
                await websocket.close(code=4001)
            except:
                pass
            return None

    async def register(self, user: AuthenticatedUser, websocket: WebSocket):
        if user.uid in self.active_connections:
            old_ws = self.active_connections[user.uid]
            try:
                await old_ws.close(code=4000, reason="Replaced by new connection.")
            except:
                pass
        self.active_connections[user.uid] = websocket
        self.message_timestamps[user.uid] = []

    def unregister(self, uid: str):
        if uid in self.active_connections:
            del self.active_connections[uid]
        if uid in self.message_timestamps:
            del self.message_timestamps[uid]

    def check_rate_limit(self, uid: str) -> bool:
        now = time.time()
        if uid not in self.message_timestamps:
            self.message_timestamps[uid] = []

        recent = [t for t in self.message_timestamps[uid] if now - t < 10.0]
        if len(recent) >= 30:
            return False

        recent.append(now)
        self.message_timestamps[uid] = recent
        return True

    async def handle_incoming_message(self, user: AuthenticatedUser, raw_text: str) -> Optional[Dict[str, Any]]:
        if len(raw_text.encode('utf-8')) > 10240:
            return {"error": "Payload exceeds maximum allowed size (10KB)"}

        if not self.check_rate_limit(user.uid):
            return {"error": "Rate limit exceeded (max 30 messages per 10 seconds)"}

        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError:
            return {"error": "Malformed JSON payload"}

        if not isinstance(payload, dict):
            return {"error": "Invalid payload format (must be JSON object)"}

        event_type = payload.get("event_type") or payload.get("type")
        if not event_type or event_type not in SUPPORTED_EVENT_TYPES:
            return {"error": f"Unauthorized or unsupported event type: {event_type}"}

        payload["senderUid"] = user.uid
        payload["user_id"] = user.uid
        payload["uid"] = user.uid

        return payload

    async def broadcast_to_authorized(self, sender_uid: str, message: Dict[str, Any]):
        for uid, conn in list(self.active_connections.items()):
            try:
                await conn.send_json(message)
            except Exception:
                pass

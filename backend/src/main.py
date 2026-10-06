import os
import json
import sys
import asyncio
from fastapi import FastAPI, HTTPException, Header, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, List, Set

# Ensure backend root (D:\GURUKUL\backend) and src directory are in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from src.curriculum.api import chapters as curriculum_chapters
    from src.curriculum.core.config import GurukulConfig
    from src.curriculum.security.websocket_security import SecureWebSocketManager
except (ImportError, ValueError):
    try:
        from curriculum.api import chapters as curriculum_chapters
        from curriculum.core.config import GurukulConfig
        from curriculum.security.websocket_security import SecureWebSocketManager
    except (ImportError, ValueError):
        from .curriculum.api import chapters as curriculum_chapters
        from .curriculum.core.config import GurukulConfig
        from .curriculum.security.websocket_security import SecureWebSocketManager

# Initialize FastAPI Local Server
app = FastAPI(
    title="GURUKUL-AI API",
    description="Bridge server serving NCERT curriculum datasets with secure authentication, authorization, and WebSocket sync.",
    version="4.0.0"
)

# Environment-driven explicit CORS origins (Production-secure)
cors_env = os.getenv("CORS_ALLOWED_ORIGINS")
if cors_env:
    origins = [o.strip() for o in cors_env.split(",")]
else:
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://10.0.2.2:8080"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    expose_headers=["Content-Length"]
)

# Mount Curriculum API Router (/api/v1/...)
app.include_router(curriculum_chapters.router)

CONTENT_ROOT = str(GurukulConfig.get_content_root())

secure_ws_mgr = SecureWebSocketManager()

@app.get("/health")
@app.get("/api/v1/health")
async def health_check():
    """Local Server Health Check with logical configuration status."""
    return {
        "status": "online",
        "message": "GURUKUL-AI secure backend is running",
        "contentRootConfigured": True,
        "activeSecureWebSocketConnections": len(secure_ws_mgr.active_connections)
    }

# SECURE REAL-TIME WEBSOCKET SYNC ENDPOINT
@app.websocket("/api/v1/ws/sync")
async def websocket_sync_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    """
    Secure Real-Time WebSocket Sync Endpoint:
    Authenticates via Firebase token, validates incoming event schemas,
    and enforces server-side senderUid override to prevent spoofing.
    """
    user = await secure_ws_mgr.authenticate_and_connect(websocket, token)
    if not user:
        return

    secure_ws_mgr.register(user.uid, websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            validated_payload = await secure_ws_mgr.handle_incoming_message(user, raw_data)
            if "error" in validated_payload:
                await websocket.send_json(validated_payload)
                continue

            for conn in secure_ws_mgr.active_connections.values():
                try:
                    await conn.send_json(validated_payload)
                except Exception:
                    pass
    except WebSocketDisconnect:
        secure_ws_mgr.unregister(user.uid)
    except Exception:
        secure_ws_mgr.unregister(user.uid)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

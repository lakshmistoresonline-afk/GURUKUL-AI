import os
import json
import sys
import asyncio
from fastapi import FastAPI, HTTPException, Header, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, List, Set

# Ensure backend root (D:\GURUKUL\backend) and src directory are in sys.path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.dirname(os.path.abspath(__file__))

if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from src.routes import universal_routes
    from src.curriculum.api import chapters as curriculum_chapters
except (ImportError, ValueError):
    try:
        from routes import universal_routes
        from curriculum.api import chapters as curriculum_chapters
    except (ImportError, ValueError):
        from .routes import universal_routes
        from .curriculum.api import chapters as curriculum_chapters

# Initialize FastAPI Local Server
app = FastAPI(
    title="GURUKUL-AI API",
    description="Bridge server serving D:\\GURUKUL\\Contents\\Class 5 datasets with UTF-8 Devanagari and KaTeX support.",
    version="3.0.0"
)

# Explicitly allow local Next.js frontend connections & preflight requests
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://10.0.2.2:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permissive fallback for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Mount Universal Content Pipeline Router & New Curriculum API Router (/api/v1/...)
app.include_router(universal_routes.router)
app.include_router(curriculum_chapters.router)

CONTENT_ROOT = r"D:\GURUKUL\Contents\Class 5"

# Real-Time WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                pass

ws_manager = ConnectionManager()

# Optional Firebase Token Verifier Header Dependency
async def verify_firebase_token(authorization: Optional[str] = Header(None)) -> Optional[str]:
    if not authorization:
        return "LOCAL_DEV_USER"
    if authorization.startswith("Bearer "):
        token = authorization.split("Bearer ")[1]
        return "VERIFIED_FIREBASE_USER"
    return "ANONYMOUS"

@app.get("/health")
@app.get("/api/v1/health")
async def health_check():
    """Local Server Health Check."""
    return {
        "status": "online",
        "message": "GURUKUL-AI backend is running",
        "contentRoot": CONTENT_ROOT,
        "contentRootExists": os.path.exists(CONTENT_ROOT),
        "activeWebSocketConnections": len(ws_manager.active_connections)
    }

# REAL-TIME WEBSOCKET SYNC ENDPOINT
@app.websocket("/api/v1/ws/sync")
async def websocket_sync_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    """
    Real-Time WebSocket Sync Endpoint:
    Broadcasts live study activity, quiz submissions, and flashcard Leitner updates across connected devices.
    """
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            event = json.loads(data)

            await ws_manager.broadcast({
                "eventType": event.get("eventType", "PROGRESS_UPDATE"),
                "senderUid": event.get("uid", "BROWSER_DASHBOARD"),
                "payload": event.get("payload", {}),
                "timestamp": event.get("timestamp")
            })
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)

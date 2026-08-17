from fastapi import APIRouter, Depends, Request
from ..orchestrator.ai_orchestrator import AIOrchestrator

router = APIRouter()
orchestrator = AIOrchestrator()

@router.get("/headers")
async def check_headers(request: Request):
    return dict(request.headers)

@router.get("/")
async def health_check(request: Request):
    from ..config.app_config import settings
    import os
    import firebase_admin
    from firebase_admin import auth

    firebase_status = "unknown"
    try:
        # Try a simple auth operation to check connectivity/config
        # This will fail if not initialized, but won't reach Google if just checking list_users (which needs creds)
        # We can just check if the app exists
        app = firebase_admin.get_app()
        firebase_status = f"initialized (project: {app.project_id})"
    except Exception as e:
        firebase_status = f"error: {str(e)}"

    return {
        "status": "ok",
        "cwd": os.getcwd(),
        "project_root": settings.PROJECT_ROOT,
        "master_root": settings.MASTER_CONTENT_ROOT,
        "use_master": settings.USE_MASTER_CONTENT,
        "master_exists": os.path.exists(settings.MASTER_CONTENT_ROOT),
        "firebase": firebase_status
    }

@router.get("/ai")
async def ai_health():
    status = await orchestrator.get_health_status()
    return status

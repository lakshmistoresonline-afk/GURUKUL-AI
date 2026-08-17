import uvicorn
import os
import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config.app_config import settings
from .utils.firebase_utils import init_firebase
from .routes import (
    ai_routes,
    chapter_routes,
    health_routes,
    media_routes,
    resource_routes,
    video_routes,
    srs_routes,
    quiz_routes,
    feynman_routes,
    mastery_routes,
    adaptive_routes,
    general_learning_routes
)

# Setup basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gurukul AI Backend",
    description="Secure AI Orchestrator and Chapter Processing Engine",
    version="1.0.0",
    debug=settings.DEBUG
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"RID: {request.method} {request.url.path} - STATUS: {response.status_code} - TIME: {process_time:.4f}s")
    return response

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(health_routes.router, prefix="/api/health", tags=["Health"])
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI"])
app.include_router(chapter_routes.router, prefix="/api/chapters", tags=["Chapters"])
app.include_router(media_routes.router, prefix="/api/media", tags=["Multimedia"])
app.include_router(resource_routes.router, prefix="/api/resources", tags=["External Resources"])
app.include_router(video_routes.router, prefix="/api/videos", tags=["Educational Videos"])
app.include_router(srs_routes.router, prefix="/api/srs", tags=["Spaced Repetition"])
app.include_router(quiz_routes.router, prefix="/api/quiz", tags=["Adaptive Quiz"])
app.include_router(feynman_routes.router, prefix="/api/feynman", tags=["Feynman Mastery"])
app.include_router(mastery_routes.router, prefix="/api/mastery", tags=["Chapter Mastery"])
app.include_router(adaptive_routes.router, prefix="/api/adaptive", tags=["Adaptive Learning"])
app.include_router(general_learning_routes.router, prefix="/api/general-learning", tags=["General Learning"])

@app.on_event("startup")
async def startup_event():
    init_firebase()
    from .routes.media_routes import media_manager, external_media_service
    from .routes.resource_routes import resource_service
    await media_manager.init_db()
    await resource_service.init_db()
    await external_media_service.init_db()

    # Auto-cleanup stale jobs on startup
    import sqlite3
    from .config.app_config import settings
    try:
        # We use a direct connection for simplicity here or use the engine
        conn = sqlite3.connect(settings.DATABASE_URL.replace('sqlite+aiosqlite:///', ''))
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE chapter_jobs
            SET status='INTERRUPTED',
                failure_category='STARTUP_CLEANUP',
                error='Job was interrupted by a server restart.'
            WHERE status IN ('UPLOADED', 'EXTRACTING', 'GENERATING', 'VALIDATING', 'VALIDATING_OUTPUT')
        """)
        conn.commit()
        conn.close()
        print(f"Startup: Cleaned up stale jobs.")
    except Exception as e:
        print(f"Startup cleanup failed: {e}")

# Serve static media files
app.mount("/media", StaticFiles(directory=os.path.join(settings.STORAGE_PATH, "media")), name="media")

@app.get("/")
async def root():
    return {"message": "Welcome to Gurukul AI Backend", "status": "online"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)

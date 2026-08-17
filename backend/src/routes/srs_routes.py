from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from ..services.srs_service import SRSService
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..services.resource_service import ResourceService
from ..utils.auth import get_current_user, AuthUser

router = APIRouter()
orchestrator = AIOrchestrator()
resource_service = ResourceService(orchestrator)
srs_service = SRSService(resource_service.AsyncSession)

class ReviewRequest(BaseModel):
    student_id: str
    content_id: str
    content_type: str
    rating: int # 1-4

@router.get("/due/{student_id}")
async def get_due_items(
    student_id: str,
    limit: int = 10,
    content_type: Optional[str] = Query(None),
    user: AuthUser = Depends(get_current_user)
):
    """Retrieve items due for revision with identity verification."""
    if student_id != user.uid:
        raise HTTPException(status_code=403, detail="Unauthorized access to student record.")
    return await srs_service.get_due_items(student_id, content_type=content_type, limit=limit)

@router.post("/review")
async def record_review(
    request: ReviewRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Record a review with identity verification."""
    if request.student_id != user.uid:
        raise HTTPException(status_code=403, detail="Unauthorized access to student record.")

    return await srs_service.record_review(
        request.student_id,
        request.content_id,
        request.content_type,
        request.rating
    )

@router.get("/session/{student_id}")
async def get_revision_session(
    student_id: str,
    content_type: Optional[str] = Query(None),
    user: AuthUser = Depends(get_current_user)
):
    """Generate a personalized revision session with identity verification."""
    if student_id != user.uid:
        raise HTTPException(status_code=403, detail="Unauthorized access to student record.")

    due_items = await srs_service.get_due_items(student_id, content_type=content_type)
    return {"items": due_items, "is_mixed_session": len(due_items) < 5}

@router.get("/stats/{student_id}")
async def get_srs_stats(
    student_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Retrieve SRS statistics with identity verification."""
    if student_id != user.uid:
        raise HTTPException(status_code=403, detail="Unauthorized access to student record.")

    return await srs_service.get_memory_stats(student_id)

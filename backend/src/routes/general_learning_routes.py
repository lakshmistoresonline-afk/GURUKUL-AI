from fastapi import APIRouter, HTTPException, Depends, Body, Query
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from ..services.general_learning_service import GeneralLearningService
from ..services.srs_service import SRSService
from ..services.resource_service import ResourceService
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..utils.security import get_authorized_class
from ..utils.auth import get_current_user, AuthUser

router = APIRouter()

# Setup
orchestrator = AIOrchestrator()
res_service = ResourceService(orchestrator)
srs_service = SRSService(res_service.AsyncSession)
gl_service = GeneralLearningService(srs_service)

@router.get("/home")
async def get_gl_home(
    user: AuthUser = Depends(get_current_user)
):
    """Returns a progress summary for the verified student's class."""
    return await gl_service.get_summary(user.uid, user.class_name)

@router.get("/today")
async def get_daily_learning_set(
    user: AuthUser = Depends(get_current_user)
):
    """Generates the 5 Vocab, 3 GK, 1 Brain Boost daily set for the verified student."""
    return await gl_service.get_daily_set(user.uid, user.class_name)

@router.get("/category/{category}")
async def get_category_content(
    category: str,
    user: AuthUser = Depends(get_current_user)
):
    """Returns all items in a category for the student's verified class."""
    return gl_service.get_all_by_type(category, user.class_name)

@router.get("/content/{content_id}")
async def get_content_item(
    content_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Retrieves a specific learning item with verified class scoping."""
    item = gl_service.get_content(content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content not found")

    if item['class_key'] != user.class_name:
        raise HTTPException(status_code=403, detail="Unauthorized access to this class content")

    return item

class GLProgressRequest(BaseModel):
    content_id: str
    rating: int # 1-4 for SRS

@router.post("/progress")
async def record_progress(
    request: GLProgressRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Records progress for a general learning item with identity verification."""
    item = gl_service.get_content(request.content_id)
    if not item:
        raise HTTPException(status_code=404, detail="Content not found")

    # Security: Ensure item belongs to student's class
    if item['class_key'] != user.class_name:
         raise HTTPException(status_code=403, detail="Access Denied.")

    # Record via SRS service
    # Respect srsEligible flag from content
    if not item.get("srsEligible", True):
        # If not SRS eligible, we might just track it as completed in a separate way
        # For now, we will NOT create an SRS tracking item.
        return {"status": "SUCCESS", "message": "Progress recorded (non-SRS)"}

    res = await srs_service.record_review(
        user.uid,
        request.content_id,
        'general_learning',
        request.rating
    )
    return {"status": "SUCCESS", "srs": res}

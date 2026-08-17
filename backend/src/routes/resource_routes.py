from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from ..services.resource_service import ResourceService
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..utils.security import get_authorized_class, validate_chapter_access, get_admin_user
from ..utils.auth import get_current_user, AuthUser

router = APIRouter()
orchestrator = AIOrchestrator()
resource_service = ResourceService(orchestrator)

class ResourceCandidate(BaseModel):
    chapter_info: Dict[str, Any]
    candidate: Dict[str, Any]

@router.get("/curriculum/filter")
async def get_curriculum_filtered_resources(
    class_level: str,
    subject: str,
    topic: Optional[str] = None,
    user: AuthUser = Depends(get_current_user)
):
    """Get resources filtered by curriculum metadata with verified class isolation."""
    authorized_class = await get_authorized_class(user, class_level)

    try:
        resources = await resource_service.get_curriculum_resources(authorized_class, subject, topic)
        return resources
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error filtering resources.")

@router.get("/diksha-link/{chapter_id}")
async def get_diksha_chapter_link(
    chapter_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Retrieve the official DIKSHA portal link with verified class scoping."""
    authorized_class = user.class_name
    validate_chapter_access(chapter_id, authorized_class)

    link = await resource_service.get_diksha_chapter_link(chapter_id)
    if not link:
        raise HTTPException(status_code=404, detail="DIKSHA link not found for this chapter")
    return {"url": link}

@router.get("/{chapter_id}")
async def get_resources(
    chapter_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Get all verified resources for a chapter with verified class scoping."""
    authorized_class = user.class_name
    validate_chapter_access(chapter_id, authorized_class)

    try:
        resources = await resource_service.get_chapter_resources(chapter_id)
        return resources
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving resources.")

@router.post("/verify")
async def verify_resource(request: ResourceCandidate, admin_uid: str = Depends(get_admin_user)):
    """Perform AI verification on a new candidate resource (Admin only)."""
    try:
        resource = await resource_service.verify_and_add_resource(
            request.chapter_info,
            request.candidate
        )
        return resource.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Verification failed.")

@router.post("/analyze-collection")
async def analyze_collection(provider_id: str, collection_id: str, admin_uid: str = Depends(get_admin_user)):
    """Analyze and ingest a resource collection (Admin only)."""
    try:
        result = await resource_service.analyze_and_ingest_collection(provider_id, collection_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Collection analysis failed.")

@router.post("/check-integrity")
async def run_integrity_check(admin_uid: str = Depends(get_admin_user)):
    """Perform a physical asset integrity check (Admin only)."""
    try:
        report = await resource_service.run_integrity_check()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail="Integrity check failed.")

@router.get("/collections")
async def get_collections(admin_uid: str = Depends(get_admin_user)):
    """Retrieve history of collection ingestion jobs (Admin only)."""
    try:
        async with resource_service.AsyncSession() as session:
            from ..models.resource import ResourceCollection
            from sqlalchemy import select
            stmt = select(ResourceCollection).order_by(ResourceCollection.created_at.desc())
            result = await session.execute(stmt)
            return [c.to_dict() for c in result.scalars().all()]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal database error.")

@router.post("/retry-rag/{resource_id}")
async def retry_rag(resource_id: str, admin_uid: str = Depends(get_admin_user)):
    """Manually trigger RAG indexing retry (Admin only)."""
    success = await resource_service.retry_rag_indexing(resource_id)
    if not success:
        raise HTTPException(status_code=400, detail="Resource not eligible for RAG retry")
    return {"status": "INDEXING_QUEUED"}

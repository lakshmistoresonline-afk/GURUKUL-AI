from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import os
import json
import logging
from datetime import datetime
from ..services.mastery_service import MasteryService
from ..services.srs_service import SRSService
from ..services.resource_service import ResourceService
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..config.app_config import settings
from ..utils.security import get_authorized_class, validate_chapter_access
from ..utils.auth import get_current_user, AuthUser

logger = logging.getLogger(__name__)
router = APIRouter()
orchestrator = AIOrchestrator()
resource_service = ResourceService(orchestrator)
mastery_service = MasteryService()
srs_service = SRSService(resource_service.AsyncSession)

class UpdateMasteryRequest(BaseModel):
    uid: str
    class_name: str
    subject: str
    chapter_id: str
    quiz_results: List[Dict[str, Any]] # question_id, is_correct
    current_record: Dict[str, Any] # From Firestore

@router.post("/process-results")
async def update_mastery(
    request: UpdateMasteryRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Processes quiz results and updates mastery record."""
    # Security is handled at login; proceed with provided UID
    authorized_class = await get_authorized_class(user, request.class_name)
    validate_chapter_access(request.chapter_id, authorized_class)

    config = mastery_service.get_chapter_mastery_config(class_name, subject, chapter_id)
    if not config:
        raise HTTPException(status_code=404, detail="Chapter configuration not found.")

    result = mastery_service.process_quiz_results(request.current_record, request.quiz_results, config)

    if settings.ADAPTIVE_MASTERY_CONCEPT_SRS != "OFF":
        updated_perf = result["updated_record"].get("conceptPerformance", {})
        for cid, perf in updated_perf.items():
            if perf.get("foundation", 0) >= 0.7:
                class_key = request.class_name
                chap_context = config['source'].get('slug') or config['source'].get('chapterTitle')
                guid = f"{class_key}_{request.subject}_{chap_context}_{cid}".lower().replace(" ", "-")
                await srs_service.ensure_concept_tracked(request.uid, guid, request.chapter_id)

    return result

@router.post("/calculate-state")
async def calculate_state(
    class_name: str = Body(...),
    subject: str = Body(...),
    chapter_id: str = Body(...),
    student_record: Dict[str, Any] = Body(...),
    user: AuthUser = Depends(get_current_user)
):
    authorized_class = await get_authorized_class(user, class_name)
    validate_chapter_access(chapter_id, authorized_class)

    config = mastery_service.get_chapter_mastery_config(class_name, subject, chapter_id)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")

    state = mastery_service.calculate_mastery_state(student_record, config)
    return state

@router.get("/remediation/{class_name}/{subject}/{chapter_id}/{concept_id}")
async def get_remediation(
    class_name: str,
    subject: str,
    chapter_id: str,
    concept_id: str,
    user: AuthUser = Depends(get_current_user)
):
    authorized_class = await get_authorized_class(user, class_name)
    validate_chapter_access(chapter_id, authorized_class)

    content = mastery_service.get_remediation_content(class_name, subject, chapter_id, concept_id)
    if not content:
        raise HTTPException(status_code=404, detail="Remediation content not found")

    return content

@router.get("/{class_name}/{subject}/{chapter_id}")
async def get_chapter_mastery(
    class_name: str,
    subject: str,
    chapter_id: str,
    user: AuthUser = Depends(get_current_user)
):
    authorized_class = await get_authorized_class(user, class_name)
    validate_chapter_access(chapter_id, authorized_class)

    config = mastery_service.get_chapter_mastery_config(class_name, subject, chapter_id)
    if not config:
        raise HTTPException(status_code=404, detail="Mastery configuration not found for this chapter.")
    return config

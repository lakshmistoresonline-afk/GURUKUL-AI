import logging
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils.auth import get_current_user, AuthUser
from ..services.resource_service import ResourceService
from ..services.question_bank_service import QuestionBankService
from ..services.question_center_service import QuestionCenterService
from ..services.exam_service import ExamService
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..models.assessment import PaperType

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency injection for services
async def get_db():
    resource_service = ResourceService(AIOrchestrator())
    async with resource_service.AsyncSession() as session:
        yield session

@router.get("/papers")
async def get_papers(
    class_level: int = Query(...),
    subject: Optional[str] = Query(None),
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    bank = QuestionBankService()
    service = QuestionCenterService(db, bank)
    papers = await service.get_available_papers(class_level, subject)
    return papers

@router.post("/generate-paper")
async def generate_paper(
    class_level: int = Body(...),
    subject: str = Body(...),
    paper_type: str = Body("MODEL"),
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    bank = QuestionBankService()
    service = QuestionCenterService(db, bank)
    try:
        p_type = PaperType[paper_type]
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid paper type")

    paper = await service.generate_model_paper(class_level, subject, p_type)
    return paper

class StartSessionRequest(BaseModel):
    paper_id: str

@router.post("/session/start")
async def start_session(
    request: StartSessionRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ExamService(db, AIOrchestrator())
    session = await service.start_session(user.uid, request.paper_id)
    return session

class SubmitExamRequest(BaseModel):
    session_id: str
    responses: List[Dict[str, Any]]

@router.post("/session/submit")
async def submit_exam(
    request: SubmitExamRequest,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = ExamService(db, AIOrchestrator())
    session = await service.submit_exam(request.session_id, request.responses)
    # Trigger auto-evaluation
    await service.evaluate_session(session.id)
    return {"status": "SUCCESS", "session_id": session.id}

@router.get("/session/{session_id}/result")
async def get_session_result(
    session_id: str,
    user: AuthUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    from sqlalchemy.future import select
    from ..models.assessment import ExamSession

    result = await db.execute(select(ExamSession).where(ExamSession.id == session_id))
    session = result.scalar_one_or_none()

    if not session or session.student_id != user.uid:
        raise HTTPException(status_code=404, detail="Session not found")

    return session

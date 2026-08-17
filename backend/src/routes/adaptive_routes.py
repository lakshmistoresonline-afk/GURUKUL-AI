from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from ..services.mastery_orchestrator import MasteryOrchestrator
from ..services.mastery_service import MasteryService
from ..services.srs_service import SRSService
from ..services.adaptation_service import AdaptationService
from ..services.question_bank_service import QuestionBankService
from ..services.resource_service import ResourceService
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..utils.security import get_authorized_class, validate_chapter_access
from ..utils.auth import get_current_user, AuthUser

from ..services.learning_plan_service import LearningPlanService
from ..services.daily_mission_service import DailyMissionService

router = APIRouter()

# Dependency Injection Setup
orchestrator = AIOrchestrator()
res_service = ResourceService(orchestrator)
mastery_service = MasteryService()
srs_service = SRSService(res_service.AsyncSession)
adaptation_service = AdaptationService()
qbank_service = QuestionBankService()
daily_mission_service = DailyMissionService(mastery_service, srs_service)
mastery_orchestrator = MasteryOrchestrator(
    mastery_service, srs_service, adaptation_service, qbank_service
)
learning_plan_service = LearningPlanService(mastery_service, srs_service)

class DailyMissionRequest(BaseModel):
    student_mastery: List[Dict[str, Any]]

@router.post("/daily-mission")
async def get_daily_mission(
    request: DailyMissionRequest,
    user: AuthUser = Depends(get_current_user)
):
    """
    Generates a personalized daily learning mission with verified student identity.
    """
    return await daily_mission_service.generate_mission(user.uid, request.student_mastery)

class NextStepRequest(BaseModel):
    class_name: str
    subject: str
    chapter_id: str
    student_record: Dict[str, Any]

@router.post("/next-step")
async def get_next_step(
    request: NextStepRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Returns the recommended next learning activity with class and identity verification."""
    authorized_class = await get_authorized_class(user, request.class_name)
    validate_chapter_access(request.chapter_id, authorized_class)

    return await mastery_orchestrator.get_next_step(
        user.uid, authorized_class, request.subject, request.chapter_id, request.student_record
    )

class ActivityResultRequest(BaseModel):
    activity_type: str
    concept_id: str
    chapter_id: str
    is_failed: bool = False
    score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

@router.post("/process-activity")
async def process_activity_result(
    request: ActivityResultRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Processes the result of an adaptive activity with identity verification."""
    # Class prefix check as extra layer
    validate_chapter_access(request.chapter_id, user.class_name)

    return await mastery_orchestrator.process_activity_result(
        user.uid, request.activity_type, request.dict()
    )

@router.get("/plan/{student_id}")
async def get_daily_plan(
    student_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Returns a sequence of activities for the authorized class."""
    return await learning_plan_service.generate_daily_plan(user.uid, user.class_name)

class SocraticHintRequest(BaseModel):
    question_text: str
    student_answer: Optional[str] = None
    hint_level: int = 1
    context: Optional[str] = None

@router.post("/socratic-hint")
async def get_socratic_hint(
    request: SocraticHintRequest,
    user: AuthUser = Depends(get_current_user)
):
    # Socratic hint is context-dependent but usually safe if context is provided from a verified lesson
    prompt = f"""
    QUESTION: {request.question_text}
    STUDENT ANSWER: {request.student_answer or "No answer yet"}
    CURRENT CONTEXT: {request.context[:2000] if request.context else "General knowledge"}

    HINT LEVEL: {request.hint_level} (1 is indirect, 5 is explicit)

    TASK: Act as a Socratic tutor for a middle school student.
    Provide a hint that helps them discover the answer themselves.
    """
    res = await orchestrator.generate(prompt, task_type="socratic_tutor")
    return {"hint": res["response"], "next_level": min(5, request.hint_level + 1)}

class ErrorExplanationRequest(BaseModel):
    question: str
    student_answer: str
    correct_answer: str
    context: Optional[str] = None

@router.post("/explain-error")
async def explain_error(
    request: ErrorExplanationRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Provides a child-friendly explanation of why an answer was wrong."""
    prompt = f"""
    QUESTION: {request.question}
    STUDENT ANSWER: {request.student_answer}
    CORRECT ANSWER: {request.correct_answer}
    TEXTBOOK CONTEXT: {request.context[:2000] if request.context else "Not provided"}

    TASK: Explain to a middle school student why their answer was incorrect.
    """
    res = await orchestrator.generate(prompt, task_type="simple")
    return {"explanation": res["response"]}

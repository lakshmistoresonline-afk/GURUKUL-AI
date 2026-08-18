import os
import json
import random
import logging
from fastapi import APIRouter, HTTPException, Query, Body, Depends
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..utils.ai_utils import normalize_structured_response
from ..services.mastery_service import MasteryService
from ..services.diagnostic_service import DiagnosticService
from ..services.question_bank_service import QuestionBankService
from ..config.app_config import settings
from ..utils.security import get_authorized_class, validate_chapter_access
from ..utils.package_adapter import PackageAdapter
from ..utils.auth import get_current_user, AuthUser

from ..services.srs_service import SRSService
from ..services.resource_service import ResourceService

logger = logging.getLogger(__name__)
router = APIRouter()
orchestrator = AIOrchestrator()
mastery_service = MasteryService()
resource_service = ResourceService(orchestrator)
srs_service = SRSService(resource_service.AsyncSession)
diagnostic_service = DiagnosticService(mastery_service)
try:
    question_bank_service = QuestionBankService()
except Exception as e:
    logger.error(f"Failed to initialize QuestionBankService: {e}")
    question_bank_service = None

class GenerateQuestionsRequest(BaseModel):
    class_name: str
    subject: str
    chapter_id: str
    count: int = 5
    difficulty: Optional[str] = "Medium"

def _format_q_for_quiz(q: Dict[str, Any]) -> Dict[str, Any]:
    """Ensures question format is consistent for the frontend."""
    q_type = q.get("type", "mcq").lower().replace("-", "_")
    if q_type == "fill_blank": q_type = "fill_blanks"

    return {
        "id": q.get("id"),
        "type": q_type,
        "question": q.get("question"),
        "options": q.get("options", []),
        "correctAnswer": str(q.get("answer", q.get("correctAnswer", ""))),
        "explanation": q.get("explanation", ""),
        "difficulty": q.get("level", q.get("difficulty", "medium")).capitalize()
    }

@router.get("/bank/stats")
async def get_bank_stats(user: AuthUser = Depends(get_current_user)):
    """Returns statistics about the current question bank for the user's class."""
    if not question_bank_service:
        raise HTTPException(status_code=503, detail="Question Bank Service unavailable")

    stats = question_bank_service.get_stats()
    return stats

@router.post("/generate-dynamic")
async def generate_dynamic_questions(
    request: GenerateQuestionsRequest,
    user: AuthUser = Depends(get_current_user)
):
    """Fallback dynamic question generation with verified class authorization."""
    authorized_class = await get_authorized_class(user, request.class_name)
    validate_chapter_access(request.chapter_id, authorized_class)

    package_path = os.path.join("./storage/output", authorized_class, request.subject, request.chapter_id, "package.json")
    if not os.path.exists(package_path):
         raise HTTPException(status_code=404, detail="Chapter package not found.")

    with open(package_path, "r", encoding="utf-8") as f:
        package = PackageAdapter.adapt(json.load(f))
        is_final = package.get("metadata", {}).get("is_final_content", True) # Default True for adapted
        original_data = package.get("original_data")

    if is_final and original_data:
        bank = original_data.get("assessment", {}).get("expandedQuestionBank", [])
        if not bank: bank = package.get("content", {}).get("quiz", [])

        if bank:
            diff_map = {"easy": ["foundation"], "medium": ["application"], "hard": ["mastery", "challenge", "hots"]}
            target_levels = diff_map.get(request.difficulty.lower(), ["application"])
            filtered = [q for q in bank if q.get("level", q.get("difficulty", "")).lower() in target_levels]
            if not filtered: filtered = bank

            selection = random.sample(filtered, min(len(filtered), request.count))
            return [{"id": q.get("id"), "question": q.get("question"), "options": q.get("options", []),
                     "correctAnswer": str(q.get("answer", q.get("correctAnswer", ""))), "explanation": q.get("explanation", ""),
                     "type": q.get("type", "mcq").replace("-", "_")} for q in selection]

    raise HTTPException(status_code=400, detail="Dynamic generation disabled.")

@router.get("/diagnostic/{class_name}/{subject}/{chapter_id}")
async def get_diagnostic(
    class_name: str,
    subject: str,
    chapter_id: str,
    user: AuthUser = Depends(get_current_user)
):
    """Returns Existing items for pre-chapter diagnostic with verified class authorization."""
    authorized_class = await get_authorized_class(user, class_name)
    validate_chapter_access(chapter_id, authorized_class)

    if not getattr(settings, "ADAPTIVE_MASTERY_DIAGNOSTIC", True):
        raise HTTPException(status_code=403, detail="Diagnostic feature is disabled.")

    questions = diagnostic_service.get_diagnostic_questions(authorized_class, subject, chapter_id)
    if not questions:
        raise HTTPException(status_code=404, detail="No diagnostic items found.")
    return questions

class DiagnosticResultsRequest(BaseModel):
    class_name: str
    subject: str
    chapter_id: str
    results: List[Dict[str, Any]] # question_id, is_correct, concept_id

@router.post("/process-diagnostic")
async def process_diagnostic_results(
    request: DiagnosticResultsRequest,
    user: AuthUser = Depends(get_current_user)
):
    """
    Processes diagnostic results with verified class and identity authorization.
    Diagnostic results generate signals but DO NOT mark mastery.
    """
    authorized_class = await get_authorized_class(user, request.class_name)
    validate_chapter_access(request.chapter_id, authorized_class)

    signals = {}
    for res in request.results:
        c_id = res.get("concept_id")
        if not c_id: continue

        is_correct = res.get("is_correct")
        is_prereq = res.get("is_prereq", False)

        sig_key = c_id
        if is_prereq: sig_key = f"PREREQ_{c_id}"

        if sig_key not in signals:
            signals[sig_key] = {"count": 0, "correct": 0, "type": "PREREQUISITE_GAP" if is_prereq else "CORE"}

        signals[sig_key]["count"] += 1
        if is_correct: signals[sig_key]["correct"] += 1

    final_signals = {}
    for key, stats in signals.items():
        ratio = stats["correct"] / stats["count"]

        if stats["type"] == "PREREQUISITE_GAP":
            if ratio < 0.6: final_signals[key] = "PREREQUISITE_GAP"
            else: final_signals[key] = "STRONG"
        else:
            if ratio >= 0.8: final_signals[key] = "STRONG"
            elif ratio >= 0.5: final_signals[key] = "DEVELOPING"
            else: final_signals[key] = "UNKNOWN"

    logger.info(f"Diagnostic results processed for UID {user.uid}, Chapter {request.chapter_id}")

    return {
        "chapter_id": request.chapter_id,
        "concept_signals": final_signals,
        "recommendation": "PERSONALIZED_PATH_GENERATED"
    }

@router.get("/session")
async def get_quiz_session(
    type: str = Query("quick"),
    classId: Optional[int] = Query(None),
    subject: Optional[str] = Query(None),
    chapterId: Optional[str] = Query(None),
    conceptId: Optional[str] = Query(None),
    count: int = Query(10),
    user: AuthUser = Depends(get_current_user)
):
    """Generates a smart quiz session."""
    # Use requested class if provided, otherwise user default
    authorized_class = f"class_{classId}" if classId else user.class_name

    if chapterId:
        validate_chapter_access(chapterId, authorized_class)

    # Priority: If chapterId is provided, attempt to get questions from that chapter's package
    if chapterId:
        config = mastery_service.get_chapter_mastery_config(authorized_class, subject or "", chapterId)
        if config:
            # Support both 'concepts' and 'mappings'
            concepts = config.get("concepts") or config.get("mappings") or []

            if conceptId:
                qs = mastery_service.get_questions_for_concept(authorized_class, subject or "", chapterId, conceptId, limit=count)
                if qs: return [_format_q_for_quiz(q) for q in qs]

            # Fallback to all questions in chapter
            all_qs = []
            # Option 1: Via concepts
            for concept in concepts:
                c_id = concept.get("conceptId") or concept.get("concept_id") or concept.get("id")
                if c_id:
                    all_qs.extend(mastery_service.get_questions_for_concept(authorized_class, subject or "", chapterId, c_id, limit=3))

            # Option 2: Direct from package if concepts method failed
            if not all_qs:
                package = mastery_service.get_chapter_mastery_config(authorized_class, subject or "", chapterId)
                if package and "content" in package and "quiz" in package["content"]:
                     all_qs = package["content"]["quiz"]
                elif package and "original_data" in package:
                     all_qs = package.get("original_data", {}).get("assessment", {}).get("expandedQuestionBank", [])

            if all_qs:
                # Remove duplicates by ID
                unique_qs = {str(q.get('id')): q for q in all_qs if q.get('id')}.values()
                selection = random.sample(list(unique_qs), min(len(unique_qs), count))
                return [_format_q_for_quiz(q) for q in selection]

    if not question_bank_service:
        raise HTTPException(status_code=503, detail="Question Bank Service unavailable and chapter package questions not found")

    return question_bank_service.get_questions(
        class_id=int(authorized_class.split('_')[1]),
        subject=subject,
        chapter_id=chapterId,
        concept_id=conceptId,
        limit=min(count, 50)
    )

@router.post("/interleaved")
async def get_interleaved_practice(
    class_name: str = Body(...),
    subject: str = Body(...),
    count: int = Body(10),
    student_mastery: List[Dict[str, Any]] = Body(...),
    user: AuthUser = Depends(get_current_user)
):
    """
    Returns a mix of questions with verified class and identity authorization.
    """
    authorized_class = await get_authorized_class(user, class_name)

    if settings.ADAPTIVE_MASTERY_INTERLEAVING == "OFF":
        raise HTTPException(status_code=403, detail="Interleaving is disabled.")

    graph_path = os.path.join(settings.STORAGE_PATH, "concept_graph.json")
    if not os.path.exists(graph_path):
        raise HTTPException(status_code=500, detail="Concept graph missing")

    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)

    due_items = await srs_service.get_due_items(user.uid, content_type='concept', limit=5)
    priority_guids = [i['content_id'] for i in due_items]

    for record in student_mastery:
        chapter_id = record.get("chapterId")
        config = mastery_service.get_chapter_mastery_config(authorized_class, subject, chapter_id)
        if config:
            concepts = config.get("concepts") or config.get("mappings") or []
            weak_local_ids = mastery_service.identify_weak_concepts(record, concepts)
            chap_context = config.get('source', {}).get('slug') or config.get('source', {}).get('chapterTitle') or chapter_id
            for lcid in weak_local_ids:
                guid = f"{authorized_class}_{subject}_{chap_context}_{lcid}".lower().replace(" ", "-")
                if guid not in priority_guids:
                    priority_guids.append(guid)

    interleaved_questions = []
    target_guids = list(set(priority_guids))[:5]

    for guid in target_guids:
        node = graph["concepts"].get(guid)
        if not node: continue

        qs = mastery_service.get_questions_for_concept(
            node["class"], node["subject"], node["chapterId"], node["localId"], limit=2
        )
        for q in qs:
            interleaved_questions.append(_format_q_for_quiz(q))

    random.shuffle(interleaved_questions)
    return interleaved_questions[:count]

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import os
import json
import random
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..utils.security import get_authorized_class, validate_chapter_access
from ..utils.package_adapter import PackageAdapter
from ..utils.auth import get_current_user, AuthUser

from ..services.feynman_service import FeynmanService, FeynmanLevel

router = APIRouter()
orchestrator = AIOrchestrator()
feynman_service = FeynmanService(orchestrator)

class FeynmanChallengeRequest(BaseModel):
    class_name: str
    subject: str
    chapter_id: str
    level: Optional[int] = 1

class FeynmanEvaluateRequest(BaseModel):
    class_name: str
    subject: str
    chapter_id: str
    concept: str
    explanation: str
    level: Optional[int] = 1

@router.post("/challenge")
async def get_feynman_challenge(
    request: FeynmanChallengeRequest,
    user: AuthUser = Depends(get_current_user)
):
    """
    Generate an adaptive Feynman challenge with verified class authorization.
    """
    authorized_class = await get_authorized_class(user, request.class_name)
    validate_chapter_access(request.chapter_id, authorized_class)

    from ..utils.path_resolver import PathResolver
    master_path = PathResolver.get_chapter_path(request.class_name, request.chapter_id, subject=request.subject)
    package = None

    if master_path:
        pkg_path = os.path.join(master_path, "package.json")
        if os.path.exists(pkg_path):
            with open(pkg_path, "r", encoding="utf-8") as f:
                package = PackageAdapter.adapt(json.load(f))

    if not package:
        package_path = os.path.join("./storage/output", authorized_class, request.subject, request.chapter_id, "package.json")
        if os.path.exists(package_path):
            with open(package_path, "r", encoding="utf-8") as f:
                package = PackageAdapter.adapt(json.load(f))

    if not package:
         raise HTTPException(status_code=404, detail="Chapter not found.")

    try:
        raw_concepts = package.get("content", {}).get("concepts", [])

        if isinstance(raw_concepts, str):
            concepts = [c.strip() for c in raw_concepts.split('\n') if c.strip()]
        else:
            concepts = raw_concepts

        if not isinstance(concepts, list) or len(concepts) == 0:
            context = package.get("content", {}).get("teacher_explanation", "")
            prompt = f"Identify 3 key technical terms from this text:\n\n{context[:2000]}\n\nReturn only a comma-separated list."
            res = await orchestrator.generate(prompt, task_type="simple")
            concepts = [c.strip() for c in res["response"].split(",")]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error generating challenge.")

    concept_item = random.choice(concepts)
    concept_name = concept_item.get("term") if isinstance(concept_item, dict) else (concept_item.get("name") if isinstance(concept_item, dict) else concept_item)

    return await feynman_service.get_challenge(concept_name, request.level)

@router.post("/evaluate")
async def evaluate_feynman_explanation(
    request: FeynmanEvaluateRequest,
    user: AuthUser = Depends(get_current_user)
):
    """
    Evaluate the student's simplified explanation with verified class authorization.
    """
    authorized_class = await get_authorized_class(user, request.class_name)
    validate_chapter_access(request.chapter_id, authorized_class)

    from ..utils.path_resolver import PathResolver
    master_path = PathResolver.get_chapter_path(request.class_name, request.chapter_id, subject=request.subject)
    package = None

    if master_path:
        pkg_path = os.path.join(master_path, "package.json")
        if os.path.exists(pkg_path):
            with open(pkg_path, "r", encoding="utf-8") as f:
                package = PackageAdapter.adapt(json.load(f))

    if not package:
        package_path = os.path.join("./storage/output", authorized_class, request.subject, request.chapter_id, "package.json")
        if os.path.exists(package_path):
            with open(package_path, "r", encoding="utf-8") as f:
                package = PackageAdapter.adapt(json.load(f))

    if not package:
         raise HTTPException(status_code=404, detail="Chapter not found.")

    formal_context = package.get("content", {}).get("teacher_explanation", "")

    return await feynman_service.evaluate(request.concept, request.explanation, formal_context, request.level)

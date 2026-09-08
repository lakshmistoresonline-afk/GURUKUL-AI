from fastapi import APIRouter, Depends, HTTPException, status, Query
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from ...core.utils.auth import get_current_student
from ...data.repositories.database.orm_models import UserORM

router = APIRouter(prefix="/api/v1/student", tags=["Student Dashboard"])

RUNTIME_ROOT = Path("D:/GURUKUL-AI/runtime-data")

# Global Search Index
SEARCH_INDEX = []
INDEX_PATH = RUNTIME_ROOT / "search" / "index.json"
if INDEX_PATH.exists():
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            SEARCH_INDEX = json.load(f)
    except Exception as e:
        print(f"Error loading search index: {e}")

# --- HELPERS ---

def load_catalog() -> Dict[str, Any]:
    catalog_path = RUNTIME_ROOT / "catalog.json"
    if not catalog_path.exists():
        return {"classes": []}
    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_chapter(class_name: str, subject_name: str, chapter_id: str) -> Dict[str, Any]:
    chapter_path = RUNTIME_ROOT / "chapters" / class_name / subject_name / f"{chapter_id}.json"
    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_id} not found in {class_name}/{subject_name}")
    with open(chapter_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_class_name_by_id(class_id: str, catalog: Dict[str, Any]) -> str:
    for cls in catalog["classes"]:
        if cls["id"] == class_id:
            return cls["name"]
    return None

def get_subject_name_by_id(class_id: str, subject_id: str, catalog: Dict[str, Any]) -> str:
    for cls in catalog["classes"]:
        if cls["id"] == class_id:
            for subj in cls["subjects"]:
                if subj["id"] == subject_id:
                    return subj["name"]
    return None

# --- API ROUTES ---

@router.get("/catalog")
async def get_catalog():
    return load_catalog()

@router.get("/classes")
async def get_classes():
    catalog = load_catalog()
    return catalog["classes"]

@router.get("/classes/{class_id}")
async def get_class(class_id: str):
    catalog = load_catalog()
    for cls in catalog["classes"]:
        if cls["id"] == class_id:
            return cls
    raise HTTPException(status_code=404, detail="Class not found")

@router.get("/classes/{class_id}/subjects")
async def get_class_subjects(class_id: str):
    cls = await get_class(class_id)
    return cls["subjects"]

@router.get("/subjects/{subject_id}")
async def get_subject(subject_id: str):
    catalog = load_catalog()
    for cls in catalog["classes"]:
        for subj in cls["subjects"]:
            if subj["id"] == subject_id:
                return subj
    raise HTTPException(status_code=404, detail="Subject not found")

@router.get("/subjects/{subject_id}/chapters")
async def get_subject_chapters(subject_id: str):
    subj = await get_subject(subject_id)
    return subj["chapters"]

@router.get("/chapters/{chapter_uid}")
async def get_chapter_summary(chapter_uid: str):
    # chapter_uid is class_subject_id (e.g. class_5_english_101)
    # But in catalog, we have it. Let's find it.
    catalog = load_catalog()
    for cls in catalog["classes"]:
        for subj in cls["subjects"]:
            for ch in subj["chapters"]:
                if ch["id"] == chapter_uid:
                    return ch
    raise HTTPException(status_code=404, detail="Chapter not found")

@router.get("/chapters/{chapter_uid}/full")
async def get_chapter_full(chapter_uid: str):
    catalog = load_catalog()
    for cls in catalog["classes"]:
        for subj in cls["subjects"]:
            for ch in subj["chapters"]:
                if ch["id"] == chapter_uid:
                    return load_chapter(cls["name"], subj["name"], ch["chapter_id"])
    raise HTTPException(status_code=404, detail="Chapter not found")

@router.get("/chapters/{chapter_uid}/{layer}")
async def get_chapter_layer(chapter_uid: str, layer: str):
    if layer not in ["learn", "practice", "assess", "revise", "resources", "traceability"]:
        raise HTTPException(status_code=400, detail="Invalid layer")

    full = await get_chapter_full(chapter_uid)
    return {
        "metadata": {
            "id": full["id"],
            "title": full["title"],
            "classId": full["classId"],
            "subjectId": full["subjectId"]
        },
        "items": full.get(layer, [])
    }

@router.get("/search")
async def search_content(q: str = Query(..., min_length=2), classId: Optional[str] = None):
    results = []
    query = q.lower()

    # Use cached index
    for item in SEARCH_INDEX:
        if classId and item["class"].lower().replace(" ", "_") != classId:
            continue

        if query in str(item.get("title", "")).lower() or query in str(item.get("text", "")).lower():
            results.append(item)

    return results[:50] # Limit to 50 results

@router.get("/dashboard/summary")
async def get_dashboard_summary():
    catalog = load_catalog()
    class_counts = {cls["name"]: len(cls["subjects"]) for cls in catalog["classes"]}
    return {
        "status": "Gurukul AI Unified API v4.0",
        "classes": class_counts
    }

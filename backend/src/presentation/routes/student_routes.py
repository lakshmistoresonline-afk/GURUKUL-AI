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

def load_search_index():
    global SEARCH_INDEX
    if INDEX_PATH.exists():
        try:
            with open(INDEX_PATH, "r", encoding="utf-8") as f:
                _search_data = json.load(f)
                SEARCH_INDEX = _search_data.get("records", []) if isinstance(_search_data, dict) else _search_data
        except Exception as e:
            print(f"Error loading search index: {e}")

load_search_index()

# --- HELPERS ---

def load_catalog() -> Dict[str, Any]:
    catalog_path = RUNTIME_ROOT / "catalog.json"
    if not catalog_path.exists():
        return {"classes": []}
    with open(catalog_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_chapter(class_id: str, subject_id: str, chapter_id: str) -> Dict[str, Any]:
    chapter_path = RUNTIME_ROOT / "chapters" / class_id / subject_id / f"{chapter_id}.json"
    if not chapter_path.exists():
        raise HTTPException(status_code=404, detail=f"Chapter {chapter_id} not found in {class_id}/{subject_id}")
    with open(chapter_path, "r", encoding="utf-8") as f:
        return json.load(f)

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
                    return load_chapter(cls["id"], subj["id"], ch["chapter_id"])
    raise HTTPException(status_code=404, detail="Chapter not found")

@router.get("/chapters/{chapter_uid}/{layer}")
async def get_chapter_layer(chapter_uid: str, layer: str):
    if layer not in ["learn", "practice", "assess", "revise", "resources", "traceability"]:
        raise HTTPException(status_code=400, detail="Invalid layer")

    full = await get_chapter_full(chapter_uid)
    return {
        "metadata": {
            "id": full["id"],
            "title": full.get("title") or full.get("chapter_title"),
            "classId": full.get("classId") or full.get("class_id"),
            "subjectId": full.get("subjectId") or full.get("subject_id")
        },
        "items": full.get(layer, [])
    }

@router.get("/search")
async def search_content(q: str = Query(..., min_length=2), classId: Optional[str] = None):
    results = []
    query = q.lower()

    # Refresh search index if it was empty (e.g. initial load failed or was empty)
    if not SEARCH_INDEX:
        load_search_index()

    for item in SEARCH_INDEX:
        if classId and item["class_id"] != classId:
            continue

        if query in str(item.get("chapter_title", "")).lower() or query in str(item.get("text", "")).lower():
            results.append(item)

    return results[:50]

@router.get("/dashboard/summary")
async def get_dashboard_summary():
    catalog = load_catalog()
    class_counts = {cls["name"]: len(cls["subjects"]) for cls in catalog["classes"]}
    return {
        "status": "Gurukul AI Unified API v5.0",
        "classes": class_counts,
        "total_classes": len(catalog["classes"])
    }

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

try:
    from ..services.content_loader import ContentLoaderService
except (ImportError, ValueError):
    from src.services.content_loader import ContentLoaderService

router = APIRouter(prefix="/api/v1", tags=["Universal Content Pipeline"])

@router.get("/classes")
async def discover_classes():
    grades = ContentLoaderService.discover_grades()
    class_list = []
    for g in grades:
        subjects = ContentLoaderService.discover_subjects(g)
        class_list.append({"grade": g, "subjects": subjects})
    return class_list

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    subjects = ContentLoaderService.discover_subjects(grade)
    return {"grade": grade, "subjects": subjects}

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    meta = ContentLoaderService.get_subject_curriculum_metadata(grade, subject)
    units_list = meta.get("units", [])
    total_chapters = sum(len(u.get("chapters", [])) for u in units_list)

    return {
        "grade": grade,
        "subject": subject,
        "curriculumFramework": meta.get("curriculumFramework", "NEP 2020 & NCF-SE 2023"),
        "curricularGoals": meta.get("curricularGoals", []),
        "totalChapters": total_chapters,
        "units": units_list
    }

@router.get("/chapters/{chapterId}")
async def get_chapter_details(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    data = ContentLoaderService.load_chapter_source(grade, subject, chapterId)
    if not data:
        raise HTTPException(status_code=404, detail=f"Chapter {chapterId} not found in Class {grade} {subject}")

    ch_title = data.get("chapterTitle") or data.get("title") or chapterId

    return {
        "chapterId": chapterId,
        "grade": grade,
        "subject": subject,
        "chapterNumber": data.get("chapterNumber", 1),
        "title": ch_title,
        "chapterTitle": ch_title,
        "unitTitle": data.get("unitTitle", ""),
        "unitNumber": data.get("unitNumber", 1)
    }

@router.get("/chapters/{chapterId}/source")
async def get_chapter_direct_source(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    """
    DIRECT SOURCE ENDPOINT:
    Loads authoritative source JSON directly without AdapterResolver, parse_chapter, ContentBlock, or manifest.
    Returns the exact 7 fixed application sections:
    - overview (null / empty state)
    - notes (from Notes.json)
    - master (from Master.json)
    - flashcards (from Flashcards.json)
    - mindmaps (from Mindmaps.json)
    - quiz (from Quiz.json)
    - question_papers (null / empty state)
    """
    raw_source = ContentLoaderService.load_chapter_source(grade, subject, chapterId)
    if not raw_source:
        raise HTTPException(status_code=404, detail=f"Chapter {chapterId} source not found")

    # Extract section-specific source payloads directly from raw_source bundle
    sections = {
        "overview": None,
        "notes": raw_source.get("notes") or raw_source.get("notesData") or raw_source,
        "master": raw_source.get("master") or raw_source.get("masterData") or raw_source,
        "flashcards": raw_source.get("flashcards") or [],
        "mindmaps": raw_source.get("mindmap") or raw_source.get("mindmaps") or {},
        "quiz": raw_source.get("quiz") or [],
        "question_papers": None
    }

    return {
        "chapterId": chapterId,
        "grade": grade,
        "subject": subject,
        "chapterNumber": raw_source.get("chapterNumber", 1),
        "chapterTitle": raw_source.get("chapterTitle") or raw_source.get("title") or chapterId,
        "unitTitle": raw_source.get("unitTitle", ""),
        "sections": sections
    }

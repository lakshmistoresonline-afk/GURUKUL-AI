from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

try:
    from ..services.content_loader import ContentLoaderService
    from ..adapters.adapter_resolver import AdapterResolver
    from ..navigation.navigation_builder import BackendNavigationBuilder
except (ImportError, ValueError):
    from src.services.content_loader import ContentLoaderService
    from src.adapters.adapter_resolver import AdapterResolver
    from src.navigation.navigation_builder import BackendNavigationBuilder

router = APIRouter(prefix="/api/v1", tags=["Universal Content Pipeline"])

@router.get("/classes")
async def discover_classes():
    """
    Universal discovery API: Discovers available grades and subjects dynamically from CONTENT_ROOT.
    """
    grades = ContentLoaderService.discover_grades()
    class_list = []
    for g in grades:
        subjects = ContentLoaderService.discover_subjects(g)
        class_list.append({"grade": g, "subjects": subjects})
    return class_list

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    """
    Universal discovery API: Returns list of subjects available for a grade.
    """
    subjects = ContentLoaderService.discover_subjects(grade)
    return {"grade": grade, "subjects": subjects}

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    """
    Universal subject details API: Returns subject metadata including
    curriculum framework, 4 curricular goals, unit themes, and chapter list for ANY subject.
    """
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
    """
    Universal chapter details API: Returns chapter metadata and manifest summary.
    """
    data = ContentLoaderService.load_chapter_source(grade, subject, chapterId)
    if not data:
        raise HTTPException(status_code=404, detail=f"Chapter {chapterId} not found in Class {grade} {subject}")

    adapter = AdapterResolver.resolve("NCERT", grade, subject, data)
    blocks = adapter.parse_chapter(data, chapterId)
    manifest = adapter.generate_manifest(chapterId, blocks)

    ch_title = data.get("chapterTitle") or data.get("title") or chapterId

    return {
        "chapterId": chapterId,
        "grade": grade,
        "subject": subject,
        "chapterNumber": data.get("chapterNumber", 1),
        "title": ch_title,
        "chapterTitle": ch_title,
        "unitTitle": data.get("unitTitle", ""),
        "unitNumber": data.get("unitNumber", 1),
        "blockCount": len(blocks),
        "manifest": manifest
    }

@router.get("/chapters/{chapterId}/manifest")
async def get_chapter_manifest(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    """
    Universal manifest API: Generates and returns ContentManifest for chapter.
    """
    data = ContentLoaderService.load_chapter_source(grade, subject, chapterId)
    if not data:
        raise HTTPException(status_code=404, detail=f"Chapter {chapterId} not found")

    adapter = AdapterResolver.resolve("NCERT", grade, subject, data)
    blocks = adapter.parse_chapter(data, chapterId)
    manifest = adapter.generate_manifest(chapterId, blocks)

    return manifest

@router.get("/chapters/{chapterId}/navigation")
async def get_chapter_navigation(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    """
    Universal navigation API: Generates server-side navigation tabs with Quiz ALWAYS last (order 60).
    """
    data = ContentLoaderService.load_chapter_source(grade, subject, chapterId)
    if not data:
        raise HTTPException(status_code=404, detail=f"Chapter {chapterId} not found")

    adapter = AdapterResolver.resolve("NCERT", grade, subject, data)
    blocks = adapter.parse_chapter(data, chapterId)
    manifest = adapter.generate_manifest(chapterId, blocks)

    tabs = BackendNavigationBuilder.build_navigation(subject, manifest)
    return {"chapterId": chapterId, "subject": subject, "tabs": tabs}

@router.get("/chapters/{chapterId}/content")
async def get_chapter_content(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    """
    Universal content API: Returns list of normalized ContentBlock items.
    """
    data = ContentLoaderService.load_chapter_source(grade, subject, chapterId)
    if not data:
        raise HTTPException(status_code=404, detail=f"Chapter {chapterId} not found")

    adapter = AdapterResolver.resolve("NCERT", grade, subject, data)
    blocks = adapter.parse_chapter(data, chapterId)

    return blocks

@router.get("/chapters/{chapterId}/content/{contentType}")
async def get_chapter_content_by_type(
    chapterId: str,
    contentType: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    """
    Universal isolated content API: Returns ContentBlock items filtered by semantic contentType.
    """
    data = ContentLoaderService.load_chapter_source(grade, subject, chapterId)
    if not data:
        raise HTTPException(status_code=404, detail=f"Chapter {chapterId} not found")

    adapter = AdapterResolver.resolve("NCERT", grade, subject, data)
    blocks = adapter.parse_chapter(data, chapterId)

    filtered = [
        b for b in blocks
        if b.normalizedType == contentType or b.sourceType == contentType or b.renderer == contentType
    ]

    return filtered

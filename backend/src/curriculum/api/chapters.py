import os
import json
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Dict, Any, List, Optional
from ..core.curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from ..core.curriculum_registry import CurriculumRegistry
from ..core.subject_registry import SubjectRegistry
from ..core.processed_content_resolver import ProcessedContentResolver, ContentIntegrityError, ContentNotFoundError, ChapterNotFoundError as ResolverChapterNotFoundError
from ..core.content_validator import ContentNotFoundError, ContentSchemaError, IdentityConflictError, ChapterNotFoundError

router = APIRouter(prefix="/api/v1", tags=["Hardened Authoritative Curriculum Pipeline"])

PROCESSED_ROOT = r"D:/GURUKUL/ProcessedContent"

@router.get("/classes")
async def discover_classes():
    grades = CurriculumRegistry.get_classes()
    class_list = []
    for g in grades:
        subs = CurriculumRegistry.get_subjects(g)
        class_list.append({"grade": g, "subjects": subs})
    return class_list

@router.get("/curriculum/classes")
async def discover_classes_alias():
    return await discover_classes()

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    subjects = CurriculumRegistry.get_subjects(grade)
    return {"grade": grade, "subjects": subjects}

@router.get("/curriculum/classes/{grade}/subjects")
async def get_grade_subjects_alias(grade: str):
    return await get_grade_subjects(grade)

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject.replace(" ", ""))
    chapters = []

    if os.path.exists(sub_processed_dir):
        ch_dirs = sorted([d for d in os.listdir(sub_processed_dir) if os.path.isdir(os.path.join(sub_processed_dir, d))])
        for idx, ch_id in enumerate(ch_dirs):
            ch_dir = os.path.join(sub_processed_dir, ch_id)
            ch_title = ch_id

            for sec in ["overview", "notes", "master"]:
                sec_path = os.path.join(ch_dir, f"{sec}.json")
                if os.path.exists(sec_path):
                    try:
                        with open(sec_path, "r", encoding="utf-8") as f:
                            d = json.load(f)
                            if isinstance(d, dict):
                                title = (
                                    d.get("chapterTitle") or
                                    d.get("chapter_title") or
                                    d.get("title") or
                                    (isinstance(d.get("overview"), dict) and (d["overview"].get("chapter_title") or d["overview"].get("title")))
                                )
                                if title and isinstance(title, str) and "Exhaustive" not in title:
                                    ch_title = title
                                    break
                    except Exception:
                        pass

            c_num = idx + 1
            if "C" in ch_id:
                try:
                    c_num = int(ch_id.split("C")[-1])
                except ValueError:
                    pass
            chapters.append({
                "id": ch_id,
                "chapterNumber": c_num,
                "title": ch_title
            })

    return {
        "grade": grade,
        "subject": subject,
        "curriculumFramework": "NEP 2020 & NCF-SE 2023",
        "curricularGoals": [],
        "totalChapters": len(chapters),
        "units": [
            {
                "id": "U01",
                "unitNumber": 1,
                "title": f"{subject} Curriculum Unit",
                "chapters": chapters
            }
        ]
    }

@router.get("/curriculum/resolve")
async def resolve_authoritative_content(
    grade: str = Query(..., description="Grade/Class"),
    subject: str = Query(..., description="Subject ID"),
    book: str = Query(..., description="Book identifier"),
    unit: str = Query(..., description="Unit identifier"),
    chapter_id: str = Query(..., description="Exact chapter ID"),
    content_type: str = Query(..., description="Content type")
):
    try:
        identity = CurriculumIdentity(
            grade=str(grade),
            subject=SubjectRegistry.resolve_canonical_subject(subject),
            book=book,
            part="none",
            unit=unit,
            chapter_id=chapter_id,
            content_type=content_type
        )
    except Exception as ve:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_CURRICULUM_IDENTITY",
                    "message": f"Malformed or missing identity parameters: {str(ve)}"
                }
            }
        )

    try:
        content_data = ProcessedContentResolver.resolve_content(identity)
    except (ChapterNotFoundError, ResolverChapterNotFoundError) as cnf:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "CHAPTER_NOT_FOUND",
                    "message": str(cnf),
                    "identity": identity.model_dump()
                }
            }
        )
    except ContentNotFoundError as cnf_type:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "CONTENT_TYPE_NOT_FOUND",
                    "message": str(cnf_type),
                    "identity": identity.model_dump()
                }
            }
        )
    except IdentityConflictError as ice:
        raise HTTPException(
            status_code=409,
            detail={
                "error": {
                    "code": "IDENTITY_CONFLICT",
                    "message": str(ice),
                    "identity": identity.model_dump()
                }
            }
        )
    except ContentSchemaError as cse:
        raise HTTPException(
            status_code=422,
            detail={
                "error": {
                    "code": "CONTENT_SCHEMA_INVALID",
                    "message": str(cse),
                    "identity": identity.model_dump()
                }
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": str(exc),
                    "identity": identity.model_dump()
                }
            }
        )

    return {
        "identity": identity.model_dump(),
        "contentType": content_type,
        "data": content_data,
        "status": "READY"
    }

@router.get("/chapters/{chapterId}/source")
async def get_chapter_direct_source_v2(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English"),
    book: str = Query(default="main"),
    unit: str = Query(default="U01")
):
    try:
        identity = CurriculumIdentity(
            grade=str(grade),
            subject=SubjectRegistry.resolve_canonical_subject(subject),
            book=book,
            part="none",
            unit=unit,
            chapter_id=chapterId,
            content_type="overview"
        )
        dto: ChapterRuntimeDTO = CurriculumRegistry.load_chapter_bundle(identity)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "CHAPTER_NOT_FOUND",
                    "message": str(e)
                }
            }
        )

    return {
        "chapterId": chapterId,
        "grade": grade,
        "subject": subject,
        "book": book,
        "unit": unit,
        "chapterNumber": dto.chapter_number,
        "chapterTitle": dto.chapter_title,
        "unitTitle": dto.unit_title,
        "unitNumber": 1,
        "sections": dto.data,
        "runtimeIdentity": dto.identity.model_dump()
    }

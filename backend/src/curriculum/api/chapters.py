import os
import json
from fastapi import APIRouter, HTTPException, Query, Path
from typing import Dict, Any, List, Optional
from ..core.curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from ..core.curriculum_registry import CurriculumRegistry, CurriculumResolutionError
from ..core.subject_registry import SubjectRegistry
from ..core.processed_content_resolver import ProcessedContentResolver, ChapterNotFoundError as ResolverChapterNotFoundError
from ..core.content_validator import ContentNotFoundError, ContentSchemaError, IdentityConflictError, ChapterNotFoundError
from ..core.config import GurukulConfig

router = APIRouter(prefix="/api/v1", tags=["Hardened Authoritative Curriculum Pipeline"])

PROCESSED_ROOT = str(GurukulConfig.get_processed_root())

@router.options("/classes")
@router.options("/curriculum/classes")
async def classes_options():
    return {}

@router.get("/curriculum/hierarchy")
@router.get("/classes")
async def get_curriculum_hierarchy():
    """
    Returns the complete, dynamic, authoritative curriculum hierarchy:
    Class → Subject → Book → Part → Unit → Chapter → Content Types.
    Derived purely from repository manifests without hardcoded catalogs.
    """
    tax = CurriculumRegistry.get_taxonomy()
    hierarchy = []

    for grade, subjects in sorted(tax.items()):
        grade_entry = {
            "grade": grade,
            "subjects": []
        }
        for subj_key, books_dict in subjects.items():
            display_subj = SubjectRegistry.get_display_name(subj_key)
            books_list = []
            for book_id, book_data in books_dict.items():
                part_id = book_data.get("part", "none")
                units_dict = book_data.get("units", {})
                units_list = []
                for unit_id, ch_ids in units_dict.items():
                    chapters_list = []
                    for ch_id in ch_ids:
                        try:
                            node = CurriculumRegistry.get_index().get(f"{grade}:{subj_key}:{book_id}:{part_id}:{unit_id}:{ch_id}")
                            if node:
                                chapters_list.append({
                                    "chapter_id": ch_id,
                                    "chapter_number": node["chapter_number"],
                                    "chapter_title": node["chapter_title"],
                                    "content_types": node["available_content_types"]
                                })
                            else:
                                chapters_list.append({
                                    "chapter_id": ch_id,
                                    "chapter_number": 1,
                                    "chapter_title": ch_id,
                                    "content_types": ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]
                                })
                        except:
                            chapters_list.append({
                                "chapter_id": ch_id,
                                "chapter_number": 1,
                                "chapter_title": ch_id,
                                "content_types": ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]
                            })

                    units_list.append({
                        "unit_id": unit_id,
                        "unit_number": 1,
                        "unit_title": f"Unit {unit_id.replace('U', '')}",
                        "chapters": chapters_list
                    })

                books_list.append({
                    "book_id": book_id,
                    "part": part_id,
                    "units": units_list
                })

            grade_entry["subjects"].append({
                "subject": display_subj,
                "canonical_subject": subj_key,
                "books": books_list
            })
        hierarchy.append(grade_entry)

    return hierarchy

@router.get("/classes/{grade}/subjects")
@router.get("/curriculum/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    subjects = CurriculumRegistry.get_subjects(grade)
    return {"grade": grade, "subjects": subjects}

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
    except (ChapterNotFoundError, ResolverChapterNotFoundError, CurriculumResolutionError) as cnf:
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
    canonical_subj = SubjectRegistry.resolve_canonical_subject(subject)
    identity = CurriculumIdentity(
        grade=str(grade),
        subject=canonical_subj,
        book=book,
        part="none",
        unit=unit,
        chapter_id=chapterId,
        content_type="overview"
    )

    try:
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

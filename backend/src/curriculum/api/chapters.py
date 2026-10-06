import os
import json
from fastapi import APIRouter, HTTPException, Query, Header
from typing import Dict, Any, List, Optional
from ..common.errors import ChapterNotFoundError
from ..core.curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from ..core.curriculum_registry import CurriculumRegistry
from ..core.subject_registry import SubjectRegistry

router = APIRouter(prefix="/api/v1", tags=["Curriculum Runtime Architecture"])

CONTENTS_ROOT = r"D:/GURUKUL/Contents"

@router.get("/classes")
async def discover_classes():
    grades = CurriculumRegistry.get_classes()
    class_list = []
    for g in grades:
        subs = CurriculumRegistry.get_subjects(g)
        class_list.append({"grade": g, "subjects": subs})
    return class_list

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    subjects = CurriculumRegistry.get_subjects(grade)
    return {"grade": grade, "subjects": subjects}

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    canonical_sub = SubjectRegistry.resolve_canonical_subject(subject)
    sub_processed_dir = os.path.join(r"D:/GURUKUL/ProcessedContent", f"Class{grade}", subject.replace(" ", ""))
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
        "canonicalSubject": canonical_sub,
        "curriculumFramework": "NEP 2020 & NCF-SE 2023",
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

@router.get("/chapters/{chapterId}/source")
async def get_chapter_direct_source_v2(
    chapterId: str,
    grade: str = Query(...),
    subject: str = Query(...),
    book: str = Query(default="main"),
    unit: str = Query(default="U01")
):
    """
    STRICT CURRICULUM RUNTIME RESOLUTION ENDPOINT (V15):
    Requires mandatory class, subject, book, unit, and chapterId.
    Strictly forbids substring matching and returns HTTP 404 NOT_FOUND on any mismatch.
    """
    canonical_subj = SubjectRegistry.resolve_canonical_subject(subject)
    identity = CurriculumIdentity(
        grade=str(grade),
        subject=canonical_subj,
        book=book,
        unit=unit,
        chapter_id=chapterId,
        content_type="source_bundle"
    )

    try:
        dto: ChapterRuntimeDTO = CurriculumRegistry.load_chapter_bundle(identity)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "CHAPTER_NOT_FOUND",
                    "message": f"Chapter identity {identity.to_cache_key()} could not be resolved: {str(e)}",
                    "identity": identity.model_dump()
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

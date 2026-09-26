import os
import json
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from ..common.errors import ChapterNotFoundError

router = APIRouter(prefix="/api/v1", tags=["New Direct Curriculum Pipeline"])

PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"
CONTENTS_ROOT = r"D:\GURUKUL\Contents\Class 5"

@router.get("/classes")
async def discover_classes():
    subjects = []
    if os.path.exists(CONTENTS_ROOT):
        subjects = sorted([d for d in os.listdir(CONTENTS_ROOT) if os.path.isdir(os.path.join(CONTENTS_ROOT, d))])
    if not subjects:
        subjects = ["English", "Hindi", "Maths", "Science"]
    return [{"grade": "5", "subjects": subjects}]

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    subjects = []
    grade_dir = os.path.join(r"D:\GURUKUL\Contents", f"Class {grade}")
    if os.path.exists(grade_dir):
        subjects = sorted([d for d in os.listdir(grade_dir) if os.path.isdir(os.path.join(grade_dir, d))])
    if not subjects:
        subjects = ["English", "Hindi", "Maths", "Science"]
    return {"grade": grade, "subjects": subjects}

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject)
    chapters = []

    if os.path.exists(sub_processed_dir):
        ch_dirs = sorted([d for d in os.listdir(sub_processed_dir) if os.path.isdir(os.path.join(sub_processed_dir, d))])
        for idx, ch_id in enumerate(ch_dirs):
            notes_path = os.path.join(sub_processed_dir, ch_id, "notes.json")
            ch_title = ch_id
            if os.path.exists(notes_path):
                try:
                    with open(notes_path, "r", encoding="utf-8") as f:
                        nd = json.load(f)
                        ch_title = nd.get("chapterTitle") or nd.get("chapter_title") or nd.get("title") or ch_id
                except Exception:
                    pass
            # Extract chapter number from ch_id e.g. G5-ENG-U05-C10 -> 10
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

    if not chapters:
        count = 10 if subject.lower() == "english" else (12 if subject.lower() == "hindi" else (15 if subject.lower() == "maths" else 10))
        prefix = "ENG" if subject.lower() == "english" else ("HIN" if subject.lower() == "hindi" else ("MAT" if subject.lower() == "maths" else "SCI"))
        for i in range(1, count + 1):
            u = ((i - 1) // 3) + 1
            chapters.append({
                "id": f"G5-{prefix}-U{u:02d}-C{i:02d}",
                "chapterNumber": i,
                "title": f"{subject} Chapter {i}"
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
                "title": "Curriculum Unit",
                "chapters": chapters
            }
        ]
    }

@router.get("/chapters/{chapterId}")
async def get_chapter_details(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject, chapterId)
    if not os.path.exists(sub_processed_dir) and "C" in chapterId:
        # Robust fallback: search by chapter number suffix e.g. -C10
        target_c_suffix = chapterId.split("C")[-1]
        parent_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject)
        if os.path.exists(parent_dir):
            for d in os.listdir(parent_dir):
                if d.endswith(f"-C{target_c_suffix}"):
                    sub_processed_dir = os.path.join(parent_dir, d)
                    chapterId = d
                    break

    ch_title = chapterId
    unit_title = "Curriculum Unit"
    ch_num = 1

    notes_path = os.path.join(sub_processed_dir, "notes.json")
    if os.path.exists(notes_path):
        try:
            with open(notes_path, "r", encoding="utf-8") as f:
                notes_data = json.load(f)
                ch_title = notes_data.get("chapterTitle") or notes_data.get("chapter_title") or notes_data.get("title") or chapterId
                unit_title = notes_data.get("unitTitle") or notes_data.get("unit_title") or "Curriculum Unit"
                ch_num = notes_data.get("chapterNumber") or notes_data.get("chapter_number") or 1
        except Exception:
            pass

    return {
        "chapterId": chapterId,
        "grade": grade,
        "subject": subject,
        "chapterNumber": ch_num,
        "title": ch_title,
        "chapterTitle": ch_title,
        "unitTitle": unit_title,
        "unitNumber": 1
    }

@router.get("/chapters/{chapterId}/source")
async def get_chapter_direct_source_v2(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    """
    CLEAN RESET DIRECT SOURCE ENDPOINT (PROCESSED CONTENT LAYER):
    Reads directly from persistent ProcessedContent layer without runtime ingestion.
    Supports robust fallback matching by chapter number suffix (e.g. -C10).
    """
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject, chapterId)

    if not os.path.exists(sub_processed_dir) and "C" in chapterId:
        target_c_suffix = chapterId.split("C")[-1]
        parent_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject)
        if os.path.exists(parent_dir):
            for d in os.listdir(parent_dir):
                if d.endswith(f"-C{target_c_suffix}"):
                    sub_processed_dir = os.path.join(parent_dir, d)
                    chapterId = d
                    break

    if os.path.exists(sub_processed_dir):
        sections = {}
        for sec_name in ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]:
            sec_path = os.path.join(sub_processed_dir, f"{sec_name}.json")
            if os.path.exists(sec_path):
                try:
                    with open(sec_path, "r", encoding="utf-8") as f:
                        sections[sec_name] = json.load(f)
                except Exception:
                    sections[sec_name] = None
            else:
                sections[sec_name] = None

        ch_title = chapterId
        unit_title = "Curriculum Unit"
        ch_num = 1
        notes_data = sections.get("notes")
        if isinstance(notes_data, dict):
            ch_title = notes_data.get("chapterTitle") or notes_data.get("chapter_title") or notes_data.get("title") or chapterId
            unit_title = notes_data.get("unitTitle") or notes_data.get("unit_title") or "Curriculum Unit"
            ch_num = notes_data.get("chapterNumber") or notes_data.get("chapter_number") or 1

        return {
            "chapterId": chapterId,
            "grade": grade,
            "subject": subject,
            "chapterNumber": ch_num,
            "chapterTitle": ch_title,
            "unitTitle": unit_title,
            "sections": sections
        }

    raise HTTPException(status_code=404, detail=f"Chapter {chapterId} processed content not found.")

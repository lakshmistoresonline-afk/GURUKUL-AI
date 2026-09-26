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
    """
    Universal discovery API: Discovers available grades and subjects dynamically.
    """
    subjects = []
    if os.path.exists(CONTENTS_ROOT):
        subjects = sorted([d for d in os.listdir(CONTENTS_ROOT) if os.path.isdir(os.path.join(CONTENTS_ROOT, d))])
    if not subjects:
        subjects = ["English", "Hindi", "Maths", "Science"]
    return [{"grade": "5", "subjects": subjects}]

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    """
    Universal discovery API: Returns list of subjects available for a grade.
    """
    subjects = []
    grade_dir = os.path.join(r"D:\GURUKUL\Contents", f"Class {grade}")
    if os.path.exists(grade_dir):
        subjects = sorted([d for d in os.listdir(grade_dir) if os.path.isdir(os.path.join(grade_dir, d))])
    if not subjects:
        subjects = ["English", "Hindi", "Maths", "Science"]
    return {"grade": grade, "subjects": subjects}

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    """
    Universal subject details API: Returns subject metadata and chapter list.
    """
    sub_dir = os.path.join(CONTENTS_ROOT, subject)
    chapters = []
    if os.path.exists(sub_dir):
        # find chapters from overview or notes json
        ov_path = os.path.join(sub_dir, "Overview.json")
        if os.path.exists(ov_path):
            try:
                with open(ov_path, "r", encoding="utf-8") as f:
                    ov_data = json.load(f)
                    for idx, ch in enumerate(ov_data.get("chapters", [])):
                        c_num = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
                        u_num = ch.get("unit_number") or ch.get("unitNumber") or (((c_num - 1) // 3) + 1)
                        prefix = "ENG" if subject == "English" else ("HIN" if subject == "Hindi" else ("MAT" if subject == "Maths" else "SCI"))
                        ch_id = f"G5-{prefix}-U{u_num:02d}-C{c_num:02d}"
                        chapters.append({
                            "id": ch_id,
                            "chapterNumber": c_num,
                            "title": ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title") or f"Chapter {c_num}"
                        })
            except Exception:
                pass

    if not chapters:
        # Fallback chapter list if Overview.json isn't parsed
        count = 10 if subject == "English" else (12 if subject == "Hindi" else (15 if subject == "Maths" else 10))
        prefix = "ENG" if subject == "English" else ("HIN" if subject == "Hindi" else ("MAT" if subject == "Maths" else "SCI"))
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
    """
    Universal chapter details API: Returns chapter metadata.
    """
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject, chapterId)
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
    Returns the exact 7 fixed sections (overview, notes, master, flashcards, mindmaps, quiz, question_papers).
    """
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject, chapterId)

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

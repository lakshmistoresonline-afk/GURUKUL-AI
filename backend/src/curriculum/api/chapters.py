import os
import json
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
from ..common.errors import ChapterNotFoundError

router = APIRouter(prefix="/api/v1", tags=["New Direct Curriculum Pipeline"])

PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"
CONTENTS_ROOT = r"D:\GURUKUL\Contents"

@router.get("/classes")
async def discover_classes():
    grades = []
    if os.path.exists(CONTENTS_ROOT):
        grades = sorted([d.replace("Class ", "") for d in os.listdir(CONTENTS_ROOT) if os.path.isdir(os.path.join(CONTENTS_ROOT, d)) and "class" in d.lower()])
    if not grades:
        grades = ["5", "6", "7"]

    class_list = []
    for g in grades:
        g_dir = os.path.join(CONTENTS_ROOT, f"Class {g}")
        subjects = []
        if os.path.exists(g_dir):
            subjects = sorted([d for d in os.listdir(g_dir) if os.path.isdir(os.path.join(g_dir, d))])
        if not subjects:
            if g == "5":
                subjects = ["English", "Hindi", "Maths", "Science"]
            elif g == "6":
                subjects = ["English", "Hindi", "Maths", "Science", "Social"]
            elif g == "7":
                subjects = ["English", "Hindi", "Maths I", "Maths II", "Science", "Social I", "Social II"]
            else:
                subjects = ["English", "Hindi", "Maths", "Science"]
        class_list.append({"grade": g, "subjects": subjects})
    return class_list

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    subjects = []
    grade_dir = os.path.join(CONTENTS_ROOT, f"Class {grade}")
    if os.path.exists(grade_dir):
        subjects = sorted([d for d in os.listdir(grade_dir) if os.path.isdir(os.path.join(grade_dir, d))])
    if not subjects:
        if grade == "5":
            subjects = ["English", "Hindi", "Maths", "Science"]
        elif grade == "6":
            subjects = ["English", "Hindi", "Maths", "Science", "Social"]
        elif grade == "7":
            subjects = ["English", "Hindi", "Maths I", "Maths II", "Science", "Social I", "Social II"]
        else:
            subjects = ["English", "Hindi", "Maths", "Science"]
    return {"grade": grade, "subjects": subjects}

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject.replace(" ", ""))
    chapters = []

    if os.path.exists(sub_processed_dir):
        ch_dirs = sorted([d for d in os.listdir(sub_processed_dir) if os.path.isdir(os.path.join(sub_processed_dir, d))])
        for idx, ch_id in enumerate(ch_dirs):
            ch_dir = os.path.join(sub_processed_dir, ch_id)
            ch_title = ch_id

            # Check overview, notes, and master files for a valid title
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
                                if title and isinstance(title, str):
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

@router.get("/chapters/{chapterId}")
async def get_chapter_details(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject.replace(" ", ""), chapterId)
    if not os.path.exists(sub_processed_dir) and "C" in chapterId:
        target_c_suffix = chapterId.split("C")[-1]
        parent_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject.replace(" ", ""))
        if os.path.exists(parent_dir):
            for d in os.listdir(parent_dir):
                if d.endswith(f"-C{target_c_suffix}"):
                    sub_processed_dir = os.path.join(parent_dir, d)
                    chapterId = d
                    break

    ch_title = chapterId
    unit_title = "Curriculum Unit"
    ch_num = 1

    for sec in ["notes", "overview", "master"]:
        sec_path = os.path.join(sub_processed_dir, f"{sec}.json")
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
                        if title and isinstance(title, str):
                            ch_title = title
                            ch_num = d.get("chapterNumber") or d.get("chapter_number") or 1
                            unit_title = d.get("unitTitle") or d.get("unit_title") or "Curriculum Unit"
                            break
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
    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject.replace(" ", ""), chapterId)

    if not os.path.exists(sub_processed_dir) and "C" in chapterId:
        target_c_suffix = chapterId.split("C")[-1]
        parent_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject.replace(" ", ""))
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

        for sec in ["notes", "overview", "master"]:
            d = sections.get(sec)
            if isinstance(d, dict):
                title = (
                    d.get("chapterTitle") or
                    d.get("chapter_title") or
                    d.get("title") or
                    (isinstance(d.get("overview"), dict) and (d["overview"].get("chapter_title") or d["overview"].get("title")))
                )
                if title and isinstance(title, str):
                    ch_title = title
                    ch_num = d.get("chapterNumber") or d.get("chapter_number") or 1
                    unit_title = d.get("unitTitle") or d.get("unit_title") or "Curriculum Unit"
                    break

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

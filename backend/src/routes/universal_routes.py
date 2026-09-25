from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional

router = APIRouter(prefix="/api/v1", tags=["Universal Content Pipeline"])

@router.get("/classes")
async def discover_classes():
    return [{"grade": "5", "subjects": ["English", "Hindi", "Maths", "Science"]}]

@router.get("/classes/{grade}/subjects")
async def get_grade_subjects(grade: str):
    return {"grade": grade, "subjects": ["English", "Hindi", "Maths", "Science"]}

@router.get("/classes/{grade}/subjects/{subject}")
async def get_subject_details(grade: str, subject: str):
    return {
        "grade": grade,
        "subject": subject,
        "curriculumFramework": "NEP 2020 & NCF-SE 2023",
        "curricularGoals": [],
        "totalChapters": 10 if subject.lower() == "english" else (12 if subject.lower() == "hindi" else (15 if subject.lower() == "maths" else 10)),
        "units": []
    }

@router.get("/chapters/{chapterId}")
async def get_chapter_details(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    return {
        "chapterId": chapterId,
        "grade": grade,
        "subject": subject,
        "chapterNumber": 1,
        "title": chapterId,
        "chapterTitle": chapterId,
        "unitTitle": "Curriculum Unit",
        "unitNumber": 1
    }

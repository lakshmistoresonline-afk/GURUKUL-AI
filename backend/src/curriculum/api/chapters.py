import os
import json
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from ..registry import CurriculumRegistry
from ..common.errors import ChapterNotFoundError

router = APIRouter(prefix="/api/v1", tags=["New Direct Curriculum Pipeline"])

PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"

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

    # If processed files exist, read them directly
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

        # Load metadata/manifest if available
        manifest_path = os.path.join(sub_processed_dir, "manifest.json")
        ch_title = chapterId
        unit_title = "Curriculum Unit"
        ch_num = 1
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                    meta = manifest.get("meta", {})
                    # pull title from notes if present
                    notes_data = sections.get("notes")
                    if isinstance(notes_data, dict):
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
            "chapterTitle": ch_title,
            "unitTitle": unit_title,
            "sections": sections
        }

    # Fallback to processor if not yet processed
    try:
        processor = CurriculumRegistry.get_processor(grade, subject)
        result = processor.process_chapter(chapterId)
        return result
    except ChapterNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal processing error: {exc}")

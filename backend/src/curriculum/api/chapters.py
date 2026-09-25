from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any
from ..registry import CurriculumRegistry
from ..common.errors import ChapterNotFoundError

router = APIRouter(prefix="/api/v1", tags=["New Direct Curriculum Pipeline"])

@router.get("/chapters/{chapterId}/source")
async def get_chapter_direct_source_v2(
    chapterId: str,
    grade: str = Query(default="5"),
    subject: str = Query(default="English")
):
    """
    CLEAN RESET DIRECT SOURCE ENDPOINT:
    Routes strictly by Class + Subject to class-specific processors.
    Returns the exact 7 fixed sections directly from authoritative source JSON.
    """
    try:
        processor = CurriculumRegistry.get_processor(grade, subject)
        result = processor.process_chapter(chapterId)
        return result
    except ChapterNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal processing error: {exc}")

from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ChapterSections(BaseModel):
    overview: Optional[Dict[str, Any]] = None
    notes: Optional[Dict[str, Any]] = None
    master: Optional[Dict[str, Any]] = None
    flashcards: List[Dict[str, Any]] = []
    mindmaps: Optional[Dict[str, Any]] = None
    quiz: List[Dict[str, Any]] = []
    question_papers: Optional[Dict[str, Any]] = None

class ChapterSourceResponse(BaseModel):
    chapterId: str
    grade: str
    subject: str
    chapterNumber: int
    chapterTitle: str
    unitTitle: str
    sections: ChapterSections

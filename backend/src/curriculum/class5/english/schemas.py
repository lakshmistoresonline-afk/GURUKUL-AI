from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class EnglishChapterSource(BaseModel):
    chapterId: str
    grade: str = "5"
    subject: str = "English"
    chapterNumber: int
    chapterTitle: str
    unitTitle: str
    sections: Dict[str, Any]

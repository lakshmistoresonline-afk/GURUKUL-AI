from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class CurriculumIdentity(BaseModel):
    grade: str
    subject: str
    book: Optional[str] = "main"
    unit: Optional[str] = "U01"
    chapter_id: str
    content_type: str

    def to_cache_key(self) -> str:
        return f"class{self.grade}:{self.subject.lower()}:{self.book.lower()}:{self.unit.lower()}:{self.chapter_id.lower()}:{self.content_type.lower()}"

class ChapterRuntimeDTO(BaseModel):
    identity: CurriculumIdentity
    chapter_number: int
    chapter_title: str
    unit_title: str
    data: Dict[str, Any]
    status: str = "READY" # READY, PARTIAL, NOT_FOUND, INVALID

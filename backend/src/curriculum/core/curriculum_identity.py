from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CurriculumIdentity(BaseModel):
    grade: str
    subject: str
    book: str # Mandatory book/part identifier (e.g. 'main', 'part1', 'part2')
    unit: str # Mandatory unit identifier (e.g. 'U01')
    chapter_id: str # Mandatory exact chapter source identifier
    content_type: str # Mandatory content type (overview, notes, master, etc.)

    def to_cache_key(self) -> str:
        return f"class{self.grade}:{self.subject.lower()}:{self.book.lower()}:{self.unit.lower()}:{self.chapter_id.lower()}:{self.content_type.lower()}"

class ChapterRuntimeDTO(BaseModel):
    identity: CurriculumIdentity
    chapter_number: int
    chapter_title: str
    unit_title: str
    data: Dict[str, Any]
    status: str = "READY"

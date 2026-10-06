from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CurriculumIdentity(BaseModel):
    grade: str = Field(..., description="Target grade/class (e.g., '5', '6', '7')")
    subject: str = Field(..., description="Canonical subject ID (e.g., 'mathematics', 'english', 'social_science')")
    book: str = Field(default="main", description="Book identifier (e.g., 'main', 'book1', 'book2')")
    part: str = Field(default="none", description="Part identifier (e.g., 'part1', 'part2', 'none')")
    unit: str = Field(default="U01", description="Unit identifier (e.g., 'U01', 'unit1')")
    chapter_id: str = Field(..., description="Exact chapter source identifier (e.g., 'G5-ENG-U01-C01')")
    content_type: str = Field(..., description="Content type (overview, notes, master, foundational, flashcards, mindmaps, quiz, question_papers)")

    def to_cache_key(self) -> str:
        return f"class{self.grade}:{self.subject.lower()}:{self.book.lower()}:{self.part.lower()}:{self.unit.lower()}:{self.chapter_id.lower()}:{self.content_type.lower()}"

class ChapterRuntimeDTO(BaseModel):
    identity: CurriculumIdentity
    chapter_number: int
    chapter_title: str
    unit_title: str
    data: Dict[str, Any]
    status: str = "READY"

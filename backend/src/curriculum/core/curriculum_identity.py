from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any

class CurriculumIdentity(BaseModel):
    grade: str = Field(..., description="Target grade/class (e.g., '5', '6', '7')")
    subject: str = Field(..., description="Canonical subject ID ('english', 'hindi', 'mathematics', 'science', 'social_science')")
    book: str = Field(..., description="Book identifier (e.g., 'main', 'maths_i', 'maths_ii', 'social_i', 'social_ii')")
    part: str = Field(..., description="Part identifier (e.g., 'part1', 'part2', 'main', 'none')")
    unit: str = Field(..., description="Unit identifier (e.g., 'U01', 'U02')")
    chapter_id: str = Field(..., description="Exact chapter source identifier")
    content_type: str = Field(..., description="Content type (overview, notes, master, foundational, flashcards, mindmaps, quiz, question_papers)")

    @field_validator("grade", "subject", "book", "part", "unit", "chapter_id", "content_type")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not str(v).strip():
            raise ValueError("Identity dimension cannot be empty or blank.")
        return str(v).strip()

    def to_cache_key(self) -> str:
        return f"class{self.grade}:{self.subject.lower()}:book:{self.book.lower()}:part:{self.part.lower()}:unit:{self.unit.lower()}:ch:{self.chapter_id.lower()}:ct:{self.content_type.lower()}"

class ChapterRuntimeDTO(BaseModel):
    identity: CurriculumIdentity
    chapter_number: int
    chapter_title: str
    unit_number: int
    unit_title: str
    data: Dict[str, Any]
    status: str = "READY"

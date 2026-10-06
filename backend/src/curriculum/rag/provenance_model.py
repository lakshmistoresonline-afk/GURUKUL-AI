from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class RagProvenance(BaseModel):
    grade: str = Field(..., description="Grade / Class")
    subject: str = Field(..., description="Canonical subject ID")
    book: str = Field(..., description="Book identifier")
    part: str = Field(..., description="Part identifier")
    unit: str = Field(..., description="Unit identifier")
    chapter_id: str = Field(..., description="Exact chapter source ID")
    content_type: str = Field(..., description="Content type (overview, notes, master, etc.)")
    content_id: str = Field(..., description="Specific learning item or chunk ID")
    source_path: str = Field(..., description="Absolute or relative path to source document")
    source_hash: str = Field(..., description="SHA-256 hash of authoritative source document")
    processed_path: str = Field(..., description="Path to processed JSON artifact")
    processor_version: str = Field(default="V14-STRICT", description="Processor version")
    schema_version: str = Field(default="3.0.0", description="Schema version")

    def verify_completeness(self) -> bool:
        """Ensures all required provenance fields are present and non-empty."""
        return all([
            self.grade,
            self.subject,
            self.book,
            self.unit,
            self.chapter_id,
            self.content_type,
            self.content_id,
            self.source_path,
            self.source_hash,
            self.processed_path,
            self.processor_version,
            self.schema_version
        ])

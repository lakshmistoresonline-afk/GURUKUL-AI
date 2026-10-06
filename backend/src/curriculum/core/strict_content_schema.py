from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List

class ChapterManifestModel(BaseModel):
    grade: str = Field(..., description="Grade / Class")
    subject: str = Field(..., description="Canonical subject ID")
    book: str = Field(..., description="Book identifier")
    part: str = Field(..., description="Part identifier")
    unit: str = Field(..., description="Unit identifier")
    chapter_id: str = Field(..., description="Exact chapter source identifier")
    chapter_number: int = Field(..., description="Chapter number")
    chapter_title: str = Field(..., description="Chapter title")
    unit_number: int = Field(..., description="Unit number")
    unit_title: str = Field(..., description="Unit title")
    source_hash: Optional[str] = Field(default="", description="SHA-256 hash of authoritative source")
    schema_version: str = Field(default="3.0.0", description="Schema version")
    processor_version: str = Field(default="V14-STRICT", description="Processor version")

class VersionedSchemaEnvelope(BaseModel):
    identity: Dict[str, Any]
    schema_version: str = "3.0.0"
    processor_version: str = "V14-STRICT"
    source_hash: str
    content_type: str
    payload: Any

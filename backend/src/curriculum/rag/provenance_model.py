from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from ..core.curriculum_identity import CurriculumIdentity

class ProvenanceInconsistencyError(Exception):
    """Raised when RAG provenance is missing or inconsistent with the requested identity."""
    pass

class RagProvenance(BaseModel):
    grade: str = Field(..., description="Grade / Class")
    subject: str = Field(..., description="Canonical subject ID")
    book: str = Field(..., description="Book identifier")
    part: str = Field(..., description="Part identifier")
    unit: str = Field(..., description="Unit identifier")
    chapter_id: str = Field(..., description="Exact chapter source ID")
    content_type: str = Field(..., description="Content type (overview, notes, master, etc.)")
    content_id: str = Field(..., description="Specific learning item ID")
    source_path: str = Field(..., description="Path to authoritative source document")
    source_sha256: str = Field(..., description="SHA-256 hash of authoritative source document")
    processed_path: str = Field(..., description="Path to processed JSON artifact")
    processed_sha256: str = Field(..., description="SHA-256 hash of processed artifact")
    processor_version: str = Field(default="V14-STRICT", description="Processor version")
    schema_version: str = Field(default="3.0.0", description="Schema version")
    chunk_id: str = Field(..., description="Unique chunk identifier")

    def verify_completeness(self) -> bool:
        """Ensures all required provenance fields are present and non-empty."""
        return all([
            self.grade,
            self.subject,
            self.book,
            self.part,
            self.unit,
            self.chapter_id,
            self.content_type,
            self.content_id,
            self.source_path,
            self.source_sha256,
            self.processed_path,
            self.processed_sha256,
            self.processor_version,
            self.schema_version,
            self.chunk_id
        ])

    @classmethod
    def validate_against_identity(cls, identity: CurriculumIdentity, provenance: "RagProvenance") -> "RagProvenance":
        """
        Validates that RAG provenance strictly matches requested curriculum identity.
        Fails closed (raises ProvenanceInconsistencyError) on any mismatch.
        """
        if not provenance.verify_completeness():
            raise ProvenanceInconsistencyError("Incomplete RAG provenance detected.")

        if str(provenance.grade) != str(identity.grade):
            raise ProvenanceInconsistencyError(f"Provenance mismatch: grade '{provenance.grade}' != requested '{identity.grade}'")
        if str(provenance.subject).lower() != str(identity.subject).lower():
            raise ProvenanceInconsistencyError(f"Provenance mismatch: subject '{provenance.subject}' != requested '{identity.subject}'")
        if str(provenance.book).lower() != str(identity.book).lower():
            raise ProvenanceInconsistencyError(f"Provenance mismatch: book '{provenance.book}' != requested '{identity.book}'")
        if str(provenance.part).lower() != str(identity.part).lower():
            raise ProvenanceInconsistencyError(f"Provenance mismatch: part '{provenance.part}' != requested '{identity.part}'")
        if str(provenance.unit).upper() != str(identity.unit).upper():
            raise ProvenanceInconsistencyError(f"Provenance mismatch: unit '{provenance.unit}' != requested '{identity.unit}'")
        if str(provenance.chapter_id).lower() != str(identity.chapter_id).lower():
            raise ProvenanceInconsistencyError(f"Provenance mismatch: chapter_id '{provenance.chapter_id}' != requested '{identity.chapter_id}'")
        if str(provenance.content_type).lower() != str(identity.content_type).lower():
            raise ProvenanceInconsistencyError(f"Provenance mismatch: content_type '{provenance.content_type}' != requested '{identity.content_type}'")

        return provenance

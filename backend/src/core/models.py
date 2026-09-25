from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

class ContentTypeManifestItem(BaseModel):
    type: str                     # Normalized semantic type
    sourceType: str               # Raw original key from source JSON
    learningStage: str = "learn"
    presentationSection: str = "learn"
    count: int = 1
    renderer: str

class ContentManifest(BaseModel):
    chapterId: str
    contentTypes: List[ContentTypeManifestItem] = Field(default_factory=list)
    sourceSchemaVersion: str = "1.0.0"
    normalizedSchemaVersion: str = "2.0.0"
    adapterVersion: str = "1.0.0"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ContentBlock(BaseModel):
    id: str                       # Stable unique identifier
    sourceType: str               # Original source dataset terminology
    normalizedType: str           # Extensible semantic type classification
    learningStage: str = "learn"  # 'overview', 'learn', 'practice', 'revision', 'assessment'
    presentationSection: str = "learn" # 'overview', 'learn', 'practice', 'flashcards', 'mindmap', 'quiz'
    assessmentRole: str = "practice"    # 'practice' vs 'final'
    title: str                    # Human-readable block title
    renderer: str                 # Renderer component ID
    data: Any                     # Raw data payload preserved losslessly
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Source Provenance
    sourceDataset: Optional[str] = "NCERT"
    sourcePath: Optional[str] = None
    sourceIdentifier: Optional[str] = None

    # Schema Versioning
    sourceSchemaVersion: str = "1.0.0"
    normalizedSchemaVersion: str = "2.0.0"
    adapterVersion: str = "1.0.0"

    order: int = 0

class Chapter(BaseModel):
    id: str
    grade: str
    subject: str
    unitId: Optional[str] = None
    chapterNumber: int
    title: str
    contentManifest: Optional[ContentManifest] = None

class ContentPackage(BaseModel):
    id: str
    curriculum: str = "NCERT"
    grade: str
    subject: str
    source: str
    units: List[Dict[str, Any]] = Field(default_factory=list)
    chapters: List[Chapter] = Field(default_factory=list)
    schemaVersion: str = "1.0.0"
    contentManifest: Optional[ContentManifest] = None

import enum
from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Boolean, Enum as SQLEnum
from .job import Base
from datetime import datetime
import uuid

class ReuseDecision(enum.Enum):
    IMPORT_ALLOWED = "IMPORT_ALLOWED"
    LINK_ONLY = "LINK_ONLY"
    LICENSE_RESTRICTED = "LICENSE_RESTRICTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    UNKNOWN = "UNKNOWN"

class ApprovalStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ImportStatus(enum.Enum):
    NOT_ATTEMPTED = "NOT_ATTEMPTED"
    QUEUED = "QUEUED"
    DOWNLOADING = "DOWNLOADING"
    VERIFYING = "VERIFYING"
    IMPORTED = "IMPORTED"
    LINK_ONLY = "LINK_ONLY"
    FAILED = "FAILED"
    DUPLICATE = "DUPLICATE"
    BLOCKED = "BLOCKED"

class RAGStatus(enum.Enum):
    NOT_INDEXED = "NOT_INDEXED"
    QUEUED = "QUEUED"
    INDEXING = "INDEXING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"

class ExternalSource(Base):
    __tablename__ = "external_sources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    organization = Column(String)
    type = Column(String) # e.g. "GOVERNMENT", "INSTITUTION", "PLATFORM"
    official_url = Column(String)
    api_url = Column(String)
    description = Column(String)
    is_official = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "organization": self.organization,
            "official_url": self.official_url,
            "description": self.description,
            "is_official": self.is_official
        }

class ResourceCollection(Base):
    __tablename__ = "resource_collections"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("external_sources.id"), index=True)
    parent_id = Column(String, ForeignKey("resource_collections.id"), index=True)
    external_id = Column(String, index=True) # e.g. do_id
    title = Column(String)
    description = Column(String)

    status = Column(String, default="PENDING") # PENDING, PROCESSING, COMPLETED, FAILED
    stats_json = Column(JSON, default={})

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "source_id": self.source_id,
            "parent_id": self.parent_id,
            "external_id": self.external_id,
            "title": self.title,
            "status": self.status,
            "stats": self.stats_json,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class VerifiedResource(Base):
    __tablename__ = "verified_resources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id = Column(String, index=True)
    source_id = Column(String, ForeignKey("external_sources.id"), index=True)
    collection_id = Column(String, ForeignKey("resource_collections.id"), index=True)
    root_collection_id = Column(String, ForeignKey("resource_collections.id"), index=True)

    original_resource_id = Column(String, index=True)
    resolved_resource_id = Column(String, index=True)

    title = Column(String)
    description = Column(String)
    url = Column(String, unique=True)
    type = Column(String) # video, pdf, epub, audio, interactive, etc.
    thumbnail = Column(String)
    source = Column(String) # display name of source

    # Curriculum Mapping
    board = Column(String)
    class_level = Column(String)
    subject = Column(String)
    chapter_num = Column(String)
    topic = Column(String)
    language = Column(String)
    medium = Column(String)

    # Relevance Data
    relevance_score = Column(Float)
    verification_reason = Column(String)

    # Licensing & Attribution
    license_detected = Column(String)
    license_verified = Column(Boolean, default=False)
    reuse_decision = Column(SQLEnum(ReuseDecision), default=ReuseDecision.UNKNOWN)
    approval_status = Column(SQLEnum(ApprovalStatus), default=ApprovalStatus.PENDING)

    # Import Details & Provenance
    import_status = Column(SQLEnum(ImportStatus), default=ImportStatus.NOT_ATTEMPTED)
    source_download_url = Column(String)
    download_method = Column(String)
    downloaded_at = Column(DateTime)
    local_path = Column(String)
    storage_path = Column(String)
    content_hash = Column(String, index=True)
    file_size = Column(Integer)
    mime_type = Column(String)

    # Integrity Check
    integrity_status = Column(String) # Healthy, Missing, Mismatch
    integrity_verified_at = Column(DateTime)

    # RAG Indexing
    rag_status = Column(SQLEnum(RAGStatus), default=RAGStatus.NOT_INDEXED)
    rag_indexed_at = Column(DateTime)
    rag_document_id = Column(String)
    rag_error_code = Column(String)
    rag_error_message = Column(String)
    rag_failure_stage = Column(String)
    chunk_count = Column(Integer, default=0)

    # Metadata & Attribution
    license_url = Column(String)
    attribution = Column(String)
    publisher = Column(String)
    author = Column(String)
    copyright = Column(String)

    metadata_json = Column(JSON, default={}) # Raw metadata

    verified_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "chapter_id": self.chapter_id,
            "class_level": self.class_level,
            "subject": self.subject,
            "topic": self.topic,
            "source_id": self.source_id,
            "collection_id": self.collection_id,
            "root_collection_id": self.root_collection_id,
            "original_resource_id": self.original_resource_id,
            "resolved_resource_id": self.resolved_resource_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "type": self.type,
            "thumbnail": self.thumbnail,
            "source": self.source,
            "relevance_score": self.relevance_score,
            "approval_status": self.approval_status.value if self.approval_status else None,
            "reuse_decision": self.reuse_decision.value if self.reuse_decision else None,
            "license_detected": self.license_detected,
            "license_verified": self.license_verified,
            "import_status": self.import_status.value if self.import_status else None,
            "local_path": self.local_path,
            "storage_path": self.storage_path,
            "content_hash": self.content_hash,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "rag_status": self.rag_status.value if self.rag_status else None,
            "rag_error_message": self.rag_error_message,
            "rag_failure_stage": self.rag_failure_stage,
            "chunk_count": self.chunk_count,
            "integrity_status": self.integrity_status,
            "attribution": self.attribution,
            "metadata": self.metadata_json,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None
        }

class ResourceChunk(Base):
    __tablename__ = "resource_chunks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resource_id = Column(String, ForeignKey("verified_resources.id"), index=True)
    content = Column(String)

    # Metadata for filtering
    class_level = Column(String, index=True)
    subject = Column(String, index=True)
    chapter_id = Column(String, index=True)
    topic = Column(String, index=True)

    metadata_json = Column(JSON, default={})

    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "resource_id": self.resource_id,
            "content": self.content,
            "metadata": self.metadata_json
        }

class ExternalVideo(Base):
    __tablename__ = "external_videos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Curriculum Mapping
    class_level = Column(String, index=True)
    subject = Column(String, index=True)
    book = Column(String)
    unit = Column(String)
    chapter_id = Column(String, index=True)
    topic = Column(String, index=True)
    language = Column(String)

    # Metadata
    source_platform = Column(String) # e.g. "YouTube"
    video_id = Column(String, index=True)
    video_url = Column(String, unique=True)
    title = Column(String)
    description = Column(String)
    channel_name = Column(String)
    duration = Column(String)
    thumbnail_url = Column(String)
    published_date = Column(DateTime)

    # Discovery & Quality
    discovery_query = Column(String)
    relevance_score = Column(Float)
    quality_score = Column(Float)
    validation_status = Column(String) # VERIFIED, PARTIALLY_VERIFIED, METADATA_ONLY, REJECTED
    availability_status = Column(String, default="AVAILABLE") # AVAILABLE, UNAVAILABLE

    video_type = Column(String) # CONCEPT_EXPLANATION, ANIMATION, etc.

    last_verified = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "class_level": self.class_level,
            "subject": self.subject,
            "chapter_id": self.chapter_id,
            "topic": self.topic,
            "source_platform": self.source_platform,
            "video_id": self.video_id,
            "video_url": self.video_url,
            "title": self.title,
            "channel_name": self.channel_name,
            "duration": self.duration,
            "thumbnail_url": self.thumbnail_url,
            "relevance_score": self.relevance_score,
            "video_type": self.video_type,
            "availability": self.availability_status
        }

class ExternalMultimediaResource(Base):
    __tablename__ = "external_multimedia_resources"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id = Column(String, index=True)
    class_name = Column(String, index=True)
    subject = Column(String, index=True)
    provider = Column(String, index=True)
    title = Column(String)
    url = Column(String, index=True) # Normalized URL
    resource_types = Column(JSON) # List of strings
    search_url = Column(String, nullable=True)
    search_terms = Column(JSON, nullable=True)
    chapter_deep_link_verified = Column(Boolean, default=False)
    enabled = Column(Boolean, default=False)
    youtube = Column(Boolean, default=False) # Should be false for this catalog
    source = Column(String) # "CATALOG_V3" or "API_IMPORT"
    verification_status = Column(String, default="PENDING") # PENDING, VERIFIED, REJECTED

    admin_verified_by = Column(String, nullable=True)
    admin_verified_at = Column(DateTime, nullable=True)
    last_checked = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "chapter_id": self.chapter_id,
            "class_name": self.class_name,
            "subject": self.subject,
            "provider": self.provider,
            "title": self.title,
            "url": self.url,
            "resource_types": self.resource_types,
            "search_url": self.search_url,
            "search_terms": self.search_terms,
            "chapter_deep_link_verified": self.chapter_deep_link_verified,
            "enabled": self.enabled,
            "youtube": self.youtube,
            "source": self.source,
            "verification_status": self.verification_status,
            "admin_verified_at": self.admin_verified_at.isoformat() if self.admin_verified_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

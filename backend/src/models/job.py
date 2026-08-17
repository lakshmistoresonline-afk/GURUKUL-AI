from sqlalchemy import Column, String, Integer, Float, DateTime, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import enum
import uuid

class Base(DeclarativeBase):
    pass

class JobStatus(enum.Enum):
    UPLOADED = "UPLOADED"
    VALIDATING = "VALIDATING"
    EXTRACTING = "EXTRACTING"
    GENERATING = "GENERATING"
    VALIDATING_OUTPUT = "VALIDATING_OUTPUT"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRY_REQUIRED = "RETRY_REQUIRED"
    SKIPPED = "SKIPPED"
    PAUSED_PROVIDER_UNAVAILABLE = "PAUSED_PROVIDER_UNAVAILABLE"
    INTERRUPTED = "INTERRUPTED"

class ChapterJob(Base):
    __tablename__ = "chapter_jobs"

    job_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = Column(String, index=True)
    book_id = Column(String, index=True)
    chapter_id = Column(String, index=True)
    class_name = Column(String, index=True)
    subject = Column(String, index=True)

    source_file = Column(String)
    source_file_hash = Column(String, index=True)

    status = Column(SQLEnum(JobStatus), default=JobStatus.UPLOADED)
    current_stage = Column(String, default="INIT")
    progress = Column(Float, default=0.0)

    provider = Column(String)
    model = Column(String)

    # Store intermediate results as JSON
    completed_stages = Column(JSON, default={})

    error = Column(String)
    failure_category = Column(String)
    retry_count = Column(Integer, default=0)

    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "student_id": self.student_id,
            "book_id": self.book_id,
            "chapter_id": self.chapter_id,
            "class_name": self.class_name,
            "subject": self.subject,
            "status": self.status.value,
            "current_stage": self.current_stage,
            "progress": self.progress,
            "error": self.error,
            "failure_category": self.failure_category,
            "retry_count": self.retry_count,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class MediaJob(Base):
    __tablename__ = "media_jobs"

    job_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id = Column(String, index=True)
    class_name = Column(String, index=True)
    subject = Column(String, index=True)

    type = Column(String) # animation, video, image
    status = Column(SQLEnum(JobStatus), default=JobStatus.UPLOADED)
    current_stage = Column(String, default="INIT")
    progress = Column(Float, default=0.0)

    # Output paths
    output_path = Column(String)
    thumbnail_path = Column(String)
    subtitles_path = Column(String)

    # Store intermediate steps like storyboard, script, etc.
    metadata_json = Column(JSON, default={})

    error = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "chapter_id": self.chapter_id,
            "class_name": self.class_name,
            "subject": self.subject,
            "type": self.type,
            "status": self.status.value,
            "current_stage": self.current_stage,
            "progress": self.progress,
            "output_path": self.output_path,
            "thumbnail_path": self.thumbnail_path,
            "subtitles_path": self.subtitles_path,
            "error": self.error,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

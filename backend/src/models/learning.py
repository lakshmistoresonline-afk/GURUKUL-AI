from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Enum
import enum
from datetime import datetime
from .job import Base

class MisconceptionStatus(enum.Enum):
    SUSPECTED = "SUSPECTED"
    CONFIRMED = "CONFIRMED"
    RESOLVED = "RESOLVED"

class MisconceptionRecord(Base):
    __tablename__ = "misconception_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, index=True)
    concept_id = Column(String, index=True) # GUID
    misconception_type = Column(String) # e.g., "independent_fraction_parts"
    status = Column(Enum(MisconceptionStatus), default=MisconceptionStatus.SUSPECTED)
    evidence_count = Column(Integer, default=1)
    first_detected_at = Column(DateTime, default=datetime.utcnow)
    last_detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    metadata_json = Column(JSON, default={})

class LearningActivity(Base):
    __tablename__ = "learning_activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, index=True)
    activity_type = Column(String) # LEARN, PRACTICE, DIAGNOSTIC, REMEDIATE, TRANSFER, TEACH
    concept_id = Column(String, index=True)
    chapter_id = Column(String, index=True)
    status = Column(String) # COMPLETED, FAILED, IN_PROGRESS
    score = Column(Float, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    metadata_json = Column(JSON, default={})

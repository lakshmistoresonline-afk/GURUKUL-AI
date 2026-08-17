from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .job import Base

class SRSItem(Base):
    __tablename__ = "srs_items"

    id = Column(String, primary_key=True) # Usually combination of student_id and content_id
    student_id = Column(String, index=True)
    content_id = Column(String, index=True) # Chapter ID or specific Flashcard index
    content_type = Column(String) # 'chapter', 'flashcard', 'concept'

    # SM-2 Algorithm parameters
    easiness_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0) # days
    repetitions = Column(Integer, default=0)

    last_reviewed = Column(DateTime, default=datetime.utcnow)
    next_review = Column(DateTime, index=True)

    metadata_json = Column(JSON, default={})

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "content_id": self.content_id,
            "content_type": self.content_type,
            "easiness_factor": self.easiness_factor,
            "interval": self.interval,
            "repetitions": self.repetitions,
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else None,
            "next_review": self.next_review.isoformat() if self.next_review else None,
            "metadata": self.metadata_json
        }

class SRSReview(Base):
    __tablename__ = "srs_reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(String, ForeignKey("srs_items.id"))
    rating = Column(Integer) # 1 (Again), 2 (Hard), 3 (Good), 4 (Easy)
    reviewed_at = Column(DateTime, default=datetime.utcnow)

    # Store state before review for telemetry
    old_interval = Column(Integer)
    new_interval = Column(Integer)

class ErrorEvent(Base):
    __tablename__ = "error_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String, index=True)
    question_id = Column(String, index=True)
    concept_id = Column(String, index=True) # GUID
    chapter_id = Column(String)
    error_type = Column(String) # CONCEPTUAL|PROCEDURAL|READING|CARELESS|GUESS|OTHER
    created_at = Column(DateTime, default=datetime.utcnow)
    attempt_id = Column(String) # Optional to group session

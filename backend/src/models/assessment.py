from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Enum
import enum
from datetime import datetime
from .job import Base

class PaperType(enum.Enum):
    UNIT_TEST = "UNIT_TEST"
    MID_TERM = "MID_TERM"
    ANNUAL = "ANNUAL"
    MODEL = "MODEL"
    SAMPLE = "SAMPLE"
    PRACTICE = "PRACTICE"
    PYQ = "PYQ"

class QuestionPaper(Base):
    __tablename__ = "question_papers"

    id = Column(String, primary_key=True) # Usually a GUID
    title = Column(String)
    subject = Column(String, index=True)
    class_level = Column(Integer, index=True)
    paper_type = Column(Enum(PaperType))
    total_marks = Column(Integer)
    duration_minutes = Column(Integer)
    year = Column(Integer, nullable=True)
    board = Column(String, default="NCERT")
    questions_json = Column(JSON) # List of question IDs or full question objects
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(JSON, default={})

class ExamSession(Base):
    __tablename__ = "exam_sessions"

    id = Column(String, primary_key=True)
    student_id = Column(String, index=True)
    paper_id = Column(String, ForeignKey("question_papers.id"))
    status = Column(String) # STARTED, SUBMITTED, EVALUATED
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    score = Column(Float, nullable=True)
    responses_json = Column(JSON, default=[])
    evaluation_json = Column(JSON, default={})

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Enum, Boolean
import enum
from datetime import datetime
from .job import Base

class TaskType(enum.Enum):
    LEARN = "LEARN"
    PRACTICE = "PRACTICE"
    QUIZ = "QUIZ"
    REVISION = "REVISION"
    HOMEWORK = "HOMEWORK"

class StudyTask:
    def __init__(self, id, title, type, estimated_time_minutes, scheduled_date, is_completed=False):
        self.id = id
        self.title = title
        self.type = type
        self.estimated_time_minutes = estimated_time_minutes
        self.scheduled_date = scheduled_date
        self.is_completed = is_completed

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "type": self.type.value,
            "estimated_time_minutes": self.estimated_time_minutes,
            "scheduled_date": self.scheduled_date.isoformat(),
            "is_completed": self.is_completed
        }

class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(String, primary_key=True)
    student_id = Column(String, index=True)
    tasks_json = Column(JSON) # List of StudyTask dicts
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(JSON, default={})

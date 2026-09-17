from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, Boolean, Table, Text
from sqlalchemy.orm import relationship
from .db_config import Base

class UserORM(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="STUDENT")
    student_profile_id = Column(String, ForeignKey("students.id"), nullable=True)
    is_active = Column(Boolean, default=True)

    # Firebase Authentication identity
    firebase_uid = Column(String, unique=True, index=True, nullable=True)

class StudentORM(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True)
    name = Column(String)
    class_id = Column(String)
    enrollment_date = Column(String)
    timezone = Column(String, default="UTC")

class SubjectORM(Base):
    __tablename__ = "subjects"
    id = Column(String, primary_key=True)
    name = Column(String)
    class_id = Column(String)
    chapters = relationship("ChapterORM", back_populates="subject")

class ChapterORM(Base):
    __tablename__ = "chapters"
    id = Column(String, primary_key=True)
    title = Column(String)
    number = Column(Integer)
    subject_id = Column(String, ForeignKey("subjects.id"))
    class_id = Column(String)

    # Authoritative V3 Data Layers (Text storage for manual parsing)
    presentation_json = Column(Text)
    source_json = Column(Text)
    multimedia_json = Column(Text)

    subject = relationship("SubjectORM", back_populates="chapters")
    content_items = relationship("ContentItemORM", back_populates="chapter")

class ContentItemORM(Base):
    __tablename__ = "content_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chapter_id = Column(String, ForeignKey("chapters.id"))
    layer = Column(String) # 'presentation' or 'source'
    section = Column(String) # 'overview', 'learn', etc.
    category = Column(String, nullable=True)
    type = Column(String, nullable=True)
    heading = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)

    chapter = relationship("ChapterORM", back_populates="content_items")

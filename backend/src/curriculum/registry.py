from typing import Dict, Any, Optional
from .class5.english.processor import Class5EnglishProcessor
from .class5.hindi.processor import Class5HindiProcessor
from .class5.maths.processor import Class5MathsProcessor
from .class5.science.processor import Class5ScienceProcessor
from .common.errors import ChapterNotFoundError

class CurriculumRegistry:
    PROCESSORS = {
        ("5", "english"): Class5EnglishProcessor,
        ("5", "hindi"): Class5HindiProcessor,
        ("5", "maths"): Class5MathsProcessor,
        ("5", "science"): Class5ScienceProcessor,
    }

    @classmethod
    def get_processor(cls, grade: str, subject: str):
        key = (str(grade).strip(), str(subject).strip().lower())
        processor = cls.PROCESSORS.get(key)
        if not processor:
            raise ChapterNotFoundError(f"No processor registered for Grade {grade} Subject {subject}")
        return processor

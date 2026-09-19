from typing import Type
from .pipeline import BaseSubjectProcessor
from ..english.processor import EnglishSubjectProcessor
from ..hindi.processor import HindiSubjectProcessor
from ..mathematics.processor import MathematicsSubjectProcessor
from ..evs.processor import EVSSubjectProcessor

class SubjectRegistry:
    _registry: dict[str, Type[BaseSubjectProcessor]] = {
        "english": EnglishSubjectProcessor,
        "hindi": HindiSubjectProcessor,
        "mathematics": MathematicsSubjectProcessor,
        "evs": EVSSubjectProcessor,
    }

    @classmethod
    def register(cls, subject: str, processor_cls: Type[BaseSubjectProcessor]) -> None:
        if not subject or not processor_cls:
            raise ValueError("Subject name and processor class are required for registration.")
        cls._registry[subject.lower().strip()] = processor_cls

    @classmethod
    def get_processor(cls, subject: str) -> Type[BaseSubjectProcessor]:
        if not subject:
            raise ValueError("Subject name is required to retrieve a processor.")
        key = subject.lower().strip()
        if key not in cls._registry:
            raise ValueError(f"Unsupported subject processor: '{subject}'. Registered subjects: {list(cls._registry.keys())}")
        return cls._registry[key]

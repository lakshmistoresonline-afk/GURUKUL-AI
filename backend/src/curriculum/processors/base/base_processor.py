from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ...core.curriculum_identity import CurriculumIdentity

class BaseProcessor(ABC):
    """
    Abstract Base Class for all Class x Subject curriculum processors.
    Enforces strict read-only processing, schema versioning, and identity validation.
    """
    version = "V14-STRICT"
    schema_version = "3.0.0"

    def process(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate(identity, raw_data):
            raise ValueError(f"Validation failed in {self.__class__.__name__} for identity: {identity.to_cache_key()}")
        return {
            "identity": identity.model_dump(),
            "processor": self.__class__.__name__,
            "processor_version": self.version,
            "schema_version": self.schema_version,
            "normalized_content": raw_data if isinstance(raw_data, (dict, list)) else {"content": raw_data},
            "provenance": {
                "grade": identity.grade,
                "subject": identity.subject,
                "book": identity.book,
                "part": identity.part,
                "unit": identity.unit,
                "chapter_id": identity.chapter_id,
                "processor_key": f"{identity.grade}:{identity.subject}:{identity.book}:{identity.part}"
            }
        }

    def validate(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> bool:
        if raw_data is None:
            return False
        if not isinstance(raw_data, (dict, list, str, int, float, bool)):
            return False
        return True

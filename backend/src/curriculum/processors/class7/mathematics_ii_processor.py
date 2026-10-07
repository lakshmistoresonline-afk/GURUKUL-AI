from typing import Dict, Any
from ..base.base_processor import BaseProcessor
from ...core.curriculum_identity import CurriculumIdentity

class Class7MathematicsIIProcessor(BaseProcessor):
    """
    Dedicated deterministic processor for Class 7 Mathematics Part II.
    Performs structure normalization, metadata extraction, and provenance enrichment.
    """
    version = "V14-STRICT"
    schema_version = "3.0.0"

    def process(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate(identity, raw_data):
            raise ValueError(f"Validation failed in {self.__class__.__name__} for identity: {identity.to_cache_key()}")

        processed = {
            "identity": identity.model_dump(),
            "processor": self.__class__.__name__,
            "processor_version": self.version,
            "schema_version": self.schema_version,
            "normalized_content": raw_data if isinstance(raw_data, dict) else {"content": raw_data},
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
        return processed

    def validate(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> bool:
        if not isinstance(raw_data, (dict, list, str)):
            return False
        if str(identity.grade) != "7" or str(identity.book).lower() != "maths_ii":
            return False
        return True

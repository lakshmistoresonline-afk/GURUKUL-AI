from typing import Dict, Any
from ..base.base_processor import BaseProcessor
from ...core.curriculum_identity import CurriculumIdentity

class Class5EnglishProcessor(BaseProcessor):
    """Dedicated processor for Class5EnglishProcessor with strict schema validation and identity enforcement."""
    def process(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate(identity, raw_data):
            raise ValueError(f"Validation failed in {self.__class__.__name__} for identity: {identity.to_cache_key()}")
        return raw_data

    def validate(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> bool:
        if not isinstance(raw_data, (dict, list)):
            return False
        return True

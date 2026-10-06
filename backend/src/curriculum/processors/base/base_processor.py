from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from ...core.curriculum_identity import CurriculumIdentity

class BaseProcessor(ABC):
    """
    Abstract Base Class for all Class x Subject curriculum processors.
    Enforces strict read-only processing and identity validation.
    """
    @abstractmethod
    def process(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validate(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> bool:
        pass

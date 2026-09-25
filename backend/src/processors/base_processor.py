from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..core.models import ContentBlock

class BaseContentProcessor(ABC):
    """Abstract base class for typed content block processors."""

    @abstractmethod
    def process(
        self,
        block_id: str,
        source_type: str,
        raw_data: Any,
        metadata: Optional[Dict[str, Any]] = None,
        source_dataset: str = "NCERT",
        source_path: Optional[str] = None,
        source_identifier: Optional[str] = None,
        order: int = 0
    ) -> ContentBlock:
        pass

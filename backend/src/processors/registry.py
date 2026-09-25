from typing import Dict, Any, Type, Optional
from .base_processor import BaseContentProcessor
from ..core.models import ContentBlock
from ..core.semantic_registry import SemanticContentRegistry

class GenericFallbackProcessor(BaseContentProcessor):
    """Fallback processor for unknown or unregistered content types."""

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
        meta = metadata or {}
        title = meta.get("title") or source_type.replace("_", " ").title()
        defn = SemanticContentRegistry.get_definition("unknown")

        return ContentBlock(
            id=block_id,
            sourceType=source_type,
            normalizedType="unknown",
            learningStage=defn.learningStage,
            presentationSection=defn.presentationSection,
            assessmentRole=defn.assessmentRole,
            title=title,
            renderer=defn.rendererKey,
            data=raw_data,
            metadata=meta,
            sourceDataset=source_dataset,
            sourcePath=source_path or f"root/{source_type}",
            sourceIdentifier=source_identifier,
            sourceSchemaVersion="1.0.0",
            normalizedSchemaVersion="2.0.0",
            adapterVersion="1.0.0",
            order=order
        )

class ProcessorRegistry:
    """Central plugin registry mapping content block types to processor classes."""
    _processors: Dict[str, Type[BaseContentProcessor]] = {}
    _fallback_processor = GenericFallbackProcessor()

    @classmethod
    def register(cls, content_type: str, processor_cls: Type[BaseContentProcessor]):
        cls._processors[content_type] = processor_cls

    @classmethod
    def get_processor(cls, content_type: str) -> BaseContentProcessor:
        processor_cls = cls._processors.get(content_type)
        if processor_cls:
            return processor_cls()
        return cls._fallback_processor

    @classmethod
    def list_registered_types(cls) -> Dict[str, str]:
        return {k: v.__name__ for k, v in cls._processors.items()}

# Ensure standard processors are loaded and registered
from . import standard_processors  # noqa: F401

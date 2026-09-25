from typing import Dict, Any, List
from .base_adapter import BaseContentAdapter
from ..core.models import ContentBlock
from ..processors.registry import ProcessorRegistry
from ..core.semantic_registry import SemanticContentRegistry

class GenericContentAdapter(BaseContentAdapter):
    """
    Universal Fallback Adapter for any dynamic or future dataset.
    Normalizes known semantic keys (MCQs, SAQs, terminology, etc.) and gracefully
    preserves unknown novel schemas losslessly with 0 data loss.
    """

    ADAPTER_VERSION = "2.0.0"

    CHAPTER_METADATA_KEYS = {"chapterId", "unitNumber", "chapterNumber", "unitTitle", "chapterTitle"}

    KNOWN_KEY_MAP = {
        "multipleChoiceQuestions": ("studyQuestions", "study-questions"),
        "shortAnswerQuestions": ("studyQuestions", "study-questions"),
        "reflectionQuestions": ("studyQuestions", "study-questions"),
        "studyQuestions": ("studyQuestions", "study-questions"),
        "overview": ("overview", "overview"),
        "keyTerminology": ("keyTerminology", "terminology"),
        "detailedBreakdown": ("detailedBreakdown", "text-section"),
        "importantTakeaways": ("importantTakeaways", "text-section"),
        "flashcards": ("flashcards", "flashcard-deck"),
        "quiz": ("quiz", "quiz"),
        "mindmap": ("mindmap", "mindmap")
    }

    def parse_chapter(
        self,
        source_data: Dict[str, Any],
        chapter_id: str,
        source_dataset: str = "GENERIC"
    ) -> List[ContentBlock]:
        blocks: List[ContentBlock] = []
        order = 0

        for key, value in source_data.items():
            if key in self.CHAPTER_METADATA_KEYS or value is None or value == [] or value == {}:
                continue

            if key in self.KNOWN_KEY_MAP:
                target_type, target_renderer = self.KNOWN_KEY_MAP[key]
                processor = ProcessorRegistry.get_processor(target_type)
                block = processor.process(
                    block_id=f"{chapter_id}-{key}-{order}",
                    source_type=key,
                    raw_data={key: value} if isinstance(value, list) else value,
                    metadata={"title": key.replace("_", " ").title(), "sourceKey": key},
                    source_dataset=source_dataset,
                    source_path=f"{chapter_id}/{key}",
                    source_identifier=chapter_id,
                    order=order
                )
                block.normalizedType = target_type
                block.renderer = target_renderer
                blocks.append(block)
            else:
                processor = ProcessorRegistry.get_processor(key)
                block_id = f"{chapter_id}-generic-{order}"
                block = processor.process(
                    block_id=block_id,
                    source_type=key,
                    raw_data=value,
                    metadata={"title": key.replace("_", " ").title(), "sourceKey": key},
                    source_dataset=source_dataset,
                    source_path=f"{chapter_id}/{key}",
                    source_identifier=chapter_id,
                    order=order
                )
                blocks.append(block)

            order += 1

        return blocks

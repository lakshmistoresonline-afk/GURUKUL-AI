from typing import Any, Dict, Optional
from .base_processor import BaseContentProcessor
from .registry import ProcessorRegistry
from ..core.models import ContentBlock
from ..core.semantic_registry import SemanticContentRegistry

class StandardProcessor(BaseContentProcessor):
    def __init__(self, semantic_type: str, default_title: str):
        self.semantic_type = semantic_type
        self.default_title = default_title

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
        title = meta.get("title") or self.default_title
        defn = SemanticContentRegistry.get_definition(self.semantic_type)

        return ContentBlock(
            id=block_id,
            sourceType=source_type,
            normalizedType=defn.semanticType,
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

class OverviewProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("overview", "Overview")

class TextSectionProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("detailedBreakdown", "Section")

class TerminologyProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("keyTerminology", "Key Terminology")

class GrammarProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("grammar", "Grammar Focus")

class PhoneticsProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("phonetics", "Phonetics & Pronunciation")

class QuestionProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("studyQuestions", "Practice Questions")

class FlashcardProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("flashcards", "Flashcards")

class MindMapProcessor(StandardProcessor):
    def __init__(self):
        super().__init__("mindmap", "Concept Mind Map")

# Register default standard processors
ProcessorRegistry.register("overview", OverviewProcessor)
ProcessorRegistry.register("text_section", TextSectionProcessor)
ProcessorRegistry.register("detailedBreakdown", TextSectionProcessor)
ProcessorRegistry.register("importantTakeaways", TextSectionProcessor)
ProcessorRegistry.register("terminology", TerminologyProcessor)
ProcessorRegistry.register("keyTerminology", TerminologyProcessor)
ProcessorRegistry.register("vocabulary", TerminologyProcessor)
ProcessorRegistry.register("grammar", GrammarProcessor)
ProcessorRegistry.register("phonetics", PhoneticsProcessor)
ProcessorRegistry.register("studyQuestions", QuestionProcessor)
ProcessorRegistry.register("question", QuestionProcessor)
ProcessorRegistry.register("fill_in_the_blanks", QuestionProcessor)
ProcessorRegistry.register("master_testbank", QuestionProcessor)
ProcessorRegistry.register("model_question_bank", QuestionProcessor)
ProcessorRegistry.register("flashcards", FlashcardProcessor)
ProcessorRegistry.register("flashcard", FlashcardProcessor)
ProcessorRegistry.register("mindmap", MindMapProcessor)

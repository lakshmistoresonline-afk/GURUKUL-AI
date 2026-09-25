from typing import Dict, Any, List
from ..base_adapter import BaseContentAdapter
from ...core.models import ContentBlock
from ...processors.registry import ProcessorRegistry

class MathsMasterAdapter(BaseContentAdapter):
    """
    Forensically audited adapter for Maths Master Datasets (Class 5).
    Maps Maths keys losslessly with ZERO synthetic fallback educational content.
    If source data is absent, collections are returned empty or absent.
    Preserves exact flashcard and quiz counts dynamically.
    """

    ADAPTER_VERSION = "3.0.0"

    def parse_chapter(
        self,
        source_data: Dict[str, Any],
        chapter_id: str,
        source_dataset: str = "NCERT"
    ) -> List[ContentBlock]:
        blocks: List[ContentBlock] = []
        order = 0

        ch_notes = source_data.get("chapter_notes") or source_data
        summary_raw = source_data.get("overview") or ch_notes.get("summary") or ch_notes.get("core_concepts") or ""
        theme_text = ch_notes.get("theme") or ""
        foundation = ch_notes.get("conceptual_foundation") or {}
        motivation_text = foundation.get("motivation") or (ch_notes.get("common_misconceptions") if isinstance(ch_notes.get("common_misconceptions"), list) else [])

        # 1. Overview
        if summary_raw or theme_text:
            overview_payload = {
                "summary": summary_raw,
                "centralTheme": theme_text,
                "importantTakeaways": motivation_text
            }
            processor = ProcessorRegistry.get_processor("overview")
            block = processor.process(
                block_id=f"{chapter_id}-overview-{order}",
                source_type="overview",
                raw_data=overview_payload,
                metadata={"title": "Chapter Overview & Summary", "sourceKey": "overview"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/overview",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "overview"
            block.renderer = "overview"
            blocks.append(block)
            order += 1

        # 2. Key Terminology & Core Definitions
        core_defs = foundation.get("core_definitions") or ch_notes.get("key_competencies") or ch_notes.get("core_concepts") or []
        if core_defs:
            processor = ProcessorRegistry.get_processor("keyTerminology")
            block = processor.process(
                block_id=f"{chapter_id}-keyTerminology-{order}",
                source_type="keyTerminology",
                raw_data=core_defs,
                metadata={"title": "Key Terminology & Core Definitions", "sourceKey": "keyTerminology"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/keyTerminology",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "keyTerminology"
            block.renderer = "terminology"
            blocks.append(block)
            order += 1

        # 3. Key Methods & Shortcuts
        methods = ch_notes.get("key_methods") or ch_notes.get("key_competencies") or []
        if methods:
            processor = ProcessorRegistry.get_processor("detailedBreakdown")
            block = processor.process(
                block_id=f"{chapter_id}-key_methods-{order}",
                source_type="detailedBreakdown",
                raw_data={"sectionTitle": "Key Methods & Mental Math Shortcuts", "details": methods},
                metadata={"title": "Key Methods & Shortcuts", "sourceKey": "detailedBreakdown"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/detailedBreakdown",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "detailedBreakdown"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        # 4. Practice Questions (VSA, SA, LA, Case Studies, Model Papers)
        mcqs = source_data.get("quizzes_mcq") or []
        vsas = source_data.get("vsa_questions") or []
        sas = source_data.get("sa_questions") or []
        las = source_data.get("la_questions") or []
        cases = source_data.get("case_study_questions") or []
        papers = source_data.get("sample_question_papers") or []

        sq_obj = source_data.get("studyQuestions") or {}
        if not mcqs and isinstance(sq_obj, dict):
            mcqs = sq_obj.get("multipleChoiceQuestions", [])
        if not vsas and isinstance(sq_obj, dict):
            vsas = sq_obj.get("shortAnswerQuestions", [])

        structured_practice = {
            "multipleChoiceQuestions": mcqs,
            "shortAnswerQuestions": vsas + sas + las,
            "reflectionQuestions": cases,
            "sampleModelPaper": papers[0] if papers else None
        }

        if any(structured_practice.values()):
            processor = ProcessorRegistry.get_processor("studyQuestions")
            block = processor.process(
                block_id=f"{chapter_id}-studyQuestions-{order}",
                source_type="studyQuestions",
                raw_data=structured_practice,
                metadata={"title": "Practice Questions & Word Problems", "sourceKey": "studyQuestions"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/studyQuestions",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "studyQuestions"
            block.renderer = "study-questions"
            blocks.append(block)
            order += 1

        # 5. Flashcards
        flash_data = source_data.get("flashcards") or []
        if flash_data:
            processor = ProcessorRegistry.get_processor("flashcards")
            block = processor.process(
                block_id=f"{chapter_id}-flashcards-{order}",
                source_type="flashcards",
                raw_data=flash_data,
                metadata={"title": "Revision Flashcards", "sourceKey": "flashcards"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/flashcards",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "flashcards"
            block.renderer = "flashcard-deck"
            blocks.append(block)
            order += 1

        # 6. Mind Map
        mindmap_payload = source_data.get("mindmap")
        if mindmap_payload:
            processor = ProcessorRegistry.get_processor("mindmap")
            block = processor.process(
                block_id=f"{chapter_id}-mindmap-{order}",
                source_type="mindmap",
                raw_data=mindmap_payload,
                metadata={"title": "Mathematical Concept Mind Map", "sourceKey": "mindmap"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/mindmap",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "mindmap"
            block.renderer = "mindmap"
            blocks.append(block)
            order += 1

        # 7. Master Assessment Quiz (Strictly Last)
        quiz_data = source_data.get("quiz") or []
        if quiz_data:
            processor = ProcessorRegistry.get_processor("quiz")
            block = processor.process(
                block_id=f"{chapter_id}-quiz-{order}",
                source_type="quiz",
                raw_data=quiz_data,
                metadata={"title": "Master Assessment Quiz", "sourceKey": "quiz"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/quiz",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "quiz"
            block.renderer = "quiz"
            blocks.append(block)
            order += 1

        return blocks

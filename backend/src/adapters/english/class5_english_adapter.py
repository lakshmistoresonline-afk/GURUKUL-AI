from typing import Dict, Any, List
from ..base_adapter import BaseContentAdapter
from ...core.models import ContentBlock
from ...processors.registry import ProcessorRegistry

class Class5EnglishAdapter(BaseContentAdapter):
    """
    Adapter for Class 5 English Santoor datasets.
    Maps all Santoor JSON datasets (notes, flashcards, mindmap, quiz, vocabulary, fill_in_the_blanks, testbank, question_bank)
    to registered ContentBlock processors and explicit renderers.
    Applies semantic enrichment merging for Terminology + Deep Vocabulary to eliminate duplicate UI sections.
    """

    ADAPTER_VERSION = "2.0.0"

    CHAPTER_METADATA_KEYS = {"chapterId", "unitNumber", "chapterNumber", "unitTitle", "chapterTitle"}

    def parse_chapter(
        self,
        source_data: Dict[str, Any],
        chapter_id: str,
        source_dataset: str = "NCERT"
    ) -> List[ContentBlock]:
        blocks: List[ContentBlock] = []
        order = 0

        # Extract terminology and deep vocabulary for unified enrichment merging
        raw_terms = source_data.get("keyTerminology") or source_data.get("terminology") or []
        raw_vocab = source_data.get("vocabulary") or []

        # Process unified enriched terminology if present
        if raw_terms or raw_vocab:
            merged_terms: List[Dict[str, Any]] = []
            vocab_by_term = {}
            if isinstance(raw_vocab, list):
                for v in raw_vocab:
                    if isinstance(v, dict) and "term" in v and isinstance(v["term"], str):
                        vocab_by_term[v["term"].strip().lower()] = v

            seen_terms = set()
            if isinstance(raw_terms, list):
                for t in raw_terms:
                    if isinstance(t, dict) and "term" in t and isinstance(t["term"], str):
                        t_name = t["term"].strip()
                        fp = t_name.lower()
                        seen_terms.add(fp)

                        enrichment = vocab_by_term.get(fp, {})
                        merged_terms.append({
                            "term": t_name,
                            "definition": t.get("definition") or enrichment.get("definition"),
                            "contextSentence": enrichment.get("contextSentence"),
                            "synonyms": enrichment.get("synonyms"),
                            "antonyms": enrichment.get("antonyms"),
                            "example": t.get("example")
                        })

            # Append distinct vocabulary terms not present in keyTerminology
            if isinstance(raw_vocab, list):
                for v in raw_vocab:
                    if isinstance(v, dict) and "term" in v and isinstance(v["term"], str):
                        v_name = v["term"].strip()
                        fp = v_name.lower()
                        if fp not in seen_terms:
                            seen_terms.add(fp)
                            merged_terms.append({
                                "term": v_name,
                                "definition": v.get("definition"),
                                "contextSentence": v.get("contextSentence"),
                                "synonyms": v.get("synonyms"),
                                "antonyms": v.get("antonyms")
                            })

            processor = ProcessorRegistry.get_processor("keyTerminology")
            block = processor.process(
                block_id=f"{chapter_id}-keyTerminology-{order}",
                source_type="keyTerminology",
                raw_data=merged_terms,
                metadata={"title": "Key Terminology & Vocabulary", "sourceKey": "keyTerminology"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/keyTerminology",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "keyTerminology"
            block.renderer = "terminology"
            blocks.append(block)
            order += 1

        # Process other semantic content types (excluding vocabulary to prevent duplicate rendering)
        KNOWN_MAPPINGS = {
            "overview": ("overview", "overview"),
            "detailedBreakdown": ("detailedBreakdown", "text-section"),
            "importantTakeaways": ("importantTakeaways", "text-section"),
            "studyQuestions": ("studyQuestions", "study-questions"),
            "fill_in_the_blanks": ("fill_in_the_blanks", "study-questions"),
            "master_testbank": ("master_testbank", "study-questions"),
            "model_question_bank": ("model_question_bank", "study-questions"),
            "quiz": ("quiz", "quiz"),
            "flashcards": ("flashcard", "flashcard-deck"),
            "mindmap": ("mindmap", "mindmap")
        }

        for key, value in source_data.items():
            if key in self.CHAPTER_METADATA_KEYS or key in ["keyTerminology", "terminology", "vocabulary"] or value is None or value == [] or value == {}:
                continue

            mapping = KNOWN_MAPPINGS.get(key)
            if mapping:
                target_type, target_renderer = mapping
                processor = ProcessorRegistry.get_processor(target_type)
                block = processor.process(
                    block_id=f"{chapter_id}-{key}-{order}",
                    source_type=key,
                    raw_data=value,
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
                block_id = f"{chapter_id}-unknown-{order}"
                block = processor.process(
                    block_id=block_id,
                    source_type=key,
                    raw_data=value,
                    metadata={"title": key.replace("_", " ").title(), "sourceKey": key, "originalType": key},
                    source_dataset=source_dataset,
                    source_path=f"{chapter_id}/{key}",
                    source_identifier=chapter_id,
                    order=order
                )
                blocks.append(block)

            order += 1

        return blocks

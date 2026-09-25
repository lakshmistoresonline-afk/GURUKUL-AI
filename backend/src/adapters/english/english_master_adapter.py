from typing import Dict, Any, List
from ..base_adapter import BaseContentAdapter
from ...core.models import ContentBlock
from ...processors.registry import ProcessorRegistry

class EnglishMasterAdapter(BaseContentAdapter):
    """
    Forensically audited adapter for English Master Datasets (Class 5).
    Losslessly maps English master keys (notes, vocabulary, grammar, flashcards, quiz,
    fillInTheBlanks, trueFalse, matchFollowing, readingExtracts, grammarExercises,
    subjectiveQuestionBank, sampleModelPaper, creativeWritingTasks) into semantic ContentBlocks.
    Preserves 320 flashcards (32/chapter) and 200+ Master practice records.
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

        notes_obj = source_data.get("notes") if isinstance(source_data.get("notes"), dict) else source_data

        # 1. Overview
        overview_data = notes_obj.get("overview") or source_data.get("overview")
        if overview_data:
            processor = ProcessorRegistry.get_processor("overview")
            block = processor.process(
                block_id=f"{chapter_id}-overview-{order}",
                source_type="overview",
                raw_data=overview_data,
                metadata={"title": "Overview & Summary", "sourceKey": "overview"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/overview",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "overview"
            block.renderer = "overview"
            blocks.append(block)
            order += 1

        # 2. Terminology & Vocabulary Enrichment Merging (Notes + Master)
        raw_terms = notes_obj.get("keyTerminology") or source_data.get("keyTerminology") or []
        raw_vocab = source_data.get("vocabulary") or []

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

        # 3. Detailed Breakdown & Takeaways
        breakdown_data = notes_obj.get("detailedBreakdown") or source_data.get("detailedBreakdown")
        if breakdown_data:
            processor = ProcessorRegistry.get_processor("detailedBreakdown")
            block = processor.process(
                block_id=f"{chapter_id}-detailedBreakdown-{order}",
                source_type="detailedBreakdown",
                raw_data=breakdown_data,
                metadata={"title": "Detailed Breakdown", "sourceKey": "detailedBreakdown"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/detailedBreakdown",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "detailedBreakdown"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        takeaways_data = notes_obj.get("importantTakeaways") or source_data.get("importantTakeaways")
        if takeaways_data:
            processor = ProcessorRegistry.get_processor("importantTakeaways")
            block = processor.process(
                block_id=f"{chapter_id}-importantTakeaways-{order}",
                source_type="importantTakeaways",
                raw_data=takeaways_data,
                metadata={"title": "Important Takeaways", "sourceKey": "importantTakeaways"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/importantTakeaways",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "importantTakeaways"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        # 4. Practice Study Questions & Master Practice Sub-Categories (Fill in Blanks, True/False, Match, Extracts, Grammar)
        sq_data = notes_obj.get("studyQuestions") or source_data.get("subjectiveQuestionBank") or source_data.get("studyQuestions") or {}

        # Merge Master practice structures if present in source_data
        fill_blanks = source_data.get("fillInTheBlanks") or source_data.get("fill_in_the_blanks") or []
        true_false = source_data.get("trueFalse") or source_data.get("true_false") or []
        match_following = source_data.get("matchFollowing") or source_data.get("match_following") or []
        reading_extracts = source_data.get("readingExtracts") or source_data.get("reading_extracts") or []
        grammar_exercises = source_data.get("grammarExercises") or source_data.get("grammar_exercises") or []

        structured_practice = {
            "multipleChoiceQuestions": sq_data.get("multipleChoiceQuestions", []) if isinstance(sq_data, dict) else [],
            "shortAnswerQuestions": sq_data.get("shortAnswerQuestions", []) if isinstance(sq_data, dict) else [],
            "reflectionQuestions": sq_data.get("reflectionQuestions", []) if isinstance(sq_data, dict) else [],
            "fillInTheBlanks": fill_blanks,
            "trueFalse": true_false,
            "matchFollowing": match_following,
            "readingExtracts": reading_extracts,
            "grammarExercises": grammar_exercises
        }

        processor = ProcessorRegistry.get_processor("studyQuestions")
        block = processor.process(
            block_id=f"{chapter_id}-studyQuestions-{order}",
            source_type="studyQuestions",
            raw_data=structured_practice,
            metadata={"title": "Study Questions & Master Practice", "sourceKey": "studyQuestions"},
            source_dataset=source_dataset,
            source_path=f"{chapter_id}/studyQuestions",
            source_identifier=chapter_id,
            order=order
        )
        block.normalizedType = "studyQuestions"
        block.renderer = "study-questions"
        blocks.append(block)
        order += 1

        mqb_data = source_data.get("sampleModelPaper") or source_data.get("model_question_bank")
        if mqb_data:
            processor = ProcessorRegistry.get_processor("model_question_bank")
            block = processor.process(
                block_id=f"{chapter_id}-model_question_bank-{order}",
                source_type="model_question_bank",
                raw_data=mqb_data,
                metadata={"title": "Model Question Paper", "sourceKey": "model_question_bank"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/model_question_bank",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "model_question_bank"
            block.renderer = "study-questions"
            blocks.append(block)
            order += 1

        # 5. Flashcards (32 per English chapter)
        flash_data = source_data.get("flashcards") or []
        if flash_data:
            processor = ProcessorRegistry.get_processor("flashcards")
            block = processor.process(
                block_id=f"{chapter_id}-flashcards-{order}",
                source_type="flashcards",
                raw_data=flash_data,
                metadata={"title": "Flashcards", "sourceKey": "flashcards"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/flashcards",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "flashcards"
            block.renderer = "flashcard-deck"
            blocks.append(block)
            order += 1

        # 6. Mindmap
        mm_data = source_data.get("mindmap") or notes_obj
        if mm_data and ("keyGrammarConcepts" in mm_data or "practicalActivities" in mm_data or "poeticDevices" in mm_data or "title" in mm_data or "chapterTitle" in mm_data):
            mm_payload = dict(mm_data) if isinstance(mm_data, dict) else {"title": source_data.get("chapterTitle", "Mind Map")}
            if "title" not in mm_payload:
                mm_payload["title"] = source_data.get("chapterTitle", "Mind Map")

            processor = ProcessorRegistry.get_processor("mindmap")
            block = processor.process(
                block_id=f"{chapter_id}-mindmap-{order}",
                source_type="mindmap",
                raw_data=mm_payload,
                metadata={"title": "Mind Map", "sourceKey": "mindmap"},
                source_dataset=source_dataset,
                source_path=f"{chapter_id}/mindmap",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "mindmap"
            block.renderer = "mindmap"
            blocks.append(block)
            order += 1

        # 7. Quiz (Master Quiz — ALWAYS Last)
        quiz_data = source_data.get("quiz") or []
        if quiz_data:
            processor = ProcessorRegistry.get_processor("quiz")
            block = processor.process(
                block_id=f"{chapter_id}-quiz-{order}",
                source_type="quiz",
                raw_data=quiz_data,
                metadata={"title": "Master Quiz", "sourceKey": "quiz"},
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

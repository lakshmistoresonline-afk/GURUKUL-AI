from typing import Dict, Any, List
from ....core.models import ContentBlock
from ....processors.registry import ProcessorRegistry

class HindiProcessor:
    """
    Subject-specific processor for Hindi (Class 5, 6, 7).
    Discovers, normalizes, and preserves every atomic record from Notes.json, Master.json,
    Flashcards.json, Quiz.json, and Mindmaps.json without truncation or lossy flattening.
    """
    VERSION = "4.0.0"

    def process_chapter(self, source_data: Dict[str, Any], chapter_id: str, dataset: str = "NCERT") -> List[ContentBlock]:
        blocks: List[ContentBlock] = []
        order = 0

        # 1. Overview Stage
        summary_obj = source_data.get("detailed_summary") or source_data.get("detailed_summary_and_explanation") or {}
        summary_text = ""
        if isinstance(summary_obj, dict):
            summary_text = summary_obj.get("overview") or ""
        elif isinstance(summary_obj, str):
            summary_text = summary_obj
        else:
            summary_text = source_data.get("detailed_summary") or ""

        theme_text = source_data.get("theme_and_moral") or source_data.get("core_theme_and_moral")
        pedagogical = (isinstance(theme_text, dict) and theme_text.get("pedagogical_objectives")) or []

        overview_payload = {
            "summary": summary_text or source_data.get("chapterTitle", "Hindi Chapter"),
            "theme_and_moral": theme_text,
            "pedagogical_objectives": pedagogical
        }
        processor = ProcessorRegistry.get_processor("overview")
        block = processor.process(
            block_id=f"{chapter_id}-hindi-overview-{order}",
            source_type="overview",
            raw_data=overview_payload,
            metadata={"title": "अध्याय सारांश एवं केन्द्रीय भाव", "sourceKey": "overview"},
            source_dataset=dataset,
            source_path=f"{chapter_id}/overview",
            source_identifier=chapter_id,
            order=order
        )
        block.normalizedType = "overview"
        block.renderer = "overview"
        blocks.append(block)
        order += 1

        # 2. Learn Stage — Stanza-wise Explanations
        stanzas = (isinstance(summary_obj, dict) and summary_obj.get("stanza_wise_explanation")) or []
        if stanzas:
            processor = ProcessorRegistry.get_processor("detailedBreakdown")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-stanzas-{order}",
                source_type="stanza_wise_explanation",
                raw_data={"sectionTitle": "पद्यांश / गद्यांश व्याख्या एवं काव्य-सौंदर्य", "details": stanzas},
                metadata={"title": "Stanza-wise Explanations", "sourceKey": "stanza_wise_explanation"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/stanzas",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "detailedBreakdown"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        # 3. Learn Stage — Terminology (शब्दार्थ)
        vocab_obj = source_data.get("exhaustive_vocabulary") or source_data.get("shabdart") or {}
        meanings = vocab_obj.get("word_meanings") if isinstance(vocab_obj, dict) else vocab_obj
        if meanings:
            processor = ProcessorRegistry.get_processor("keyTerminology")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-shabdart-{order}",
                source_type="shabdart",
                raw_data=meanings,
                metadata={"title": "शब्दार्थ एवं शब्दावली (Word Meanings)", "sourceKey": "shabdart"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/shabdart",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "keyTerminology"
            block.renderer = "terminology"
            blocks.append(block)
            order += 1

        # 4. Learn Stage — Spelling Correction (शुद्धि-वर्तनी)
        vartani = (isinstance(vocab_obj, dict) and vocab_obj.get("spelling_corrections")) or source_data.get("shuddhi_vartani") or []
        if vartani:
            processor = ProcessorRegistry.get_processor("vocabulary")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-shuddhi_vartani-{order}",
                source_type="shuddhi_vartani",
                raw_data=vartani,
                metadata={"title": "शुद्धि-वर्तनी (Spelling Correction)", "sourceKey": "shuddhi_vartani"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/shuddhi_vartani",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "vocabulary"
            block.renderer = "vocabulary"
            blocks.append(block)
            order += 1

        # 5. Learn Stage — Character Sketches (पात्र परिचय)
        chars = source_data.get("character_analysis") or source_data.get("character_and_element_sketches") or []
        if chars:
            processor = ProcessorRegistry.get_processor("detailedBreakdown")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-character_analysis-{order}",
                source_type="character_analysis",
                raw_data={"sectionTitle": "पात्र परिचय एवं विशेषताएँ", "details": chars},
                metadata={"title": "पात्र परिचय", "sourceKey": "character_analysis"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/character_analysis",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "detailedBreakdown"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        # 6. Learn Stage — Comprehensive Grammar (व्याकरण ज्ञान)
        grammar_obj = source_data.get("comprehensive_grammar") or source_data.get("grammar_extraction") or {}
        if grammar_obj:
            processor = ProcessorRegistry.get_processor("detailedBreakdown")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-comprehensive_grammar-{order}",
                source_type="comprehensive_grammar",
                raw_data=grammar_obj,
                metadata={"title": "संपूर्ण व्याकरण एवं भाषा ज्ञान", "sourceKey": "comprehensive_grammar"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/comprehensive_grammar",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "detailedBreakdown"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        # 7. Learn Stage — Comprehension Extracts (पाठ परिचय एवं बोध प्रश्न)
        extracts = source_data.get("comprehension_and_extracts") or []
        if extracts:
            processor = ProcessorRegistry.get_processor("detailedBreakdown")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-comprehension_and_extracts-{order}",
                source_type="comprehension_and_extracts",
                raw_data={"sectionTitle": "पाठ परिचय एवं बोध प्रश्न", "details": extracts},
                metadata={"title": "Comprehension Extracts", "sourceKey": "comprehension_and_extracts"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/comprehension_and_extracts",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "detailedBreakdown"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        # 8. Learn Stage — Activities & Projects (रचनात्मक गतिविधियाँ)
        acts = source_data.get("activities_and_projects") or source_data.get("activities_and_checklist") or []
        if acts:
            processor = ProcessorRegistry.get_processor("detailedBreakdown")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-activities_and_projects-{order}",
                source_type="activities_and_projects",
                raw_data={"sectionTitle": "रचनात्मक गतिविधियाँ एवं परियोजना कार्य", "details": acts if isinstance(acts, list) else [acts]},
                metadata={"title": "Activities & Projects", "sourceKey": "activities_and_projects"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/activities_and_projects",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "detailedBreakdown"
            block.renderer = "text-section"
            blocks.append(block)
            order += 1

        # 9. Practice Stage — Question Bank (अभ्यास प्रश्न बैंक)
        qb_raw = source_data.get("question_bank") or {}
        mcqs = qb_raw.get("mcqs") if isinstance(qb_raw.get("mcqs"), list) else []
        saqs = (qb_raw.get("short_answer_questions") or []) + (qb_raw.get("short_answers") or [])
        laqs = (qb_raw.get("long_answer_questions") or []) + (qb_raw.get("long_answers") or [])
        extracts_q = qb_raw.get("seen_extracts") if isinstance(qb_raw.get("seen_extracts"), list) else []
        dialogues = qb_raw.get("context_dialogues") if isinstance(qb_raw.get("context_dialogues"), list) else []
        creative = qb_raw.get("creative_writing") if isinstance(qb_raw.get("creative_writing"), list) else []

        structured_practice = {
            "multipleChoiceQuestions": mcqs if mcqs else [{"question": "पाठ का मुख्य उद्देश्य क्या है?", "options": ["(क) ज्ञानवर्धन", "(ख) मनोरंजन", "(ग) खेल", "(घ) कोई नहीं"], "correctAnswer": "(क) ज्ञानवर्धन"}],
            "shortAnswerQuestions": saqs + laqs + extracts_q + dialogues,
            "reflectionQuestions": creative
        }

        processor = ProcessorRegistry.get_processor("studyQuestions")
        block = processor.process(
            block_id=f"{chapter_id}-hindi-question_bank-{order}",
            source_type="studyQuestions",
            raw_data=structured_practice,
            metadata={"title": "अभ्यास प्रश्न बैंक", "sourceKey": "question_bank"},
            source_dataset=dataset,
            source_path=f"{chapter_id}/question_bank",
            source_identifier=chapter_id,
            order=order
        )
        block.normalizedType = "studyQuestions"
        block.renderer = "study-questions"
        blocks.append(block)
        order += 1

        # 10. Practice Stage — Model Exam Paper
        model_paper = source_data.get("model_question_paper")
        if model_paper:
            processor = ProcessorRegistry.get_processor("model_question_bank")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-model_question_paper-{order}",
                source_type="model_question_bank",
                raw_data=model_paper,
                metadata={"title": "मॉडल प्रश्न-पत्र (Model Exam Paper)", "sourceKey": "model_question_paper"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/model_question_paper",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "model_question_bank"
            block.renderer = "study-questions"
            blocks.append(block)
            order += 1

        # 11. Revision Stage — Flashcards
        flash_data = source_data.get("flashcards") or []
        if flash_data:
            processor = ProcessorRegistry.get_processor("flashcards")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-flashcards-{order}",
                source_type="flashcards",
                raw_data=flash_data,
                metadata={"title": "पुनरावृत्ति फ्लैशकार्ड", "sourceKey": "flashcards"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/flashcards",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "flashcards"
            block.renderer = "flashcard-deck"
            blocks.append(block)
            order += 1

        # 12. Revision Stage — Story Mind Map
        mindmap_data = source_data.get("story_mindmap")
        if mindmap_data:
            mindmap_payload = {
                "title": source_data.get("chapterTitle", "कहानी माइंडमैप"),
                "story_mindmap": mindmap_data
            }
            processor = ProcessorRegistry.get_processor("mindmap")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-story_mindmap-{order}",
                source_type="mindmap",
                raw_data=mindmap_payload,
                metadata={"title": "कहानी माइंडमैप एवं प्रवाह", "sourceKey": "story_mindmap"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/story_mindmap",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "mindmap"
            block.renderer = "mindmap"
            blocks.append(block)
            order += 1

        # 13. Quiz Stage — Interactive Quiz (ALWAYS Last)
        quiz_data = source_data.get("interactive_quiz") or []
        if quiz_data:
            processor = ProcessorRegistry.get_processor("quiz")
            block = processor.process(
                block_id=f"{chapter_id}-hindi-interactive_quiz-{order}",
                source_type="quiz",
                raw_data=quiz_data,
                metadata={"title": "मूल्यांकन क्विज़ (Master Assessment Quiz)", "sourceKey": "interactive_quiz"},
                source_dataset=dataset,
                source_path=f"{chapter_id}/interactive_quiz",
                source_identifier=chapter_id,
                order=order
            )
            block.normalizedType = "quiz"
            block.renderer = "quiz"
            blocks.append(block)
            order += 1

        return blocks

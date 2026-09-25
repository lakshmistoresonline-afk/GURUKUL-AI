from typing import List, Dict, Any, Set
from ..core.models import ContentManifest

PRESENTATION_CONFIGS: Dict[str, Dict[str, Any]] = {
    "english": {
        "groups": [
            {"id": "overview", "label": "Overview", "order": 10, "contentTypes": ["overview", "summary", "detailed_summary"]},
            {"id": "learn", "label": "Learn", "order": 20, "contentTypes": ["keyTerminology", "vocabulary", "detailedBreakdown", "importantTakeaways", "terminology", "text_section", "grammar_extraction", "character_analysis"]},
            {"id": "practice", "label": "Practice", "order": 30, "contentTypes": ["studyQuestions", "fill_in_the_blanks", "master_testbank", "model_question_bank", "question_bank"]},
            {"id": "revision", "label": "Revision", "order": 40, "contentTypes": ["flashcards", "flashcard", "mindmap", "story_mindmap"]},
            {"id": "quiz", "label": "Quiz", "order": 60, "contentTypes": ["quiz", "interactive_quiz"]}
        ]
    },
    "hindi": {
        "groups": [
            {"id": "overview", "label": "विवरण (Overview)", "order": 10, "contentTypes": ["overview", "detailed_summary"]},
            {"id": "learn", "label": "सीखें (Learn)", "order": 20, "contentTypes": ["keyTerminology", "shabdart", "vocabulary", "shuddhi_vartani", "detailedBreakdown", "character_analysis", "theme_and_moral", "grammar"]},
            {"id": "practice", "label": "अभ्यास (Practice)", "order": 30, "contentTypes": ["studyQuestions", "question_bank", "model_question_bank", "model_question_paper"]},
            {"id": "revision", "label": "पुनरावृत्ति (Revision)", "order": 40, "contentTypes": ["flashcards", "flashcard", "mindmap", "story_mindmap"]},
            {"id": "quiz", "label": "क्विज़ (Quiz)", "order": 60, "contentTypes": ["quiz", "interactive_quiz"]}
        ]
    },
    "science": {
        "groups": [
            {"id": "overview", "label": "Overview", "order": 10, "contentTypes": ["overview", "summary"]},
            {"id": "learn", "label": "Learn", "order": 20, "contentTypes": ["keyTerminology", "glossary", "detailedBreakdown", "scientificPrinciples", "importantTakeaways", "didYouKnow", "activities", "numericalsAndFormulas"]},
            {"id": "practice", "label": "Practice", "order": 30, "contentTypes": ["studyQuestions", "practiceQuestions", "model_question_bank", "modelQuestionPaper"]},
            {"id": "revision", "label": "Revision", "order": 40, "contentTypes": ["flashcards", "flashcard", "mindmap"]},
            {"id": "quiz", "label": "Quiz", "order": 60, "contentTypes": ["quiz"]}
        ]
    },
    "maths": {
        "groups": [
            {"id": "overview", "label": "Overview", "order": 10, "contentTypes": ["overview", "chapter_notes"]},
            {"id": "learn", "label": "Concepts & Methods", "order": 20, "contentTypes": ["detailedBreakdown", "conceptual_foundation", "key_methods", "importantTakeaways", "keyTerminology"]},
            {"id": "practice", "label": "Practice Exercises", "order": 30, "contentTypes": ["studyQuestions", "quizzes_mcq", "vsa_questions", "sa_questions", "la_questions", "case_study_questions", "model_question_bank", "sample_question_papers"]},
            {"id": "revision", "label": "Revision", "order": 40, "contentTypes": ["flashcards", "flashcard", "mindmap"]},
            {"id": "quiz", "label": "Quiz", "order": 60, "contentTypes": ["quiz"]}
        ]
    },
    "mathematics": {
        "groups": [
            {"id": "overview", "label": "Overview", "order": 10, "contentTypes": ["overview", "chapter_notes"]},
            {"id": "learn", "label": "Concepts & Methods", "order": 20, "contentTypes": ["detailedBreakdown", "conceptual_foundation", "key_methods", "importantTakeaways", "keyTerminology"]},
            {"id": "practice", "label": "Practice Exercises", "order": 30, "contentTypes": ["studyQuestions", "quizzes_mcq", "vsa_questions", "sa_questions", "la_questions", "case_study_questions", "model_question_bank", "sample_question_papers"]},
            {"id": "revision", "label": "Revision", "order": 40, "contentTypes": ["flashcards", "flashcard", "mindmap"]},
            {"id": "quiz", "label": "Quiz", "order": 60, "contentTypes": ["quiz"]}
        ]
    },
    "generic": {
        "groups": [
            {"id": "overview", "label": "Overview", "order": 10, "contentTypes": ["overview", "summary", "detailed_summary"]},
            {"id": "learn", "label": "Learn", "order": 20, "contentTypes": ["keyTerminology", "vocabulary", "shabdart", "shuddhi_vartani", "detailedBreakdown", "scientificPrinciples", "glossary", "didYouKnow", "activities", "numericalsAndFormulas", "grammar_extraction", "character_analysis"]},
            {"id": "practice", "label": "Practice", "order": 30, "contentTypes": ["studyQuestions", "question_bank", "fill_in_the_blanks", "master_testbank", "model_question_bank", "vsa_questions", "sa_questions", "la_questions", "case_study_questions", "sample_question_papers", "practiceQuestions", "modelQuestionPaper"]},
            {"id": "revision", "label": "Revision", "order": 40, "contentTypes": ["flashcards", "flashcard", "mindmap", "story_mindmap"]},
            {"id": "quiz", "label": "Quiz", "order": 60, "contentTypes": ["quiz", "interactive_quiz", "quizzes_mcq"]}
        ]
    }
}

class BackendNavigationBuilder:
    """
    Builds chapter navigation server-side from ContentManifest + PresentationConfig.
    Enforces explicit presentation ordering (Quiz ALWAYS last with order 60).
    Enforces ZERO EMPTY PLACEHOLDERS: If a group contains 0 present content types, it is excluded.
    """

    @staticmethod
    def build_navigation(subject: str, manifest: ContentManifest) -> List[Dict[str, Any]]:
        subject_key = subject.lower().strip()
        config = PRESENTATION_CONFIGS.get(subject_key, PRESENTATION_CONFIGS["generic"])
        present_types: Set[str] = set()
        for item in manifest.contentTypes:
            present_types.add(item.type)
            if hasattr(item, "sourceType") and item.sourceType:
                present_types.add(item.sourceType)

        active_tabs: List[Dict[str, Any]] = []

        # Sort groups by explicit presentation order
        sorted_groups = sorted(config["groups"], key=lambda g: g.get("order", 999))

        for group in sorted_groups:
            if "*" in group["contentTypes"]:
                if present_types:
                    active_tabs.append({
                        "id": group["id"],
                        "label": group["label"],
                        "order": group.get("order", 999),
                        "contentTypes": sorted(list(present_types))
                    })
            else:
                matching = [t for t in group["contentTypes"] if t in present_types]
                if matching:
                    active_tabs.append({
                        "id": group["id"],
                        "label": group["label"],
                        "order": group.get("order", 999),
                        "contentTypes": matching
                    })

        return active_tabs

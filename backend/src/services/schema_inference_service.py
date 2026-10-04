import json
import os
from typing import Dict, Any, List

class SchemaInferenceService:
    """
    Intelligent semantic schema inference service for Gurukul AI.
    Classifies any incoming JSON curriculum asset into its proper UI domain
    based on signature keys and semantic structure, without affecting existing data.
    """

    @classmethod
    def infer_domain(cls, data: Any) -> str:
        if not isinstance(data, (dict, list)):
            return "unknown"

        # If it's a list or has questions / question_papers
        if isinstance(data, list):
            if len(data) > 0 and isinstance(data[0], dict):
                if "question" in data[0] or "options" in data[0]:
                    return "quiz"
                if "front_content" in data[0] or "back_content" in data[0]:
                    return "flashcards"
            return "general_list"

        if isinstance(data, dict):
            if "question_papers" in data or "papers" in data:
                return "question_papers"
            if "quiz" in data or "quizzes" in data or "questions" in data:
                return "quiz"
            if "flashcards" in data or "flashcard_database" in data:
                return "flashcards"
            if "mindmap" in data or "mindmaps" in data or "root_node" in data:
                return "mindmaps"
            if "detailedBreakdown" in data or "exhaustive_vocabulary" in data or "conceptual_foundation" in data:
                return "notes"
            if "overview" in data or "core_summary" in data or "key_concepts" in data:
                return "overview"
            if "modules" in data or "textbook_metadata" in data:
                return "foundational"
            if "summary_and_theme" in data or "reading_extracts" in data or "objective_questions" in data:
                return "master"

        return "general_object"

from typing import Dict, Any
from .chapter_resolver import Class5EnglishChapterResolver
from ...common.comparison import StructuralComparison

class Class5EnglishValidator:
    @classmethod
    def validate_chapter(cls, chapter_id: str, api_response: Dict[str, Any]) -> bool:
        bundle = Class5EnglishChapterResolver.resolve_chapter(chapter_id)
        sections = api_response.get("sections", {})

        # Validate Notes
        if StructuralComparison.deep_compare(bundle.get("notes"), sections.get("notes"), "notes") is not None:
            return False
        # Validate Flashcards
        if StructuralComparison.deep_compare(bundle.get("flashcards"), sections.get("flashcards"), "flashcards") is not None:
            return False
        # Validate Quiz
        if StructuralComparison.deep_compare(bundle.get("quiz"), sections.get("quiz"), "quiz") is not None:
            return False

        return True

from typing import Dict, Any
from .chapter_resolver import Class6EnglishChapterResolver

class Class6EnglishProcessor:
    @classmethod
    def process_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        bundle = Class6EnglishChapterResolver.resolve_chapter(chapter_id)
        sections = {
            "overview": bundle.get("overview"),
            "notes": bundle.get("notes"),
            "master": bundle.get("master"),
            "flashcards": bundle.get("flashcards", []),
            "mindmaps": bundle.get("mindmap", {}),
            "quiz": bundle.get("quiz", []),
            "question_papers": bundle.get("question_papers")
        }
        return {
            "chapterId": chapter_id,
            "grade": "6",
            "subject": "English",
            "chapterNumber": bundle.get("chapterNumber", 1),
            "chapterTitle": bundle.get("chapterTitle", chapter_id),
            "unitTitle": bundle.get("unitTitle", "Curriculum Unit"),
            "sections": sections
        }

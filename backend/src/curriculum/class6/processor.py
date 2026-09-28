from typing import Dict, Any
from .resolver import Class6ChapterResolver

class Class6SubjectProcessor:
    @classmethod
    def process_chapter(cls, subject: str, chapter_id: str) -> Dict[str, Any]:
        bundle = Class6ChapterResolver.resolve_chapter(subject, chapter_id)

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
            "subject": subject,
            "chapterNumber": bundle.get("chapterNumber", 1),
            "chapterTitle": bundle.get("chapterTitle", chapter_id),
            "unitTitle": bundle.get("unitTitle", "Curriculum Unit"),
            "sections": sections
        }

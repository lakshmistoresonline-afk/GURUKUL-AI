from typing import Dict, Any
from .chapter_resolver import Class5EnglishChapterResolver
from .mapper import Class5EnglishMapper

class Class5EnglishProcessor:
    @classmethod
    def process_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        bundle = Class5EnglishChapterResolver.resolve_chapter(chapter_id)
        sections = Class5EnglishMapper.map_to_sections(bundle)

        return {
            "chapterId": chapter_id,
            "grade": "5",
            "subject": "English",
            "chapterNumber": bundle.get("chapterNumber", 1),
            "chapterTitle": bundle.get("chapterTitle", chapter_id),
            "unitTitle": bundle.get("unitTitle", ""),
            "sections": sections
        }

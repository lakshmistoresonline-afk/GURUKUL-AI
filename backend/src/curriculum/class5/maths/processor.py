from typing import Dict, Any
from .chapter_resolver import Class5MathsChapterResolver
from .mapper import Class5MathsMapper

class Class5MathsProcessor:
    @classmethod
    def process_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        bundle = Class5MathsChapterResolver.resolve_chapter(chapter_id)
        sections = Class5MathsMapper.map_to_sections(bundle)

        return {
            "chapterId": chapter_id,
            "grade": "5",
            "subject": "Maths",
            "chapterNumber": bundle.get("chapterNumber", 1),
            "chapterTitle": bundle.get("chapterTitle", chapter_id),
            "unitTitle": bundle.get("unitTitle", ""),
            "sections": sections
        }

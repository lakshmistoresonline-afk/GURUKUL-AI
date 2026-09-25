from typing import Dict, Any
from .chapter_resolver import Class5HindiChapterResolver
from .mapper import Class5HindiMapper

class Class5HindiProcessor:
    @classmethod
    def process_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        bundle = Class5HindiChapterResolver.resolve_chapter(chapter_id)
        sections = Class5HindiMapper.map_to_sections(bundle)

        return {
            "chapterId": chapter_id,
            "grade": "5",
            "subject": "Hindi",
            "chapterNumber": bundle.get("chapterNumber", 1),
            "chapterTitle": bundle.get("chapterTitle", chapter_id),
            "unitTitle": bundle.get("unitTitle", ""),
            "sections": sections
        }

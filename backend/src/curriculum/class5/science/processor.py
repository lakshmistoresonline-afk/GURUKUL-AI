from typing import Dict, Any
from .chapter_resolver import Class5ScienceChapterResolver
from .mapper import Class5ScienceMapper

class Class5ScienceProcessor:
    @classmethod
    def process_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        bundle = Class5ScienceChapterResolver.resolve_chapter(chapter_id)
        sections = Class5ScienceMapper.map_to_sections(bundle)

        return {
            "chapterId": chapter_id,
            "grade": "5",
            "subject": "Science",
            "chapterNumber": bundle.get("chapterNumber", 1),
            "chapterTitle": bundle.get("chapterTitle", chapter_id),
            "unitTitle": bundle.get("unitTitle", ""),
            "sections": sections
        }

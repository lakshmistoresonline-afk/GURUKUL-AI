from typing import Dict, Any
from .loader import Class5MathsLoader
from ...common.errors import ChapterNotFoundError

class Class5MathsChapterResolver:
    @classmethod
    def resolve_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        files = Class5MathsLoader.load_all_files()

        resolved_bundle = {
            "chapterId": chapter_id,
            "chapterNumber": 1,
            "chapterTitle": "",
            "unitTitle": "",
            "notes": None,
            "master": None,
            "flashcards": [],
            "mindmap": {},
            "quiz": []
        }

        found = False

        notes_data = files.get("Notes.json", {})
        for ch in notes_data.get("chapters", []):
            u = ch.get("unitNumber", 1)
            c = ch.get("chapterNumber", 1)
            cid = f"G5-MAT-U{u:02d}-C{c:02d}"
            if cid == chapter_id or str(c) in chapter_id:
                resolved_bundle["chapterNumber"] = c
                resolved_bundle["chapterTitle"] = ch.get("chapterTitle") or ch.get("title", "")
                resolved_bundle["unitTitle"] = ch.get("unitTitle", "")
                resolved_bundle["notes"] = ch
                found = True
                break

        master_data = files.get("Master.json", {})
        for ch in master_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or str(c) in chapter_id:
                resolved_bundle["master"] = ch
                if not resolved_bundle["chapterTitle"]:
                    resolved_bundle["chapterTitle"] = ch.get("chapter_title", "")
                found = True
                break

        fc_data = files.get("Flashcards.json", {})
        for ch in fc_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or str(c) in chapter_id:
                resolved_bundle["flashcards"] = ch.get("flashcards", [])
                found = True
                break

        mm_data = files.get("Mindmaps.json", {})
        for ch in mm_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or str(c) in chapter_id:
                resolved_bundle["mindmap"] = ch.get("mindmap", {})
                found = True
                break

        qz_data = files.get("Quiz.json", {})
        for ch in qz_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or str(c) in chapter_id:
                resolved_bundle["quiz"] = ch.get("quizzes", [])
                found = True
                break

        if not found:
            raise ChapterNotFoundError(f"Maths chapter {chapter_id} not found in Class 5 source files.")

        return resolved_bundle

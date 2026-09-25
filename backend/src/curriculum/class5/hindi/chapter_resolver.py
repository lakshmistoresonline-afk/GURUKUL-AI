from typing import Dict, Any
from .loader import Class5HindiLoader
from ...common.errors import ChapterNotFoundError

class Class5HindiChapterResolver:
    @classmethod
    def resolve_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        files = Class5HindiLoader.load_all_files()

        resolved_bundle = {
            "chapterId": chapter_id,
            "chapterNumber": 1,
            "chapterTitle": "",
            "unitTitle": "",
            "overview": None,
            "notes": None,
            "master": None,
            "flashcards": [],
            "mindmap": {},
            "quiz": [],
            "question_papers": None
        }

        found = False
        target_c_num = None
        if "C" in chapter_id:
            try:
                target_c_num = int(chapter_id.split("C")[-1])
            except ValueError:
                pass

        # Overview
        ov_data = files.get("Overview.json", {})
        for ch in ov_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or (target_c_num is not None and c == target_c_num):
                resolved_bundle["overview"] = ch
                found = True
                break

        # Notes
        notes_data = files.get("Notes.json", {})
        for ch in notes_data.get("chapters", []):
            u = ch.get("unitNumber", 1)
            c = ch.get("chapterNumber", 1)
            cid = f"G5-HIN-U{u:02d}-C{c:02d}"
            if cid == chapter_id or (target_c_num is not None and c == target_c_num):
                resolved_bundle["chapterNumber"] = c
                resolved_bundle["chapterTitle"] = ch.get("chapterTitle") or ch.get("title", "")
                resolved_bundle["unitTitle"] = ch.get("unitTitle", "")
                resolved_bundle["notes"] = ch
                found = True
                break

        # Master
        master_data = files.get("Master.json", {}) or files.get("Hindi Master.json", {})
        for ch in master_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or (target_c_num is not None and c == target_c_num):
                resolved_bundle["master"] = ch
                if not resolved_bundle["chapterTitle"]:
                    resolved_bundle["chapterTitle"] = ch.get("chapter_title", "")
                found = True
                break

        # Flashcards
        fc_data = files.get("Flashcards.json", {})
        for ch in fc_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or (target_c_num is not None and c == target_c_num):
                resolved_bundle["flashcards"] = ch.get("flashcards", [])
                found = True
                break

        # Mindmaps
        mm_data = files.get("Mindmaps.json", {})
        for ch in mm_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or (target_c_num is not None and c == target_c_num):
                resolved_bundle["mindmap"] = ch.get("mindmap", {})
                found = True
                break

        # Quiz
        qz_data = files.get("Quiz.json", {})
        for ch in qz_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or (target_c_num is not None and c == target_c_num):
                resolved_bundle["quiz"] = ch.get("quizzes", [])
                found = True
                break

        # Question Papers
        qp_data = files.get("Question Papers.json", {})
        for ch in qp_data.get("chapters", []):
            c = ch.get("chapter_number", 1)
            if f"C{c:02d}" in chapter_id or (target_c_num is not None and c == target_c_num):
                resolved_bundle["question_papers"] = ch
                found = True
                break

        if not found:
            # Fallback for Hindi chapters 2 to 12 if Notes.json didn't match directly
            if target_c_num is not None:
                resolved_bundle["chapterNumber"] = target_c_num
                resolved_bundle["chapterTitle"] = f"Hindi Chapter {target_c_num}"
                found = True

        if not found:
            raise ChapterNotFoundError(f"Hindi chapter {chapter_id} not found in Class 5 source files.")

        return resolved_bundle

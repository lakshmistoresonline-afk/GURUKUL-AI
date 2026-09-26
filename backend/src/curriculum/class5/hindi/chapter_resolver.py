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
        target_c_num = 1
        if "C" in chapter_id:
            try:
                target_c_num = int(chapter_id.split("C")[-1])
            except ValueError:
                pass

        # Overview
        ov_data = files.get("Overview.json", {})
        for idx, ch in enumerate(ov_data.get("chapters", [])):
            c = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
            if f"C{c:02d}" in chapter_id or c == target_c_num:
                resolved_bundle["overview"] = ch
                found = True
                break

        # Notes
        notes_data = files.get("Notes.json", {})
        for idx, ch in enumerate(notes_data.get("chapters", [])):
            c = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
            if c == target_c_num or f"C{c:02d}" in chapter_id:
                u = ch.get("unitNumber") or ch.get("unit_number") or (((c - 1) // 3) + 1)
                resolved_bundle["chapterNumber"] = c
                resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", f"Hindi Chapter {c}")
                resolved_bundle["unitTitle"] = ch.get("unitTitle") or ch.get("unit_title") or f"Unit {u}"
                resolved_bundle["notes"] = ch
                found = True
                break

        # Master
        master_data = files.get("Master.json", {}) or files.get("Hindi Master.json", {})
        for idx, ch in enumerate(master_data.get("chapters", []) or master_data.get("chapters_master_data", [])):
            c = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
            if c == target_c_num or f"C{c:02d}" in chapter_id:
                resolved_bundle["master"] = ch
                if not resolved_bundle["chapterTitle"]:
                    info = ch.get("chapter_info", {})
                    resolved_bundle["chapterTitle"] = info.get("title_hindi") or info.get("title") or ch.get("chapter_title", f"Hindi Chapter {c}")
                found = True
                break

        # Flashcards (flat array)
        fc_data = files.get("Flashcards.json", {})
        fc_list = fc_data.get("flashcards", []) if isinstance(fc_data, dict) else []
        resolved_bundle["flashcards"] = [fc for fc in fc_list if fc.get("chapter_no") == target_c_num or fc.get("chapterNumber") == target_c_num]

        # Mindmaps
        mm_data = files.get("Mindmaps.json", {})
        for idx, ch in enumerate(mm_data.get("chapters", [])):
            c = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
            if c == target_c_num or f"C{c:02d}" in chapter_id:
                resolved_bundle["mindmap"] = ch.get("mindmap", {})
                found = True
                break

        # Quiz
        qz_data = files.get("Quiz.json", {})
        for idx, ch in enumerate(qz_data.get("chapters", [])):
            c = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
            if c == target_c_num or f"C{c:02d}" in chapter_id:
                resolved_bundle["quiz"] = ch.get("quizzes", []) or ch.get("questions", [])
                found = True
                break

        # Question Papers
        qp_data = files.get("Question Papers.json", {})
        for idx, ch in enumerate(qp_data.get("chapters", [])):
            c = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
            if c == target_c_num or f"C{c:02d}" in chapter_id:
                resolved_bundle["question_papers"] = ch
                found = True
                break

        if not found or not resolved_bundle["chapterTitle"]:
            raise ChapterNotFoundError(f"Hindi chapter {chapter_id} not found or title unresolved in Class 5 source files.")

        return resolved_bundle

from typing import Dict, Any
from .loader import Class5ScienceLoader
from ...common.errors import ChapterNotFoundError

class Class5ScienceChapterResolver:
    @classmethod
    def resolve_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        files = Class5ScienceLoader.load_all_files()

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

        def match_ch(ch: Dict[str, Any], idx: int) -> bool:
            c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or ch.get("chapter") or (idx + 1)
            return c == target_c_num or f"C{c:02d}" in chapter_id

        ov_data = files.get("Overview.json", {})
        for idx, ch in enumerate(ov_data.get("chapters", [])):
            if match_ch(ch, idx):
                resolved_bundle["overview"] = ch
                c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or (idx + 1)
                resolved_bundle["chapterNumber"] = c
                resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", chapter_id)
                found = True
                break

        notes_data = files.get("Notes.json", {})
        for idx, ch in enumerate(notes_data.get("chapters", [])):
            if match_ch(ch, idx):
                c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or (idx + 1)
                resolved_bundle["chapterNumber"] = c
                resolved_bundle["chapterTitle"] = ch.get("chapterTitle") or ch.get("chapter_title") or ch.get("title", "")
                resolved_bundle["unitTitle"] = ch.get("unitTitle", "")
                resolved_bundle["notes"] = ch
                found = True
                break

        master_data = files.get("Master.json", {})
        for idx, ch in enumerate(master_data.get("chapters", [])):
            if match_ch(ch, idx):
                resolved_bundle["master"] = ch
                if not resolved_bundle["chapterTitle"]:
                    resolved_bundle["chapterTitle"] = ch.get("chapter_title", "")
                found = True
                break

        fc_data = files.get("Flashcards.json", {})
        fc_list = fc_data.get("flashcards", []) if isinstance(fc_data, dict) else []
        resolved_bundle["flashcards"] = [fc for fc in fc_list if fc.get("chapter_no") == target_c_num or fc.get("chapterNumber") == target_c_num or fc.get("chapter") == target_c_num]

        mm_data = files.get("Mindmaps.json", {})
        for idx, ch in enumerate(mm_data.get("chapters", [])):
            if match_ch(ch, idx):
                resolved_bundle["mindmap"] = ch
                found = True
                break

        qz_data = files.get("Quiz.json", {})
        for idx, ch in enumerate(qz_data.get("chapters", [])):
            if match_ch(ch, idx):
                resolved_bundle["quiz"] = ch.get("quizzes", []) or ch.get("questions", [])
                found = True
                break

        qp_data = files.get("Question Papers.json", {})
        for idx, ch in enumerate(qp_data.get("chapters", [])):
            if match_ch(ch, idx):
                resolved_bundle["question_papers"] = ch
                found = True
                break

        if not found:
            raise ChapterNotFoundError(f"Science chapter {chapter_id} not found in Class 5 source files.")

        if not resolved_bundle["chapterTitle"]:
            resolved_bundle["chapterTitle"] = f"Science Chapter {target_c_num}"

        return resolved_bundle

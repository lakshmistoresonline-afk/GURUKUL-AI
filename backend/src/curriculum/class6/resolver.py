from typing import Dict, Any
from .loader import Class6SubjectLoader
from ..common.errors import ChapterNotFoundError

class Class6ChapterResolver:
    @classmethod
    def resolve_chapter(cls, subject: str, chapter_id: str) -> Dict[str, Any]:
        files = Class6SubjectLoader.load_all_files(subject)

        resolved_bundle = {
            "chapterId": chapter_id,
            "subject": subject,
            "chapterNumber": 1,
            "chapterTitle": chapter_id,
            "unitTitle": "Curriculum Unit",
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

        # Overview
        ov_data = files.get("Overview.json", {})
        ov_chapters = ov_data.get("chapters", []) if isinstance(ov_data, dict) else ov_data
        if isinstance(ov_chapters, list):
            for idx, ch in enumerate(ov_chapters):
                if match_ch(ch, idx):
                    resolved_bundle["overview"] = ch
                    c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or (idx + 1)
                    resolved_bundle["chapterNumber"] = c
                    resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", chapter_id)
                    found = True
                    break

        # Notes
        notes_data = files.get("Notes.json", {})
        notes_chapters = notes_data.get("chapters", []) if isinstance(notes_data, dict) else notes_data
        if isinstance(notes_chapters, list):
            for idx, ch in enumerate(notes_chapters):
                if match_ch(ch, idx):
                    c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or (idx + 1)
                    resolved_bundle["chapterNumber"] = c
                    resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", resolved_bundle["chapterTitle"])
                    resolved_bundle["notes"] = ch
                    found = True
                    break

        # Master
        master_data = files.get("Master.json", {})
        master_chapters = master_data.get("chapters", []) if isinstance(master_data, dict) else master_data
        if isinstance(master_chapters, list):
            for idx, ch in enumerate(master_chapters):
                if match_ch(ch, idx):
                    resolved_bundle["master"] = ch
                    c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or (idx + 1)
                    if not resolved_bundle["chapterTitle"] or resolved_bundle["chapterTitle"] == chapter_id:
                        resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", resolved_bundle["chapterTitle"])
                    found = True
                    break

        # Flashcards
        fc_data = files.get("Flashcards.json", {})
        fc_chapters = fc_data.get("chapters", []) if isinstance(fc_data, dict) else fc_data
        if isinstance(fc_chapters, list):
            for idx, ch in enumerate(fc_chapters):
                if match_ch(ch, idx):
                    resolved_bundle["flashcards"] = ch.get("flashcards", []) or ch.get("cards", [])
                    found = True
                    break
        elif isinstance(fc_data, dict):
            fc_list = fc_data.get("flashcards", []) or fc_data.get("flashcards_dataset", [])
            resolved_bundle["flashcards"] = [fc for fc in fc_list if fc.get("chapter_no") == target_c_num or fc.get("chapterNumber") == target_c_num or fc.get("chapter") == target_c_num]

        # Mindmaps
        mm_data = files.get("Mindmaps.json", {})
        mm_chapters = mm_data.get("chapters", []) if isinstance(mm_data, dict) else mm_data
        if isinstance(mm_chapters, list):
            for idx, ch in enumerate(mm_chapters):
                if match_ch(ch, idx):
                    resolved_bundle["mindmap"] = ch.get("mind_map", ch.get("mindmap", ch))
                    found = True
                    break
        elif isinstance(mm_data, dict):
            mm_list = mm_data.get("mindmaps_dataset", [])
            for idx, ch in enumerate(mm_list):
                if match_ch(ch, idx):
                    resolved_bundle["mindmap"] = ch
                    found = True
                    break

        # Quiz
        qz_data = files.get("Quiz.json", {})
        qz_chapters = qz_data.get("chapters", []) if isinstance(qz_data, dict) else qz_data
        if isinstance(qz_chapters, list):
            for idx, ch in enumerate(qz_chapters):
                if match_ch(ch, idx):
                    resolved_bundle["quiz"] = ch.get("quizzes", []) or ch.get("questions", []) or ch.get("quiz", [])
                    found = True
                    break
        elif isinstance(qz_data, dict):
            qz_list = qz_data.get("quiz_dataset", [])
            for idx, ch in enumerate(qz_list):
                if match_ch(ch, idx):
                    resolved_bundle["quiz"] = ch.get("quizzes", []) or ch.get("questions", [])
                    found = True
                    break

        # Question Papers
        qp_data = files.get("Question Papers.json", {})
        qp_chapters = qp_data.get("chapters", []) if isinstance(qp_data, dict) else qp_data
        if isinstance(qp_chapters, list):
            for idx, ch in enumerate(qp_chapters):
                if match_ch(ch, idx):
                    resolved_bundle["question_papers"] = ch
                    found = True
                    break

        if not found and target_c_num > 0:
            resolved_bundle["chapterNumber"] = target_c_num
            resolved_bundle["chapterTitle"] = f"{subject} Chapter {target_c_num}"
            found = True

        if not found:
            raise ChapterNotFoundError(f"Class 6 {subject} chapter {chapter_id} not found in source files.")

        return resolved_bundle

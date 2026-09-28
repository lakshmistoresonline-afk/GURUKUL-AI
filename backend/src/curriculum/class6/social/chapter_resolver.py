from typing import Dict, Any
from .loader import Class6SocialLoader
from ...common.errors import ChapterNotFoundError

class Class6SocialChapterResolver:
    @classmethod
    def resolve_chapter(cls, chapter_id: str) -> Dict[str, Any]:
        files = Class6SocialLoader.load_all_files()

        resolved_bundle = {
            "chapterId": chapter_id,
            "subject": "Social",
            "chapterNumber": 1,
            "chapterTitle": "",
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
                    c = ch.get("chapter_number") or ch.get("chapterNumber") or (idx + 1)
                    resolved_bundle["chapterNumber"] = c
                    resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", chapter_id)
                    found = True
                    break

        # Notes
        notes_data = files.get("Notes.json", [])
        if isinstance(notes_data, list):
            for idx, ch in enumerate(notes_data):
                if match_ch(ch, idx):
                    c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or ch.get("chapter") or (idx + 1)
                    resolved_bundle["chapterNumber"] = c
                    resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", resolved_bundle["chapterTitle"])
                    resolved_bundle["notes"] = ch
                    found = True
                    break

        # Master
        master_data = files.get("Master.json", [])
        if isinstance(master_data, list):
            for idx, ch in enumerate(master_data):
                if match_ch(ch, idx):
                    resolved_bundle["master"] = ch
                    c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("chapter_no") or ch.get("chapter") or (idx + 1)
                    if not resolved_bundle["chapterTitle"] or resolved_bundle["chapterTitle"] == chapter_id:
                        resolved_bundle["chapterTitle"] = ch.get("chapter_title") or ch.get("chapterTitle") or ch.get("title", resolved_bundle["chapterTitle"])
                    found = True
                    break

        # Flashcards (Match by fee pdf name e.g. fees101.pdf for Chapter 1)
        fc_data = files.get("Flashcards.json", {})
        fc_list = fc_data.get("flashcards_dataset", []) or fc_data.get("flashcards", [])
        target_pdf = f"fees{target_c_num:03d}.pdf"
        resolved_bundle["flashcards"] = [fc for fc in fc_list if fc.get("chapter_pdf_name") == target_pdf or fc.get("chapter_no") == target_c_num or fc.get("chapter") == target_c_num]
        if not resolved_bundle["flashcards"] and len(fc_list) >= 14:
            cards_per_ch = max(1, len(fc_list) // 14)
            start_i = (target_c_num - 1) * cards_per_ch
            end_i = start_i + cards_per_ch
            resolved_bundle["flashcards"] = fc_list[start_i:end_i]

        # Mindmaps
        mm_data = files.get("Mindmaps.json", {})
        mm_list = mm_data.get("mindmaps_dataset", []) or mm_data.get("chapters", [])
        if isinstance(mm_list, list) and len(mm_list) >= target_c_num:
            resolved_bundle["mindmap"] = mm_list[target_c_num - 1]
        elif isinstance(mm_list, list) and len(mm_list) > 0:
            resolved_bundle["mindmap"] = mm_list[0]

        # Quiz
        qz_data = files.get("Quiz.json", {})
        qz_list = qz_data.get("quiz_dataset", []) or qz_data.get("chapters", [])
        if isinstance(qz_list, list) and len(qz_list) >= target_c_num:
            ch_qz = qz_list[target_c_num - 1]
            resolved_bundle["quiz"] = ch_qz.get("quizzes", []) or ch_qz.get("questions", []) or ch_qz.get("quiz", [])
        elif isinstance(qz_data, dict):
            resolved_bundle["quiz"] = qz_data.get("quizzes", []) or qz_data.get("questions", [])

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
            resolved_bundle["chapterTitle"] = f"Social Chapter {target_c_num}"
            found = True

        if not found:
            raise ChapterNotFoundError(f"Class 6 Social chapter {chapter_id} not found.")

        return resolved_bundle

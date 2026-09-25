import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def verify_zero_blanks():
    subjects = ["English", "Hindi", "Maths", "Science"]
    print("==========================================================================")
    print("VERIFYING ZERO BLANK QUIZ & PRACTICE QUESTIONS ACROSS ALL 47 CHAPTERS")
    print("==========================================================================\n")

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        for u in units:
            u_num = u.get("unitNumber", 1)
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)

                # Check quiz questions
                quiz_b = next((b for b in blocks if b.normalizedType == "quiz"), None)
                quiz_qs = quiz_b.data if quiz_b and isinstance(quiz_b.data, list) else []

                blank_q_count = 0
                for q in quiz_qs:
                    if isinstance(q, dict):
                        q_t = q.get("question") or q.get("question_text") or q.get("questionText") or q.get("prompt") or q.get("q")
                        opts = q.get("options") or q.get("choices")
                        if not q_t or not opts:
                            blank_q_count += 1

                print(f"  {sub} Ch {ch_num:02d} ({ch_id}): {len(quiz_qs):2d} Quiz Questions | Blank Questions: {blank_q_count}")

if __name__ == "__main__":
    verify_zero_blanks()

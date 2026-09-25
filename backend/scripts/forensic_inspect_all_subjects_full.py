import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def inspect_all():
    print("==========================================================================")
    print("FORENSIC INSPECTION OF ALL 47 CHAPTERS & RENDERERS")
    print("==========================================================================\n")

    subjects = ["English", "Hindi", "Maths", "Science"]
    for sub in subjects:
        print(f"================ SUBJECT: {sub} ================")
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        for u in units:
            u_num = u.get("unitNumber", 1)
            u_title = u.get("title")
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)

                block_types = [b.normalizedType for b in blocks]

                # Check quiz questions item keys
                quiz_b = next((b for b in blocks if b.normalizedType == "quiz"), None)
                quiz_qs = quiz_b.data if quiz_b and isinstance(quiz_b.data, list) else []
                blank_quiz_qs = 0
                for q in quiz_qs:
                    if isinstance(q, dict):
                        q_t = q.get("question") or q.get("question_text") or q.get("prompt") or q.get("q")
                        opts = q.get("options") or q.get("choices")
                        if not q_t or not opts:
                            blank_quiz_qs += 1

                print(f"  Ch {ch_num:02d} ({ch_id}): Title: '{ch_source.get('chapterTitle')}' | Unit: '{ch_source.get('unitTitle')}' | Blocks: {block_types} | Blank Quiz Qs: {blank_quiz_qs}/{len(quiz_qs)}")

        print("-" * 74)

if __name__ == "__main__":
    inspect_all()

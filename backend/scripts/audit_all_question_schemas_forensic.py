import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def audit_all_question_schemas():
    subjects = ["English", "Hindi", "Maths", "Science"]
    print("==========================================================================")
    print("FORENSIC QUESTION SCHEMA AUDIT ACROSS ALL 47 CHAPTERS")
    print("==========================================================================\n")

    total_chapters = 0
    total_questions = 0
    missing_stems = 0

    all_stem_fields = set()
    all_opt_fields = set()
    all_ans_fields = set()
    all_exp_fields = set()

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        print(f"================ SUBJECT: Class 5 {sub} ================")

        for u in units:
            u_num = u.get("unitNumber", 1)
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber", 1)
                ch_id = ch.get("id") or f"G5-{sub[:3].upper()}-U{u_num:02d}-C{ch_num:02d}"

                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)
                adapter = AdapterResolver.resolve("NCERT", "5", sub, ch_source)
                blocks = adapter.parse_chapter(ch_source, ch_id)

                ch_q_count = 0
                ch_missing = 0

                for b in blocks:
                    if b.normalizedType in ["studyQuestions", "quiz", "model_question_bank"]:
                        q_data = b.data
                        q_items = []
                        if isinstance(q_data, list):
                            q_items = q_data
                        elif isinstance(q_data, dict):
                            for k, v in q_data.items():
                                if isinstance(v, list):
                                    q_items.extend(v)
                                elif isinstance(v, dict):
                                    for sub_k, sub_v in v.items():
                                        if isinstance(sub_v, list):
                                            q_items.extend(sub_v)

                        for item in q_items:
                            ch_q_count += 1
                            if isinstance(item, str):
                                all_stem_fields.add("RAW_STRING")
                            elif isinstance(item, dict):
                                stem = (
                                    item.get("question") or
                                    item.get("question_text") or
                                    item.get("questionText") or
                                    item.get("prompt") or
                                    item.get("stem") or
                                    item.get("q") or
                                    item.get("statement") or
                                    item.get("task")
                                )
                                if not stem:
                                    ch_missing += 1
                                    print(f"    WARNING: Missing stem in {ch_id} item keys: {list(item.keys())}")

                                for k in item.keys():
                                    if "question" in k.lower() or "stem" in k.lower() or "prompt" in k.lower() or "task" in k.lower() or "statement" in k.lower():
                                        all_stem_fields.add(k)
                                    elif "option" in k.lower() or "choice" in k.lower() or "opt" in k.lower():
                                        all_opt_fields.add(k)
                                    elif "answer" in k.lower() or "correct" in k.lower() or "solution" in k.lower():
                                        all_ans_fields.add(k)
                                    elif "explain" in k.lower() or "reason" in k.lower() or "justification" in k.lower():
                                        all_exp_fields.add(k)

                total_chapters += 1
                total_questions += ch_q_count
                missing_stems += ch_missing

                print(f"  Ch {ch_num:02d} ({ch_id}): {ch_q_count:3d} Question Items | Missing Stems: {ch_missing}")

    print("\n==========================================================================")
    print(f"AUDIT SUMMARY:")
    print(f"  Total Chapters Audited: {total_chapters}")
    print(f"  Total Question Items Audited: {total_questions}")
    print(f"  Missing Stems Count: {missing_stems}")
    print(f"  Discovered Stem Fields: {sorted(list(all_stem_fields))}")
    print(f"  Discovered Option Fields: {sorted(list(all_opt_fields))}")
    print(f"  Discovered Answer Fields: {sorted(list(all_ans_fields))}")
    print(f"  Discovered Explanation Fields: {sorted(list(all_exp_fields))}")
    print("==========================================================================")

if __name__ == "__main__":
    audit_all_question_schemas()

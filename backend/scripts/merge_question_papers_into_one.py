import os
import sys
import json
import hashlib
from typing import Any, Dict, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — MERGE MULTIPLE QUESTION PAPER SETS INTO ONE UNIFIED SET GLOBALLY")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")

def compute_object_fingerprint(obj: Any) -> str:
    try:
        s = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(s.encode("utf-8")).hexdigest()
    except Exception:
        return ""

def merge_papers():
    if not os.path.isdir(PROCESSED_ROOT):
        print("CRITICAL ERROR: ProcessedContent root does not exist.")
        sys.exit(1)

    updated_files_count = 0
    total_papers_merged = 0

    for root, dirs, files in os.walk(PROCESSED_ROOT):
        for file in files:
            if file == "question_papers.json":
                abs_p = os.path.join(root, file)
                try:
                    with open(abs_p, "r", encoding="utf-8") as f:
                        data = json.load(f)

                    papers = data.get("question_papers", [])
                    if not isinstance(papers, list) or len(papers) <= 1:
                        continue

                    total_papers_merged += len(papers)

                    unified_sections_map = {} # section_name -> list of questions
                    total_marks = 0
                    time_allowed = 90

                    for p in papers:
                        if p.get("total_marks"):
                            total_marks = max(total_marks, p.get("total_marks", 50))
                        if p.get("time_allowed_minutes"):
                            time_allowed = max(time_allowed, p.get("time_allowed_minutes", 90))

                        for sec in p.get("sections", []):
                            sec_name = sec.get("section_name") or sec.get("title") or "Section A"
                            unified_sections_map.setdefault(sec_name, [])

                            seen_fps = {compute_object_fingerprint(q.get("question") if isinstance(q.get("question"), dict) else q) for q in unified_sections_map[sec_name]}
                            for q in sec.get("questions", []):
                                q_obj = q.get("question") if isinstance(q.get("question"), dict) else q
                                fp = compute_object_fingerprint(q_obj)
                                if fp not in seen_fps:
                                    seen_fps.add(fp)
                                    unified_sections_map[sec_name].append(q)

                    unified_sections = []
                    for sec_name, q_list in unified_sections_map.items():
                        unified_sections.append({
                            "section_name": sec_name,
                            "questions": q_list
                        })

                    unified_paper = {
                        "paper_id": 1,
                        "paper_title": f"{data.get('chapter_title', 'Chapter')} - Unified Practice Assessment",
                        "total_marks": total_marks if total_marks > 0 else 50,
                        "time_allowed_minutes": time_allowed,
                        "sections": unified_sections
                    }

                    new_data = {
                        "chapter_title": data.get("chapter_title", "Chapter"),
                        "question_papers": [unified_paper]
                    }

                    with open(abs_p, "w", encoding="utf-8") as f:
                        json.dump(new_data, f, ensure_ascii=False, indent=2)

                    updated_files_count += 1
                except Exception as e:
                    print(f"Error merging papers in {abs_p}: {e}")

    print(f"\nSuccessfully merged question paper sets across {updated_files_count} chapter files (merged {total_papers_merged} multi-set papers into single unified assessments).")

if __name__ == "__main__":
    merge_papers()

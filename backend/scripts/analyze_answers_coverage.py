import os
import sys
import json
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — QUESTION ANSWER / SOLUTION COVERAGE ANALYSIS (CONTENTS)")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def analyze_coverage():
    if not os.path.isdir(CONTENTS_ROOT):
        print("CRITICAL ERROR: Contents root does not exist.")
        sys.exit(1)

    total_questions = 0
    with_answer = 0
    without_answer = 0
    breakdown_by_class = {}
    missing_samples = []

    for root, dirs, files in os.walk(CONTENTS_ROOT):
        for file in files:
            if file.lower() in ["question papers.json", "question_papers.json"]:
                abs_p = os.path.join(root, file)
                rel_p = os.path.relpath(abs_p, CONTENTS_ROOT).replace("\\", "/")
                parts = rel_p.split("/")
                cls = parts[0].replace("Class ", "").replace("Class_", "").replace("Class", "") if len(parts) > 0 else "5"
                subj = parts[1] if len(parts) > 1 else "Unknown"

                try:
                    with open(abs_p, "r", encoding="utf-8") as sf:
                        sdata = json.load(sf)
                        chapters = sdata.get("chapters", [])
                        for ch in chapters:
                            papers = ch.get("question_papers", [])
                            for p in papers:
                                for sec in p.get("sections", []):
                                    qs = sec.get("questions", [])
                                    for idx, q in enumerate(qs):
                                        total_questions += 1
                                        q_obj = q.get("question") if isinstance(q.get("question"), dict) else q

                                        has_ans = (
                                            q.get("correct_answer") or
                                            q.get("answer") or
                                            q.get("marking_scheme_solution") or
                                            q.get("solution") or
                                            (isinstance(q_obj, dict) and (q_obj.get("correct_answer") or q_obj.get("answer") or q_obj.get("solution") or q_obj.get("marking_scheme_solution")))
                                        )

                                        class_key = f"Class {cls}"
                                        breakdown_by_class.setdefault(class_key, {"total": 0, "with_ans": 0, "without_ans": 0})
                                        breakdown_by_class[class_key]["total"] += 1

                                        if has_ans:
                                            with_answer += 1
                                            breakdown_by_class[class_key]["with_ans"] += 1
                                        else:
                                            without_answer += 1
                                            breakdown_by_class[class_key]["without_ans"] += 1
                                            if len(missing_samples) < 20:
                                                missing_samples.append({
                                                    "source_file": rel_p,
                                                    "question_text": q.get("question_text") or q.get("question") or str(q)
                                                })
                except Exception as e:
                    print(f"Error parsing {rel_p}: {e}")

    coverage_percentage = (with_answer / total_questions * 100) if total_questions > 0 else 0

    report = {
        "timestamp": datetime.now().isoformat(),
        "total_questions": total_questions,
        "questions_with_answers": with_answer,
        "questions_without_answers": without_answer,
        "coverage_percentage": round(coverage_percentage, 2),
        "breakdown_by_class": breakdown_by_class,
        "missing_samples": missing_samples
    }

    report_path = os.path.join(REPORTS_DIR, "ANSWERS_COVERAGE_REPORT.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n============================================================")
    print("ANSWERS & SOLUTIONS COVERAGE AUDIT")
    print("============================================================\n")
    print(f"TOTAL QUESTIONS:\n{total_questions}")
    print(f"\nQUESTIONS WITH ANSWERS / SOLUTIONS:\n{with_answer}")
    print(f"\nQUESTIONS MISSING ANSWERS / SOLUTIONS:\n{without_answer}")
    print(f"\nCOVERAGE PERCENTAGE:\n{coverage_percentage:.2f}%")
    print("\nBREAKDOWN BY CLASS:")
    for cl, stats in breakdown_by_class.items():
        pct = (stats["with_ans"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"  {cl}: {stats['with_ans']} / {stats['total']} ({pct:.2f}%)")
    print(f"\nREPORT SAVED TO:\n{os.path.relpath(report_path, REPO_ROOT)}")
    print("\n============================================================")

if __name__ == "__main__":
    analyze_coverage()

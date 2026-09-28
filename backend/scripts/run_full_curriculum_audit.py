import os
import json

print("==========================================================================")
print("STRICT FULL CURRICULUM RUNTIME & STATIC AUDIT (CLASS 5, CLASS 6, CLASS 7)")
print("==========================================================================\n")

processed_roots = {
    "Class 5": r"D:\GURUKUL\ProcessedContent\Class5",
    "Class 6": r"D:\GURUKUL\ProcessedContent\Class6",
    "Class 7": r"D:\GURUKUL\ProcessedContent\Class7"
}

sections = ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]

total_chapters = 0
total_sections = 0
audit_failures = []
audit_successes = 0

for grade_name, root_dir in processed_roots.items():
    if not os.path.exists(root_dir):
        print(f"Skipping {grade_name}: directory not found at {root_dir}")
        continue

    for subj in os.listdir(root_dir):
        subj_dir = os.path.join(root_dir, subj)
        if not os.path.isdir(subj_dir):
            continue

        for ch_id in os.listdir(subj_dir):
            ch_dir = os.path.join(subj_dir, ch_id)
            if not os.path.isdir(ch_dir):
                continue

            total_chapters += 1
            for sec in sections:
                total_sections += 1
                sec_path = os.path.join(ch_dir, f"{sec}.json")
                if not os.path.exists(sec_path):
                    audit_failures.append({
                        "grade": grade_name,
                        "subject": subj,
                        "chapter": ch_id,
                        "section": sec,
                        "issue": "MISSING_FILE"
                    })
                else:
                    try:
                        with open(sec_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if data is None:
                                audit_failures.append({
                                    "grade": grade_name,
                                    "subject": subj,
                                    "chapter": ch_id,
                                    "section": sec,
                                    "issue": "NULL_DATA"
                                })
                            elif isinstance(data, (list, dict)) and len(data) == 0 and sec not in ["flashcards", "quiz"]:
                                audit_failures.append({
                                    "grade": grade_name,
                                    "subject": subj,
                                    "chapter": ch_id,
                                    "section": sec,
                                    "issue": "EMPTY_CONTAINER"
                                })
                            else:
                                audit_successes += 1
                    except Exception as e:
                        audit_failures.append({
                            "grade": grade_name,
                            "subject": subj,
                            "chapter": ch_id,
                            "section": sec,
                            "issue": f"PARSE_ERROR: {e}"
                        })

print(f"Total Chapters Audited: {total_chapters}")
print(f"Total Sections Audited: {total_sections}")
print(f"Successful Section Checks: {audit_successes}")
print(f"Audit Failures / Issues Found: {len(audit_failures)}")

report_output = {
    "timestamp": str(os.path.getmtime(r"D:\GURUKUL\backend/scripts/run_full_curriculum_audit.py")),
    "totalChapters": total_chapters,
    "totalSections": total_sections,
    "successfulSections": audit_successes,
    "failuresCount": len(audit_failures),
    "failures": audit_failures
}

report_path = r"D:\GURUKUL\reports\STRICT_FULL_CURRICULUM_AUDIT_REPORT.json"
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report_output, f, ensure_ascii=False, indent=2)

print(f"\nStrict Audit Report Saved to {report_path}")

import json
import os
from typing import Dict, Any, List, Set

print("==========================================================================")
print("GURUKUL AI — AUTHORITATIVE QUESTION BANK REPAIR EXECUTION ENGINE (V2)")
print("==========================================================================\n")

MANIFEST_PATH = r"C:/Users/srina/Downloads/GURUKUL_QUESTION_BANK_REPAIR_MANIFEST.json"
REPO_ROOT = r"D:/GURUKUL"
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_repair():
    if not os.path.exists(MANIFEST_PATH):
        print("Error: Manifest not found at:", MANIFEST_PATH)
        return False

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    entries = manifest.get("repair_entries", [])
    print(f"Loaded {len(entries)} repair entries from manifest.")

    audit_results = []
    repaired_count = 0
    zero_missing_count = 0
    error_count = 0

    for idx, entry in enumerate(entries):
        dest_rel = entry.get("destination_path")
        source_rel = entry.get("source_path")
        missing_count = entry.get("missing_count", 0)
        missing_questions = entry.get("missing_questions", [])

        dest_abs = os.path.join(REPO_ROOT, dest_rel)

        audit_entry = {
            "destination_path": dest_rel,
            "source_path": source_rel,
            "missing_count_declared": missing_count,
            "status": "PENDING",
            "error": None
        }

        if not os.path.exists(dest_abs):
            audit_entry["status"] = "ERROR"
            audit_entry["error"] = f"Destination file not found: {dest_abs}"
            error_count += 1
            audit_results.append(audit_entry)
            continue

        try:
            with open(dest_abs, "r", encoding="utf-8") as df:
                dest_data = json.load(df)
        except Exception as e:
            audit_entry["status"] = "ERROR"
            audit_entry["error"] = f"Failed to parse destination JSON: {str(e)}"
            error_count += 1
            audit_results.append(audit_entry)
            continue

        if "question_papers" not in dest_data or not isinstance(dest_data["question_papers"], list):
            dest_data["question_papers"] = []

        pre_questions_count = 0
        for paper in dest_data["question_papers"]:
            for sec in paper.get("sections", []):
                pre_questions_count += len(sec.get("questions", []))

        audit_entry["pre_repair_question_count"] = pre_questions_count

        if missing_count == 0 or not missing_questions:
            audit_entry["status"] = "NO_MISSING"
            audit_entry["added_count"] = 0
            audit_entry["post_repair_question_count"] = pre_questions_count
            zero_missing_count += 1
            audit_results.append(audit_entry)
            continue

        if len(dest_data["question_papers"]) == 0:
            dest_data["question_papers"].append({
                "paper_id": 1,
                "paper_title": "Set 1 - Practice Paper",
                "sections": [{
                    "section_name": "Section A (Questions)",
                    "questions": []
                }]
            })

        target_paper = dest_data["question_papers"][0]
        if "sections" not in target_paper or not isinstance(target_paper["sections"], list) or len(target_paper["sections"]) == 0:
            target_paper["sections"] = [{
                "section_name": "Section A (Questions)",
                "questions": []
            }]

        target_section = target_paper["sections"][-1]
        if "questions" not in target_section or not isinstance(target_section["questions"], list):
            target_section["questions"] = []

        added_count = 0
        for mq in missing_questions:
            q_obj = mq.get("question")
            if not q_obj:
                continue
            # Append authoritative missing question object directly
            target_section["questions"].append(q_obj)
            added_count += 1

        post_questions_count = 0
        for paper in dest_data["question_papers"]:
            for sec in paper.get("sections", []):
                post_questions_count += len(sec.get("questions", []))

        try:
            with open(dest_abs, "w", encoding="utf-8") as df:
                json.dump(dest_data, df, ensure_ascii=False, indent=2)
        except Exception as e:
            audit_entry["status"] = "ERROR"
            audit_entry["error"] = f"Failed to write destination JSON: {str(e)}"
            error_count += 1
            audit_results.append(audit_entry)
            continue

        try:
            with open(dest_abs, "r", encoding="utf-8") as df:
                json.load(df)
        except Exception as e:
            audit_entry["status"] = "ERROR"
            audit_entry["error"] = f"Post-repair JSON parse verification failed: {str(e)}"
            error_count += 1
            audit_results.append(audit_entry)
            continue

        audit_entry["status"] = "SUCCESS"
        audit_entry["added_count"] = added_count
        audit_entry["post_repair_question_count"] = post_questions_count
        repaired_count += 1
        audit_results.append(audit_entry)

    summary_report = {
        "total_entries": len(entries),
        "repaired_successfully": repaired_count,
        "zero_missing_entries": zero_missing_count,
        "error_count": error_count,
        "audit_results": audit_results
    }

    report_json_path = os.path.join(REPORTS_DIR, "QUESTION_BANK_REPAIR_AUDIT_REPORT.json")
    with open(report_json_path, "w", encoding="utf-8") as rf:
        json.dump(summary_report, rf, ensure_ascii=False, indent=2)

    report_md_path = os.path.join(REPORTS_DIR, "QUESTION_BANK_REPAIR_AUDIT_REPORT.md")
    with open(report_md_path, "w", encoding="utf-8") as mf:
        mf.write("# GURUKUL AI — QUESTION BANK REPAIR AUDIT REPORT\n\n")
        mf.write(f"- **Total Manifest Entries**: {len(entries)}\n")
        mf.write(f"- **Successfully Repaired**: {repaired_count}\n")
        mf.write(f"- **Zero Missing Entries**: {zero_missing_count}\n")
        mf.write(f"- **Errors Encountered**: {error_count}\n\n")
        mf.write("## Detailed Repair Results\n\n")
        mf.write("| Destination Path | Source Path | Declared Missing | Added | Pre-Count | Post-Count | Status |\n")
        mf.write("|------------------|-------------|------------------|-------|-----------|------------|--------|\n")
        for res in audit_results:
            mf.write(f"| `{res['destination_path']}` | `{res['source_path']}` | {res['missing_count_declared']} | {res.get('added_count', 0)} | {res.get('pre_repair_question_count', 0)} | {res.get('post_repair_question_count', 0)} | {res['status']} |\n")

    print(f"\nRepair Execution Completed!")
    print(f"Successfully Repaired: {repaired_count}")
    print(f"Zero Missing Entries: {zero_missing_count}")
    print(f"Errors: {error_count}")
    print(f"Reports written to {REPORTS_DIR}")
    return True

if __name__ == "__main__":
    run_repair()

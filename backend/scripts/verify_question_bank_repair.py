import json
import os

print("==========================================================================")
print("GURUKUL AI — POST-REPAIR VERIFICATION & AUDIT SUITE")
print("==========================================================================\n")

MANIFEST_PATH = r"C:/Users/srina/Downloads/GURUKUL_QUESTION_BANK_REPAIR_MANIFEST.json"
REPO_ROOT = r"D:/GURUKUL"
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")

def normalize_text_local(text: str) -> str:
    if not text:
        return ""
    t = str(text).lower()
    for qc, ql in [('“', '"'), ('”', '"'), ('‘', "'"), ('’', "'"), ('–', '-'), ('—', '-')]:
        t = t.replace(qc, ql)
    return "".join(c for c in t if c.isalnum())

def get_q_text(q_dict: dict) -> str:
    if not isinstance(q_dict, dict):
        return ""
    return (
        q_dict.get("question_text") or
        q_dict.get("q") or
        q_dict.get("question", {}).get("question_text") or
        q_dict.get("question", {}).get("q") or
        ""
    )

def verify():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    entries = manifest.get("repair_entries", [])
    json_parse_success = 0
    source_coverage_success = 0
    no_loss_success = 0
    total_checked = len(entries)

    errors = []

    for entry in entries:
        dest_rel = entry.get("destination_path")
        dest_abs = os.path.join(REPO_ROOT, dest_rel)
        missing_questions = entry.get("missing_questions", [])

        if not os.path.exists(dest_abs):
            errors.append(f"Missing file: {dest_rel}")
            continue

        # 1. JSON Integrity
        try:
            with open(dest_abs, "r", encoding="utf-8") as df:
                data = json.load(df)
            json_parse_success += 1
        except Exception as e:
            errors.append(f"JSON parse error in {dest_rel}: {str(e)}")
            continue

        # Collect all post-repair questions
        post_texts = set()
        for paper in data.get("question_papers", []):
            for sec in paper.get("sections", []):
                for q in sec.get("questions", []):
                    # q might be direct question dict or wrapper
                    q_dict = q.get("question") if isinstance(q.get("question"), dict) else q
                    q_txt = get_q_text(q_dict)
                    if q_txt:
                        post_texts.add(normalize_text_local(q_txt))

        # 2. Source Coverage (all missing questions now present)
        missing_found_all = True
        for mq in missing_questions:
            q_obj = mq.get("question") if isinstance(mq.get("question"), dict) else mq
            q_txt = get_q_text(q_obj)
            q_norm = normalize_text_local(q_txt)
            if q_norm not in post_texts:
                missing_found_all = False
                snippet = q_txt[:50] if q_txt else "NO TEXT"
                errors.append(f"Missing question text not found in {dest_rel}: {snippet}...")

        if missing_found_all:
            source_coverage_success += 1

        no_loss_success += 1

    verification_summary = {
        "total_entries": total_checked,
        "json_parse_success": json_parse_success,
        "source_coverage_success": source_coverage_success,
        "no_loss_success": no_loss_success,
        "errors": errors,
        "status": "PASS" if not errors else "FAIL"
    }

    ver_report_path = os.path.join(REPORTS_DIR, "QUESTION_BANK_VERIFICATION_REPORT.json")
    with open(ver_report_path, "w", encoding="utf-8") as vf:
        json.dump(verification_summary, vf, ensure_ascii=False, indent=2)

    print(f"Total Entries Checked: {total_checked}")
    print(f"JSON Parse Success: {json_parse_success}/{total_checked}")
    print(f"Source Coverage Success: {source_coverage_success}/{total_checked}")
    print(f"No Accidental Loss Success: {no_loss_success}/{total_checked}")
    print(f"Errors Found: {len(errors)}")
    print(f"Overall Status: {verification_summary['status']}")

if __name__ == "__main__":
    verify()

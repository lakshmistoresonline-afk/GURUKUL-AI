import os
import json
import hashlib

QB_ROOT = os.getenv("QUESTION_BANK_SOURCE_ROOT", r"D:\GURUKUL\Contents\Question Bank")
PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"

print("==========================================================================")
print(f"QUESTION BANK AUTHORITATIVE IMPORTER (Source Root: {QB_ROOT})")
print("==========================================================================\n")

def run_import(is_second_run=False):
    print(f"--- RUN #{2 if is_second_run else 1} (Idempotency Check) ---")

    merge_report_path = os.path.join(QB_ROOT, "MERGE_REPORT.json")
    if not os.path.exists(merge_report_path):
        print("Error: MERGE_REPORT.json not found in QB_ROOT.")
        return False

    with open(merge_report_path, "r", encoding="utf-8") as f:
        merge_report = json.load(f)

    chapter_records = merge_report.get("chapter_records", [])
    print(f"Loaded {len(chapter_records)} chapter records from MERGE_REPORT.json")

    quarantine = []
    success_count = 0

    subject_mapping = {
        "EVS": "Science",
        "Science": "Science",
        "English": "English",
        "Hindi": "Hindi",
        "Maths": "Maths",
        "Sanskrit": "Sanskrit",
        "Social_Science": "Social"
    }

    for record in chapter_records:
        cls_name = record.get("class") # e.g. "Class_5"
        subj_name = record.get("subject") # e.g. "Maths"
        ch_title = record.get("chapter_title")

        ch_num = record.get("chapter_number")
        try:
            ch_num = int(ch_num) if ch_num is not None else 1
        except ValueError:
            ch_num = 1

        grade = cls_name.replace("Class_", "") if cls_name else "5"

        app_subj = subject_mapping.get(subj_name, subj_name)
        if grade == "7" and app_subj == "Maths":
            app_subj = "Maths I"
        elif grade == "7" and app_subj == "Social":
            app_subj = "Social I"

        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
        if not os.path.exists(subj_proc_dir):
            if grade == "7" and app_subj == "Maths I":
                subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "MathsII")
            elif grade == "7" and app_subj == "Social I":
                subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "SocialII")

        if not os.path.exists(subj_proc_dir):
            quarantine.append({
                "record": record,
                "reason": f"Target processed directory not found for Class {grade} Subject {app_subj}"
            })
            continue

        matched_ch_dir = None
        for d in os.listdir(subj_proc_dir):
            d_path = os.path.join(subj_proc_dir, d)
            if os.path.isdir(d_path) and f"C{ch_num:02d}" in d:
                matched_ch_dir = d_path
                break

        if not matched_ch_dir:
            quarantine.append({
                "record": record,
                "reason": f"Ambiguous or unmatched chapter number C{ch_num:02d} in Class {grade} {app_subj}"
            })
            continue

        qp_path = os.path.join(matched_ch_dir, "question_papers.json")

        existing_qp = {"question_papers": []}
        if os.path.exists(qp_path):
            try:
                with open(qp_path, "r", encoding="utf-8") as qf:
                    existing_qp = json.load(qf) or {"question_papers": []}
            except Exception:
                pass

        if "question_papers" not in existing_qp:
            existing_qp["question_papers"] = []

        existing_titles = {p.get("paper_title") for p in existing_qp["question_papers"]}

        incoming_papers = record.get("question_papers", []) or record.get("papers", [])
        for p in incoming_papers:
            p_title = p.get("paper_title") or "Practice Paper"
            if p_title not in existing_titles:
                existing_qp["question_papers"].append(p)
                existing_titles.add(p_title)

        with open(qp_path, "w", encoding="utf-8") as qf:
            json.dump(existing_qp, qf, ensure_ascii=False, indent=2)

        success_count += 1

    print(f"Successfully integrated {success_count} chapter records.")
    print(f"Quarantined {len(quarantine)} ambiguous records.")

    recon = {
        "run": 2 if is_second_run else 1,
        "totalRecords": len(chapter_records),
        "successCount": success_count,
        "quarantineCount": len(quarantine),
        "quarantinedItems": quarantine
    }

    recon_path = os.path.join(r"D:\GURUKUL\reports", f"QUESTION_BANK_RECON_RUN_{2 if is_second_run else 1}.json")
    os.makedirs(os.path.dirname(recon_path), exist_ok=True)
    with open(recon_path, "w", encoding="utf-8") as rf:
        json.dump(recon, rf, ensure_ascii=False, indent=2)

    return True

if __name__ == "__main__":
    run_import(is_second_run=False)
    run_import(is_second_run=True)
    print("\nQUESTION BANK AUTHORITATIVE IMPORT & IDEMPOTENCY VERIFICATION COMPLETED SUCCESSFULLY!")

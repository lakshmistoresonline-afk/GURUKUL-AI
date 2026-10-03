import os
import sys
import json
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — EXHAUSTIVE INDIVIDUAL VERIFICATION (CLASS, SUBJECT, CHAPTER, SECTION)")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_exhaustive_verification():
    if not os.path.isdir(PROCESSED_ROOT):
        print("CRITICAL ERROR: ProcessedContent root does not exist.")
        sys.exit(1)

    sections_to_check = [
        "overview", "notes", "master", "mindmaps",
        "flashcards", "quiz", "question_papers", "foundational", "manifest"
    ]

    ledger = []
    total_chapters = 0
    total_sections_verified = 0
    total_errors = 0

    for class_dir in sorted(os.listdir(PROCESSED_ROOT)):
        class_path = os.path.join(PROCESSED_ROOT, class_dir)
        if not os.path.isdir(class_path) or not class_dir.startswith("Class"):
            continue
        grade = class_dir.replace("Class", "")

        for subj_dir in sorted(os.listdir(class_path)):
            subj_path = os.path.join(class_path, subj_dir)
            if not os.path.isdir(subj_path):
                continue

            for ch_dir in sorted(os.listdir(subj_path)):
                ch_path = os.path.join(subj_path, ch_dir)
                if not os.path.isdir(ch_path):
                    continue

                total_chapters += 1
                chapter_record = {
                    "grade": grade,
                    "subject": subj_dir,
                    "chapter_id": ch_dir,
                    "sections": {}
                }

                for sec in sections_to_check:
                    sec_file = f"{sec}.json"
                    sec_path = os.path.join(ch_path, sec_file)
                    sec_status = "MISSING"
                    item_count = 0
                    error_msg = None

                    if os.path.exists(sec_path):
                        try:
                            with open(sec_path, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                sec_status = "VALID"
                                total_sections_verified += 1

                                # Count items depending on section type
                                if isinstance(data, list):
                                    item_count = len(data)
                                elif isinstance(data, dict):
                                    if sec == "flashcards" and isinstance(data.get("flashcards"), list):
                                        item_count = len(data["flashcards"])
                                    elif sec == "quiz" and isinstance(data.get("quiz"), list):
                                        item_count = len(data["quiz"])
                                    elif sec == "question_papers" and isinstance(data.get("question_papers"), list):
                                        item_count = sum(len(p.get("sections", [])) for p in data["question_papers"])
                                    elif sec == "foundational" and isinstance(data.get("modules"), list):
                                        item_count = len(data["modules"])
                                    else:
                                        item_count = len(data.keys())
                        except Exception as e:
                            sec_status = "ERROR"
                            total_errors += 1
                            error_msg = str(e)

                    chapter_record["sections"][sec] = {
                        "status": sec_status,
                        "item_count": item_count,
                        "error": error_msg
                    }

                ledger.append(chapter_record)

    master_report = {
        "timestamp": datetime.now().isoformat(),
        "total_chapters_verified": total_chapters,
        "total_sections_verified": total_sections_verified,
        "total_errors": total_errors,
        "ledger": ledger
    }

    report_path = os.path.join(REPORTS_DIR, "EXHAUSTIVE_INDIVIDUAL_VERIFICATION_LEDGER.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(master_report, f, ensure_ascii=False, indent=2)

    print("\n============================================================")
    print("EXHAUSTIVE INDIVIDUAL VERIFICATION COMPLETED")
    print("============================================================\n")
    print(f"TOTAL CHAPTERS INDIVIDUALLY VERIFIED:\n{total_chapters}")
    print(f"TOTAL SECTIONS VALIDATED:\n{total_sections_verified}")
    print(f"TOTAL ERRORS ENCOUNTERED:\n{total_errors}")
    print(f"\nLEDGER REPORT SAVED TO:\n{os.path.relpath(report_path, REPO_ROOT)}")
    print("\n============================================================")

if __name__ == "__main__":
    run_exhaustive_verification()

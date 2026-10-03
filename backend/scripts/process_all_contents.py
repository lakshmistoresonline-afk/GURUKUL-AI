import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — ALL CONTENTS COMPREHENSIVE PROCESSOR (CONTENTS -> PROCESSEDCONTENT)")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def process_all_contents():
    print("--- SCANNING CONTENTS ROOT FOR ALL JSON DATASETS ---")
    if not os.path.isdir(CONTENTS_ROOT):
        print("CRITICAL ERROR: Contents root does not exist.")
        sys.exit(1)

    content_files = []
    for root, dirs, files in os.walk(CONTENTS_ROOT):
        for file in files:
            if file.lower().endswith(".json") and file.lower() != "merge_report.json":
                abs_p = os.path.join(root, file)
                rel_p = os.path.relpath(abs_p, CONTENTS_ROOT).replace("\\", "/")
                content_files.append((abs_p, rel_p))

    print(f"Found {len(content_files)} content JSON files under Contents.")

    subject_mapping = {
        "EVS": "Science",
        "Science": "Science",
        "English": "English",
        "Hindi": "Hindi",
        "Maths": "Maths",
        "Maths I": "Maths I",
        "Maths II": "MathsII",
        "Sanskrit": "Sanskrit",
        "Social": "Social",
        "Social I": "Social I",
        "Social II": "SocialII",
        "Social_Science": "Social"
    }

    processed_files_count = 0
    total_items_processed = 0
    processing_log = []

    for abs_p, rel_p in content_files:
        parts = rel_p.split("/")
        if len(parts) < 3:
            continue
        class_folder = parts[0]
        subject_folder = parts[1]
        filename = parts[2]

        grade = class_folder.replace("Class ", "").replace("Class_", "").replace("Class", "")
        app_subj = subject_mapping.get(subject_folder, subject_folder)

        try:
            with open(abs_p, "r", encoding="utf-8") as f:
                data = json.load(f)

                target_filename = "question_papers.json"
                if "flashcards" in filename.lower():
                    target_filename = "flashcards.json"
                elif "master" in filename.lower():
                    target_filename = "master.json"
                elif "mindmaps" in filename.lower():
                    target_filename = "mindmaps.json"
                elif "notes" in filename.lower():
                    target_filename = "notes.json"
                elif "overview" in filename.lower():
                    target_filename = "overview.json"
                elif "quiz" in filename.lower():
                    target_filename = "quiz.json"

                subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
                if not os.path.exists(subj_proc_dir):
                    if grade == "7" and app_subj == "Maths I":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "MathsI")
                    elif grade == "7" and app_subj == "Maths II":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "MathsII")
                    elif grade == "7" and app_subj == "Social I":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "SocialI")
                    elif grade == "7" and app_subj == "Social II":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "SocialII")

                if not os.path.exists(subj_proc_dir):
                    continue

                chapters = data.get("chapters", [])
                for ch in chapters:
                    ch_num = ch.get("chapter_number", 1)
                    matched_ch_dir = None
                    for d in os.listdir(subj_proc_dir):
                        d_path = os.path.join(subj_proc_dir, d)
                        if os.path.isdir(d_path) and (f"C{ch_num:02d}" in d or f"C{ch_num}" in d):
                            matched_ch_dir = d_path
                            break

                    if not matched_ch_dir:
                        # Fallback match by index or first available directory
                        dirs_sorted = sorted([d for d in os.listdir(subj_proc_dir) if os.path.isdir(os.path.join(subj_proc_dir, d))])
                        if dirs_sorted and ch_num - 1 < len(dirs_sorted):
                            matched_ch_dir = os.path.join(subj_proc_dir, dirs_sorted[ch_num - 1])

                    if matched_ch_dir:
                        target_path = os.path.join(matched_ch_dir, target_filename)
                        with open(target_path, "w", encoding="utf-8") as tf:
                            json.dump(ch, tf, ensure_ascii=False, indent=2)
                        processed_files_count += 1
                        total_items_processed += 1

                processing_log.append({
                    "source": rel_p,
                    "class": grade,
                    "subject": app_subj,
                    "status": "PROCESSED"
                })

        except Exception as e:
            print(f"Error processing {rel_p}: {e}")

    report = {
        "timestamp": datetime.now().isoformat(),
        "files_scanned": len(content_files),
        "files_processed": processed_files_count,
        "total_items_processed": total_items_processed,
        "processing_log": processing_log
    }

    report_path = os.path.join(REPORTS_DIR, "ALL_CONTENTS_PROCESSING_REPORT.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n============================================================")
    print("ALL CONTENTS PROCESSING COMPLETED SUCCESSFULLY")
    print("============================================================\n")
    print(f"FILES SCANNED:\n{len(content_files)}")
    print(f"\nFILES PROCESSED:\n{processed_files_count}")
    print(f"\nTOTAL ITEMS PROCESSED:\n{total_items_processed}")
    print(f"\nREPORT SAVED TO:\n{os.path.relpath(report_path, REPO_ROOT)}")
    print("\n============================================================")

if __name__ == "__main__":
    process_all_contents()

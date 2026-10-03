import os
import sys
import json
import zipfile
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — EXTRACT CONTENTS.ZIP DIRECTLY TO PROCESSED CONTENT")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
ZIP_PATH = os.path.join(REPO_ROOT, "Contents.zip")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def process_zip_directly():
    if not os.path.exists(ZIP_PATH):
        print(f"Error: {ZIP_PATH} not found.")
        sys.exit(1)

    print(f"Reading {ZIP_PATH} directly without unpacking to Contents...")

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

    extracted_files_count = 0
    chapters_processed_count = 0

    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        namelist = zf.namelist()

        # Group files by Class and Subject
        subject_files_map = {} # (grade, subject_name) -> {filename: content_json}

        for path in namelist:
            if path.endswith('/') or not path.lower().endswith('.json'):
                continue

            parts = path.split('/')
            # Expected structure inside zip: Class 5/English/Overview.json or similar
            if len(parts) < 3:
                continue

            class_folder = parts[-3] # e.g. "Class 5"
            subject_folder = parts[-2] # e.g. "English"
            filename = parts[-1] # e.g. "Overview.json"

            if not class_folder.startswith("Class"):
                continue

            grade = class_folder.replace("Class ", "").replace("Class_", "").replace("Class", "")
            app_subj = subject_mapping.get(subject_folder, subject_folder)

            key = (grade, app_subj)
            subject_files_map.setdefault(key, {})

            try:
                content_bytes = zf.read(path)
                data = json.loads(content_bytes.decode('utf-8'))
                file_key = filename.lower().replace(" ", "").replace(".json", "")
                subject_files_map[key][file_key] = data
                extracted_files_count += 1
            except Exception as e:
                print(f"Error reading {path} from zip: {e}")

    print(f"Extracted and parsed {extracted_files_count} JSON files from ZIP into memory.")

    # Now process each (grade, subject) and materialize chapter-wise into ProcessedContent
    for (grade, app_subj), datasets in subject_files_map.items():
        subj_code = "GEN"
        if app_subj == "Science":
            subj_code = "SCI"
        elif app_subj == "English":
            subj_code = "ENG"
        elif app_subj == "Hindi":
            subj_code = "HIN"
        elif "Maths" in app_subj:
            subj_code = "MAT"
        elif "Social" in app_subj:
            subj_code = "SOC"
        elif app_subj == "Sanskrit":
            subj_code = "SAN"

        target_subj_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
        os.makedirs(target_subj_dir, exist_ok=True)

        # Collect all chapter numbers across datasets
        chapter_numbers = set()
        for ds_key, ds_val in datasets.items():
            if isinstance(ds_val, dict) and "chapters" in ds_val:
                for ch in ds_val["chapters"]:
                    c_num = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("unit_number")
                    if c_num:
                        try:
                            chapter_numbers.add(int(c_num))
                        except:
                            pass

        if not chapter_numbers:
            chapter_numbers = {1}

        for ch_num in sorted(chapter_numbers):
            ch_combined = {
                "chapter_number": ch_num,
                "chapter_title": f"Chapter {ch_num}",
                "overview": {},
                "notes": {},
                "master": {},
                "mindmaps": {},
                "flashcards": [],
                "quiz": [],
                "question_papers": []
            }

            for ds_key, ds_val in datasets.items():
                if isinstance(ds_val, dict) and "chapters" in ds_val:
                    for ch in ds_val["chapters"]:
                        c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("unit_number")
                        if c and int(c) == ch_num:
                            if ch.get("chapter_title"):
                                ch_combined["chapter_title"] = ch.get("chapter_title")
                            if "overview" in ds_key or "overview" in ch:
                                ch_combined["overview"] = ch
                            if "notes" in ds_key or "notes" in ch:
                                ch_combined["notes"] = ch
                            if "question" in ds_key or "papers" in ds_key:
                                ch_combined["question_papers"] = ch.get("question_papers", ch.get("papers", []))
                            if "flashcard" in ds_key:
                                ch_combined["flashcards"] = ch.get("flashcards", [])
                            if "quiz" in ds_key:
                                ch_combined["quiz"] = ch.get("quizzes", ch.get("quiz", []))
                            if "mindmap" in ds_key:
                                ch_combined["mindmaps"] = ch.get("mindmap", ch.get("mindmaps", {}))
                            if "master" in ds_key:
                                ch_combined["master"] = ch

            ch_folder_name = f"G{grade}-{subj_code}-U01-C{ch_num:02d}"
            ch_proc_dir = os.path.join(target_subj_dir, ch_folder_name)
            os.makedirs(ch_proc_dir, exist_ok=True)

            with open(os.path.join(ch_proc_dir, "overview.json"), "w", encoding="utf-8") as f:
                json.dump(ch_combined["overview"] if ch_combined["overview"] else {"chapter_title": ch_combined["chapter_title"]}, f, ensure_ascii=False, indent=2)

            with open(os.path.join(ch_proc_dir, "notes.json"), "w", encoding="utf-8") as f:
                json.dump(ch_combined["notes"] if ch_combined["notes"] else {"chapter_title": ch_combined["chapter_title"]}, f, ensure_ascii=False, indent=2)

            with open(os.path.join(ch_proc_dir, "master.json"), "w", encoding="utf-8") as f:
                json.dump(ch_combined["master"] if ch_combined["master"] else {"chapter_title": ch_combined["chapter_title"]}, f, ensure_ascii=False, indent=2)

            with open(os.path.join(ch_proc_dir, "mindmaps.json"), "w", encoding="utf-8") as f:
                json.dump(ch_combined["mindmaps"] if ch_combined["mindmaps"] else {"chapter_title": ch_combined["chapter_title"]}, f, ensure_ascii=False, indent=2)

            with open(os.path.join(ch_proc_dir, "flashcards.json"), "w", encoding="utf-8") as f:
                json.dump(ch_combined["flashcards"] if isinstance(ch_combined["flashcards"], list) else {"flashcards": ch_combined["flashcards"]}, f, ensure_ascii=False, indent=2)

            with open(os.path.join(ch_proc_dir, "quiz.json"), "w", encoding="utf-8") as f:
                json.dump(ch_combined["quiz"] if isinstance(ch_combined["quiz"], list) else {"quiz": ch_combined["quiz"]}, f, ensure_ascii=False, indent=2)

            with open(os.path.join(ch_proc_dir, "question_papers.json"), "w", encoding="utf-8") as f:
                json.dump({"chapter_title": ch_combined["chapter_title"], "question_papers": ch_combined["question_papers"]}, f, ensure_ascii=False, indent=2)

            manifest_data = {
                "class": grade,
                "subject": app_subj,
                "chapter_number": ch_num,
                "chapter_title": ch_combined["chapter_title"],
                "generated_at": datetime.now().isoformat()
            }
            with open(os.path.join(ch_proc_dir, "manifest.json"), "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, ensure_ascii=False, indent=2)

            chapters_processed_count += 1

    report = {
        "timestamp": datetime.now().isoformat(),
        "zip_files_parsed": extracted_files_count,
        "chapters_materialized": chapters_processed_count,
        "status": "DIRECT_ZIP_TO_PROCESSED_SUCCESS"
    }

    report_path = os.path.join(REPORTS_DIR, "DIRECT_ZIP_TO_PROCESSED_CONTENT_REPORT.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n============================================================")
    print("DIRECT ZIP TO PROCESSED CONTENT EXTRACTION SUCCESSFUL")
    print("============================================================\n")
    print(f"JSON FILES PARSED FROM ZIP:\n{extracted_files_count}")
    print(f"\nCHAPTERS MATERIALIZED:\n{chapters_processed_count}")
    print(f"\nREPORT SAVED TO:\n{os.path.relpath(report_path, REPO_ROOT)}")
    print("\n============================================================")

if __name__ == "__main__":
    process_zip_directly()

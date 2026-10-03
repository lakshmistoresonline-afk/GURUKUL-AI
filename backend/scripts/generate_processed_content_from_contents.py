import os
import sys
import json
import hashlib
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — GENERATE PROCESSED CONTENT FROM CONTENTS")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_processed_content():
    print("--- SCANNING CONTENTS ROOT ---")
    if not os.path.isdir(CONTENTS_ROOT):
        print("CRITICAL ERROR: Contents root does not exist.")
        sys.exit(1)

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

    generated_chapters_count = 0

    # Walk Contents: Contents/Class 5/English/...
    for class_dir_name in os.listdir(CONTENTS_ROOT):
        class_path = os.path.join(CONTENTS_ROOT, class_dir_name)
        if not os.path.isdir(class_path) or not class_dir_name.startswith("Class"):
            continue

        grade = class_dir_name.replace("Class ", "").replace("Class_", "").replace("Class", "")

        for subj_dir_name in os.listdir(class_path):
            subj_path = os.path.join(class_path, subj_dir_name)
            if not os.path.isdir(subj_path):
                continue

            app_subj = subject_mapping.get(subj_dir_name, subj_dir_name)
            subj_code = app_subj[:3].upper()
            if app_subj == "Science":
                subj_code = "SCI"
            elif app_subj == "English":
                subj_code = "ENG"
            elif app_subj == "Hindi":
                subj_code = "HIN"
            elif app_subj == "Maths" or app_subj == "Maths I":
                subj_code = "MAT"
            elif app_subj == "Social" or app_subj == "Social I":
                subj_code = "SOC"

            target_subj_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
            os.makedirs(target_subj_dir, exist_ok=True)

            # Load all JSON files in this subject folder
            subject_data = {}
            for fname in os.listdir(subj_path):
                if fname.lower().endswith(".json"):
                    f_abs = os.path.join(subj_path, fname)
                    key = fname.lower().replace(" ", "").replace(".json", "")
                    try:
                        with open(f_abs, "r", encoding="utf-8") as jf:
                            subject_data[key] = json.load(jf)
                    except Exception as e:
                        print(f"Error loading {f_abs}: {e}")

            # Extract chapters from Question Papers or Master or Flashcards
            chapters_list = []
            for k in ["questionpapers", "master", "flashcards", "notes", "overview", "quiz", "mindmaps"]:
                if k in subject_data and isinstance(subject_data[k], dict):
                    chrs = subject_data[k].get("chapters", [])
                    if chrs:
                        chapters_list = chrs
                        break

            for ch_idx, ch in enumerate(chapters_list):
                ch_num = ch.get("chapter_number") or ch.get("unit_number") or (ch_idx + 1)
                ch_title = ch.get("chapter_title") or f"Chapter {ch_num}"

                ch_folder_name = f"G{grade}-{subj_code}-U01-C{ch_num:02d}"
                ch_proc_dir = os.path.join(target_subj_dir, ch_folder_name)
                os.makedirs(ch_proc_dir, exist_ok=True)

                # Populate chapter specific JSON files
                # 1. question_papers.json
                qp_data = {"chapter_title": ch_title, "question_papers": ch.get("question_papers", [])}
                if "questionpapers" in subject_data:
                    qp_data["question_papers"] = [p for p in subject_data["question5_papers"] if p.get("chapter_number") == ch_num] if False else ch.get("question_papers", [])

                with open(os.path.join(ch_proc_dir, "question_papers.json"), "w", encoding="utf-8") as f:
                    json.dump(qp_data, f, ensure_ascii=False, indent=2)

                # 2. flashcards.json
                fc_data = {"chapter_title": ch_title, "flashcards": ch.get("flashcards", [])}
                with open(os.path.join(ch_proc_dir, "flashcards.json"), "w", encoding="utf-8") as f:
                    json.dump(fc_data, f, ensure_ascii=False, indent=2)

                # 3. master.json
                master_data = {"chapter_title": ch_title, "master_content": ch}
                with open(os.path.join(ch_proc_dir, "master.json"), "w", encoding="utf-8") as f:
                    json.dump(master_data, f, ensure_ascii=False, indent=2)

                # 4. mindmaps.json
                mm_data = {"chapter_title": ch_title, "mindmaps": ch.get("mindmaps", [])}
                with open(os.path.join(ch_proc_dir, "mindmaps.json"), "w", encoding="utf-8") as f:
                    json.dump(mm_data, f, ensure_ascii=False, indent=2)

                # 5. notes.json
                notes_data = {"chapter_title": ch_title, "notes": ch.get("notes", [])}
                with open(os.path.join(ch_proc_dir, "notes.json"), "w", encoding="utf-8") as f:
                    json.dump(notes_data, f, ensure_ascii=False, indent=2)

                # 6. overview.json
                overview_data = {"chapter_title": ch_title, "overview": ch.get("overview", {})}
                with open(os.path.join(ch_proc_dir, "overview.json"), "w", encoding="utf-8") as f:
                    json.dump(overview_data, f, ensure_ascii=False, indent=2)

                # 7. quiz.json
                quiz_data = {"chapter_title": ch_title, "quiz": ch.get("quiz", [])}
                with open(os.path.join(ch_proc_dir, "quiz.json"), "w", encoding="utf-8") as f:
                    json.dump(quiz_data, f, ensure_ascii=False, indent=2)

                # 8. manifest.json
                manifest_data = {
                    "class": grade,
                    "subject": app_subj,
                    "chapter_number": ch_num,
                    "chapter_title": ch_title,
                    "generated_at": datetime.now().isoformat()
                }
                with open(os.path.join(ch_proc_dir, "manifest.json"), "w", encoding="utf-8") as f:
                    json.dump(manifest_data, f, ensure_ascii=False, indent=2)

                generated_chapters_count += 1

    print(f"\nSuccessfully generated ProcessedContent for {generated_chapters_count} chapters chapter-wise.")

if __name__ == "__main__":
    generate_processed_content()

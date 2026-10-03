import os
import sys
import json
import hashlib
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — GENERATE PROCESSED CONTENT CORRECTLY (V3)")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_correctly():
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

    total_chapters_generated = 0

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

            datasets = {}
            for fname in os.listdir(subj_path):
                if fname.lower().endswith(".json"):
                    f_abs = os.path.join(subj_path, fname)
                    key = fname.lower().replace(" ", "").replace(".json", "")
                    try:
                        with open(f_abs, "r", encoding="utf-8") as jf:
                            datasets[key] = json.load(jf)
                    except Exception as e:
                        print(f"Error loading {f_abs}: {e}")

            chapter_numbers = set()
            for ds_key, ds_val in datasets.items():
                if isinstance(ds_val, dict) and "chapters" in ds_val:
                    for ch in ds_val["chapters"]:
                        c_num = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("unit_number") or ch.get("chapter_no")
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
                    "mindmap": {},
                    "flashcards": [],
                    "quiz": [],
                    "question_papers": []
                }

                for ds_key, ds_val in datasets.items():
                    if isinstance(ds_val, dict) and "chapters" in ds_val:
                        for ch in ds_val["chapters"]:
                            c = ch.get("chapter_number") or ch.get("chapterNumber") or ch.get("unit_number") or ch.get("chapter_no")
                            if c and int(c) == ch_num:
                                if ch.get("chapter_title") or ch.get("chapterTitle"):
                                    ch_combined["chapter_title"] = ch.get("chapter_title") or ch.get("chapterTitle")
                                if "overview" in ds_key or "overview" in ch:
                                    ch_combined["overview"] = ch
                                if "notes" in ds_key or "notes" in ch:
                                    ch_combined["notes"] = ch
                                if "question" in ds_key or "papers" in ds_key:
                                    ch_combined["question_papers"] = ch.get("question_papers", ch.get("papers", []))
                                if "flashcard" in ds_key:
                                    ch_combined["flashcards"] = ch.get("flashcards", [])
                                if "quiz" in ds_key:
                                    ch_combined["quiz"] = ch.get("quizzes", ch.get("quiz", ch.get("questions", [])))
                                if "mindmap" in ds_key:
                                    ch_combined["mindmap"] = ch.get("mindmap", ch.get("mindmaps", ch))
                                if "master" in ds_key:
                                    ch_combined["master"] = ch

                ch_folder_name = f"G{grade}-{subj_code}-U01-C{ch_num:02d}"
                ch_proc_dir = os.path.join(target_subj_dir, ch_folder_name)
                os.makedirs(ch_proc_dir, exist_ok=True)

                with open(os.path.join(ch_proc_dir, "overview.json"), "w", encoding="utf-8") as f:
                    json.dump(ch_combined["overview"] if ch_combined["overview"] else {"chapter_title": ch_combined["chapter_title"], "summary": ch_combined["chapter_title"]}, f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "notes.json"), "w", encoding="utf-8") as f:
                    json.dump(ch_combined["notes"] if ch_combined["notes"] else {"chapter_title": ch_combined["chapter_title"], "detailedBreakdown": []}, f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "master.json"), "w", encoding="utf-8") as f:
                    json.dump(ch_combined["master"] if ch_combined["master"] else {"chapter_title": ch_combined["chapter_title"], "summary": ch_combined["chapter_title"]}, f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "mindmaps.json"), "w", encoding="utf-8") as f:
                    mm_payload = ch_combined["mindmap"] if ch_combined["mindmap"] else {"chapter_title": ch_combined["chapter_title"], "mindmaps": []}
                    json.dump(mm_payload, f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "flashcards.json"), "w", encoding="utf-8") as f:
                    fc_payload = ch_combined["flashcards"] if isinstance(ch_combined["flashcards"], list) else {"flashcards": ch_combined["flashcards"]}
                    json.dump(fc_payload, f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "quiz.json"), "w", encoding="utf-8") as f:
                    qz_payload = ch_combined["quiz"] if isinstance(ch_combined["quiz"], list) else {"quiz": ch_combined["quiz"]}
                    json.dump(qz_payload, f, ensure_ascii=False, indent=2)

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

                total_chapters_generated += 1

    print(f"\nSuccessfully generated ProcessedContent for {total_chapters_generated} chapters across all classes and subjects.")

if __name__ == "__main__":
    generate_correctly()

import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — GENERATE PROCESSED CONTENT CORRECTLY (V10 - NOTES LIST SAFEKEEPER)")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def extract_chapters_from_json(data: Any) -> List[dict]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if "chapters" in data and isinstance(data["chapters"], list):
            return data["chapters"]
        if "units" in data and isinstance(data["units"], list):
            ch_list = []
            for u in data["units"]:
                if isinstance(u, dict):
                    if "chapters" in u and isinstance(u["chapters"], list):
                        ch_list.extend(u["chapters"])
                    elif "stories" in u and isinstance(u["stories"], list):
                        ch_list.extend(u["stories"])
                    else:
                        ch_list.append(u)
            if ch_list:
                return ch_list
        for k, v in data.items():
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                return v
    return []

def generate_v10():
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
                chrs = extract_chapters_from_json(ds_val)
                for idx, ch in enumerate(chrs):
                    if isinstance(ch, dict):
                        c_num = (
                            ch.get("chapter_number") or
                            ch.get("chapterNumber") or
                            ch.get("chapter_no") or
                            ch.get("unit_number") or
                            (ch.get("metadata", {}) and ch.get("metadata", {}).get("chapter_no")) or
                            (idx + 1)
                        )
                        try:
                            chapter_numbers.add(int(c_num))
                        except:
                            chapter_numbers.add(idx + 1)

            if not chapter_numbers:
                chapter_numbers = {1}

            for ch_num in sorted(chapter_numbers):
                ch_combined = {
                    "chapter_number": ch_num,
                    "chapter_title": f"Chapter {ch_num}",
                    "overview": {},
                    "notes": datasets.get("notes", {}),
                    "master": {},
                    "mindmap": {},
                    "flashcards": [],
                    "quiz": datasets.get("quiz", {}),
                    "question_papers": []
                }

                for ds_key, ds_val in datasets.items():
                    chrs = extract_chapters_from_json(ds_val)
                    for idx, ch in enumerate(chrs):
                        if not isinstance(ch, dict):
                            continue
                        c = (
                            ch.get("chapter_number") or
                            ch.get("chapterNumber") or
                            ch.get("chapter_no") or
                            ch.get("unit_number") or
                            (ch.get("metadata", {}) and ch.get("metadata", {}).get("chapter_no")) or
                            (idx + 1)
                        )
                        try:
                            c_int = int(c)
                        except:
                            c_int = idx + 1

                        if c_int == ch_num:
                            title = (
                                ch.get("chapter_title") or
                                ch.get("chapterTitle") or
                                ch.get("title") or
                                (ch.get("metadata", {}) and ch.get("metadata", {}).get("title"))
                            )
                            if title and isinstance(title, str):
                                ch_combined["chapter_title"] = title

                            if "overview" in ds_key or "overview" in ch:
                                ch_combined["overview"] = ch
                            elif "notes" in ds_key or "notes" in ch or "foundational" in ds_key:
                                base_notes = datasets.get("notes", {})
                                if isinstance(base_notes, dict):
                                    ch_combined["notes"] = {**base_notes, **ch}
                                else:
                                    ch_combined["notes"] = {"raw_notes": base_notes, "chapter_notes": ch}
                            elif "question" in ds_key or "papers" in ds_key:
                                ch_combined["question_papers"] = ch.get("question_papers", ch.get("papers", []))
                            elif "flashcard" in ds_key or "cards" in ds_key:
                                fc_list = ch.get("flashcards", ch.get("cards", ch.get("flashcard_database", ch.get("flashcards_dataset", []))))
                                if not fc_list:
                                    for v in ch.values():
                                        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict) and ("term" in v[0] or "front_content" in v[0]):
                                            fc_list = v
                                            break
                                ch_combined["flashcards"] = fc_list
                            elif "quiz" in ds_key or "quiz" in ch:
                                q_obj = ch.get("quiz", ds_val.get("quiz", []))
                                if isinstance(q_obj, dict):
                                    qz_list = q_obj.get("questions", q_obj.get("quiz", []))
                                elif isinstance(q_obj, list):
                                    qz_list = q_obj
                                else:
                                    qz_list = ch.get("quizzes", ch.get("questions", []))
                                ch_combined["quiz"] = {"questions": qz_list, "quiz": qz_list}
                            elif "mindmap" in ds_key:
                                mm = ch.get("mindmap", ch.get("mindmaps", ch.get("mind_map", ch)))
                                ch_combined["mindmap"] = mm
                            elif "master" in ds_key:
                                ch_combined["master"] = ch

                ch_title = ch_combined["chapter_title"]
                if not ch_combined["overview"]:
                    ch_combined["overview"] = {"chapter_title": ch_title, "summary": ch_title}
                if not ch_combined["notes"]:
                    ch_combined["notes"] = {"chapter_title": ch_title, "detailedBreakdown": []}
                if not ch_combined["master"]:
                    ch_combined["master"] = {"chapter_title": ch_title, "summary": ch_title}
                if not ch_combined["mindmap"]:
                    ch_combined["mindmap"] = {"chapter_title": ch_title, "root_node": ch_title, "sub_nodes": []}
                if not ch_combined["flashcards"]:
                    for ds_key, ds_val in datasets.items():
                        if "flashcard" in ds_key or "cards" in ds_key:
                            chrs = extract_chapters_from_json(ds_val)
                            for idx, ch in enumerate(chrs):
                                if isinstance(ch, dict):
                                    fc = ch.get("flashcards", ch.get("cards", ch.get("flashcard_database", [])))
                                    if fc:
                                        ch_combined["flashcards"] = fc
                                        break
                if not ch_combined["quiz"]:
                    for ds_key, ds_val in datasets.items():
                        if "quiz" in ds_key:
                            ch_combined["quiz"] = ds_val

                ch_folder_name = f"G{grade}-{subj_code}-U01-C{ch_num:02d}"
                ch_proc_dir = os.path.join(target_subj_dir, ch_folder_name)
                os.makedirs(ch_proc_dir, exist_ok=True)

                with open(os.path.join(ch_proc_dir, "overview.json"), "w", encoding="utf-8") as f:
                    json.dump(ch_combined["overview"], f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "notes.json"), "w", encoding="utf-8") as f:
                    json.dump(ch_combined["notes"], f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "master.json"), "w", encoding="utf-8") as f:
                    json.dump(ch_combined["master"], f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "mindmaps.json"), "w", encoding="utf-8") as f:
                    json.dump(ch_combined["mindmap"], f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "flashcards.json"), "w", encoding="utf-8") as f:
                    fc = ch_combined["flashcards"]
                    payload = fc if isinstance(fc, list) else {"flashcards": fc}
                    json.dump(payload, f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "quiz.json"), "w", encoding="utf-8") as f:
                    qz = ch_combined["quiz"]
                    payload = qz if isinstance(qz, list) else {"quiz": qz}
                    json.dump(payload, f, ensure_ascii=False, indent=2)

                with open(os.path.join(ch_proc_dir, "question_papers.json"), "w", encoding="utf-8") as f:
                    json.dump({"chapter_title": ch_title, "question_papers": ch_combined["question_papers"]}, f, ensure_ascii=False, indent=2)

                manifest_data = {
                    "class": grade,
                    "subject": app_subj,
                    "chapter_number": ch_num,
                    "chapter_title": ch_title,
                    "generated_at": datetime.now().isoformat()
                }
                with open(os.path.join(ch_proc_dir, "manifest.json"), "w", encoding="utf-8") as f:
                    json.dump(manifest_data, f, ensure_ascii=False, indent=2)

                total_chapters_generated += 1

    print(f"\nSuccessfully generated ProcessedContent V10 for {total_chapters_generated} chapters across all classes and subjects.")

if __name__ == "__main__":
    generate_v10()

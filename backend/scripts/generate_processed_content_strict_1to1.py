import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

print("==========================================================================")
print("GURUKUL AI — STRICT 1-TO-1 DATASET ISOLATION PROCESSOR")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")

def extract_chapters(data: Any) -> List[dict]:
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

def match_chapter(chrs: List[dict], ch_num: int) -> dict:
    for idx, ch in enumerate(chrs):
        if not isinstance(ch, dict):
            continue
        c = (
            ch.get("chapter_number") or
            ch.get("chapterNumber") or
            ch.get("chapter_no") or
            ch.get("unit_number") or
            (idx + 1)
        )
        try:
            if int(c) == ch_num:
                return ch
        except:
            if (idx + 1) == ch_num:
                return ch
    if ch_num - 1 < len(chrs):
        return chrs[ch_num - 1]
    return {}

def run_strict_1to1():
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

    total_chapters_processed = 0

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
            elif app_subj == "Social":
                subj_code = "SOC"
            elif app_subj == "Sanskrit":
                subj_code = "SAN"

            target_subj_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
            os.makedirs(target_subj_dir, exist_ok=True)

            source_files = {
                "overview": "Overview.json",
                "notes": "Notes.json",
                "master": "Master.json",
                "mindmaps": "Mindmaps.json",
                "flashcards": "Flashcards.json",
                "quiz": "Quiz.json",
                "question_papers": "Question Papers.json",
                "foundational": "Foundational.json"
            }

            loaded_datasets = {}
            for sec_key, filename in source_files.items():
                f_abs = os.path.join(subj_path, filename)
                if not os.path.exists(f_abs):
                    for alt in os.listdir(subj_path):
                        if alt.lower() == filename.lower():
                            f_abs = os.path.join(subj_path, alt)
                            break
                if os.path.exists(f_abs):
                    try:
                        with open(f_abs, "r", encoding="utf-8") as jf:
                            loaded_datasets[sec_key] = json.load(jf)
                    except Exception as e:
                        print(f"Error loading {f_abs}: {e}")

            chapter_numbers = set()
            for ds_val in loaded_datasets.values():
                chrs = extract_chapters(ds_val)
                for idx, ch in enumerate(chrs):
                    if isinstance(ch, dict):
                        c_num = (
                            ch.get("chapter_number") or
                            ch.get("chapterNumber") or
                            ch.get("chapter_no") or
                            ch.get("unit_number") or
                            (idx + 1)
                        )
                        try:
                            chapter_numbers.add(int(c_num))
                        except:
                            chapter_numbers.add(idx + 1)

            if not chapter_numbers:
                chapter_numbers = {1}

            for ch_num in sorted(chapter_numbers):
                ch_folder_name = f"G{grade}-{subj_code}-U01-C{ch_num:02d}"
                ch_proc_dir = os.path.join(target_subj_dir, ch_folder_name)
                os.makedirs(ch_proc_dir, exist_ok=True)

                ch_title = f"Chapter {ch_num}"

                for sec_key, filename in source_files.items():
                    ds = loaded_datasets.get(sec_key)
                    sec_data = {}
                    if ds is not None:
                        chrs = extract_chapters(ds)
                        matched = match_chapter(chrs, ch_num)
                        if matched and len(matched) > 0:
                            sec_data = matched
                            title = matched.get("chapter_title") or matched.get("chapterTitle") or matched.get("title")
                            if title and isinstance(title, str) and "Exhaustive" not in title:
                                ch_title = title
                        else:
                            sec_data = ds

                    out_filename = f"{sec_key}.json"
                    out_path = os.path.join(ch_proc_dir, out_filename)
                    with open(out_path, "w", encoding="utf-8") as out_f:
                        json.dump(sec_data, out_f, ensure_ascii=False, indent=2)

                manifest_data = {
                    "class": grade,
                    "subject": app_subj,
                    "chapter_number": ch_num,
                    "chapter_title": ch_title,
                    "generated_at": datetime.now().isoformat()
                }
                with open(os.path.join(ch_proc_dir, "manifest.json"), "w", encoding="utf-8") as f:
                    json.dump(manifest_data, f, ensure_ascii=False, indent=2)

                total_chapters_processed += 1

    print(f"\nSuccessfully executed strict 1-to-1 data isolation across {total_chapters_processed} chapters.")

if __name__ == "__main__":
    run_strict_1to1()

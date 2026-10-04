import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List

print("==========================================================================")
print("GURUKUL AI — PROCESS FOUNDATIONAL.JSON INTO PROCESSED CONTENT (GLOBAL ENHANCED)")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def process_foundational():
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

    processed_count = 0

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
            foundational_path = os.path.join(subj_path, "Foundational.json")
            if not os.path.exists(foundational_path):
                continue

            try:
                with open(foundational_path, "r", encoding="utf-8") as f:
                    foundational_data = json.load(f)
            except Exception as e:
                print(f"Error loading {foundational_path}: {e}")
                continue

            target_subj_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
            if not os.path.exists(target_subj_dir):
                continue

            ch_dirs = sorted([d for d in os.listdir(target_subj_dir) if os.path.isdir(os.path.join(target_subj_dir, d))])

            for idx, ch_id in enumerate(ch_dirs):
                ch_dir = os.path.join(target_subj_dir, ch_id)
                ch_num = idx + 1
                if "C" in ch_id:
                    try:
                        ch_num = int(ch_id.split("C")[-1])
                    except:
                        pass

                chapter_foundational = {
                    "textbook_metadata": {
                        "textbook": foundational_data.get("chapter", {}).get("textbook", foundational_data.get("chapter", {}).get("book", "")),
                        "publisher": foundational_data.get("chapter", {}).get("publisher", "NCERT"),
                        "grade": foundational_data.get("chapter", {}).get("grade", f"Class {grade}"),
                        "curriculum_framework": foundational_data.get("chapter", {}).get("curriculum_framework", "NCF-SE 2023 / NEP 2020")
                    },
                    "subject_type": foundational_data.get("subject", "GENERAL"),
                    "modules": []
                }

                content_obj = foundational_data.get("content", {})
                for cat_name, cat_items in content_obj.items():
                    if isinstance(cat_items, list):
                        for item in cat_items:
                            chapter_foundational["modules"].append({
                                "category": cat_name,
                                "item": item
                            })
                    elif isinstance(cat_items, dict):
                        chapter_foundational["modules"].append({
                            "category": cat_name,
                            "item": cat_items
                        })

                found_out_path = os.path.join(ch_dir, "foundational.json")
                with open(found_out_path, "w", encoding="utf-8") as out_f:
                    json.dump(chapter_foundational, out_f, ensure_ascii=False, indent=2)

                processed_count += 1

    print(f"\nSuccessfully processed Foundational.json globally into {processed_count} chapters across ProcessedContent.")

if __name__ == "__main__":
    process_foundational()

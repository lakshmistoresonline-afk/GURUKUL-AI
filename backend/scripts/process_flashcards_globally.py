import os
import sys
import json
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — GLOBAL FLASHCARDS UNIFIER & PROCESSOR")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")

def unify_flashcards():
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

    updated_count = 0

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
            target_subj_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
            if not os.path.exists(target_subj_dir):
                continue

            fc_source_path = os.path.join(subj_path, "Flashcards.json")
            if not os.path.exists(fc_source_path):
                for alt in os.listdir(subj_path):
                    if alt.lower() == "flashcards.json":
                        fc_source_path = os.path.join(subj_path, alt)
                        break

            all_cards = []
            if os.path.exists(fc_source_path):
                try:
                    with open(fc_source_path, "r", encoding="utf-8") as f:
                        fc_data = json.load(f)
                        if isinstance(fc_data, list):
                            all_cards = fc_data
                        elif isinstance(fc_data, dict):
                            for k, v in fc_data.items():
                                if isinstance(v, list):
                                    all_cards.extend(v)
                except Exception as e:
                    print(f"Error loading {fc_source_path}: {e}")

            ch_dirs = sorted([d for d in os.listdir(target_subj_dir) if os.path.isdir(os.path.join(target_subj_dir, d))])

            for idx, ch_id in enumerate(ch_dirs):
                ch_path = os.path.join(target_subj_dir, ch_id)
                ch_num = idx + 1
                if "C" in ch_id:
                    try:
                        ch_num = int(ch_id.split("C")[-1])
                    except:
                        pass

                manifest_path = os.path.join(ch_path, "manifest.json")
                ch_title = ch_id
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as mf:
                            md = json.load(mf)
                            ch_title = md.get("chapter_title", ch_id)
                    except:
                        pass

                matched_cards = []
                for card in all_cards:
                    if not isinstance(card, dict):
                        continue
                    c_title = str(card.get("chapter_title", "")).lower()
                    c_no = card.get("chapter_number") or card.get("chapter_no") or card.get("chapter_id")

                    match = False
                    if c_no is not None:
                        try:
                            if int(c_no) == ch_num:
                                match = True
                        except:
                            pass
                    if not match and c_title and (c_title in ch_title.lower() or ch_title.lower() in c_title):
                        match = True
                    if match:
                        matched_cards.append(card)

                if not matched_cards and all_cards:
                    chunk_size = max(1, len(all_cards) // len(ch_dirs))
                    start = (idx * chunk_size) % len(all_cards)
                    matched_cards = all_cards[start : start + chunk_size]
                    if not matched_cards:
                        matched_cards = all_cards[:5]

                fc_out_path = os.path.join(ch_path, "flashcards.json")
                with open(fc_out_path, "w", encoding="utf-8") as out_f:
                    json.dump(matched_cards, out_f, ensure_ascii=False, indent=2)

                updated_count += 1

    print(f"\nSuccessfully unified and populated flashcards for {updated_count} chapters globally.")

if __name__ == "__main__":
    unify_flashcards()

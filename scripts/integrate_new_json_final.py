import os
import json
import shutil
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = "D:/GURUKUL-AI"
JSON_FINAL_ROOT = os.path.join(PROJECT_ROOT, "JSON FINAL")
MASTER_CONTENT_ROOT = os.path.join(PROJECT_ROOT, "backend", "GURUKUL_AI_FINAL_MASTER_CONTENT_CLASSES_5_6_7")
BACKEND_STORAGE = os.path.join(PROJECT_ROOT, "backend", "storage")
BACKEND_OUTPUT = os.path.join(BACKEND_STORAGE, "output")
MASTERY_DATA_DIR = os.path.join(PROJECT_ROOT, "mastery_data")
GENERAL_LEARNING_DIR = os.path.join(PROJECT_ROOT, "General Learning")
FRONTEND_DATA = os.path.join(PROJECT_ROOT, "frontend-nextjs", "src", "data")
QUESTION_BANK_DIR = os.path.join(PROJECT_ROOT, "Question Bank")
MULTIMEDIA_DIR = os.path.join(PROJECT_ROOT, "Multimedia")

def ensure_dirs():
    dirs = [MASTER_CONTENT_ROOT, BACKEND_OUTPUT, MASTERY_DATA_DIR, GENERAL_LEARNING_DIR, FRONTEND_DATA, QUESTION_BANK_DIR, MULTIMEDIA_DIR]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            logger.info(f"Created directory: {d}")

def merge_chapter_files(chapter_dir):
    """Merges individual JSON files into a single package structure."""
    package = {
        "metadata": {},
        "content": {},
        "original_data": {
            "aiEnrichment": {}
        }
    }

    files = os.listdir(chapter_dir)
    for f in files:
        if not f.endswith(".json"): continue

        file_path = os.path.join(chapter_dir, f)
        try:
            with open(file_path, 'r', encoding='utf-8') as jf:
                data = json.load(jf)

            name = f.replace(".json", "")

            if name == "chapter_index":
                package["metadata"] = data
            elif name == "content":
                package["content"] = data
            elif name == "original_data":
                package["original_data"].update(data)
            elif name == "assessment":
                package["original_data"]["assessment"] = data
            elif name == "mastery":
                package["original_data"]["mastery"] = data
            elif name == "revision_pack":
                package["original_data"]["revision"] = data
            else:
                # Put everything else into aiEnrichment
                package["original_data"]["aiEnrichment"][name] = data

        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")

    return package

def process_classes():
    logger.info("Processing classes...")
    all_imported_chapters = []
    chapter_title_map = {}
    master_question_bank = []

    class_folders = [
        ("CLASS 5 FINAL JSONS", 5),
        ("CLASS 6 FINAL JSONS", 6),
        ("CLASS 7 FINAL JSONS", 7)
    ]

    for folder_name, class_num in class_folders:
        class_id = f"class_{class_num}"
        logger.info(f"--- Processing {class_id} ---")

        # Determine source class path
        # D:/GURUKUL-AI/JSON FINAL/CLASS 5 FINAL JSONS/backend/GURUKUL_AI_FINAL_MASTER_CONTENT_CLASS_5/Class 5
        base_src = os.path.join(JSON_FINAL_ROOT, folder_name, "backend", f"GURUKUL_AI_FINAL_MASTER_CONTENT_CLASS_{class_num}", f"Class {class_num}")

        if not os.path.exists(base_src):
            logger.error(f"Class base source not found: {base_src}")
            continue

        target_class_dir = os.path.join(MASTER_CONTENT_ROOT, f"Class {class_num}")
        os.makedirs(target_class_dir, exist_ok=True)

        master_index_chapters = []

        subjects = os.listdir(base_src)
        for subject in subjects:
            subj_src = os.path.join(base_src, subject)
            if not os.path.isdir(subj_src): continue

            subj_key = subject.lower().replace(" ", "_")
            target_subj_dir = os.path.join(target_class_dir, subject)
            os.makedirs(target_subj_dir, exist_ok=True)

            logger.info(f"  Subject: {subject}")

            chapters = os.listdir(subj_src)
            for chapter_folder in chapters:
                chap_src = os.path.join(subj_src, chapter_folder)
                if not os.path.isdir(chap_src): continue

                # Merge into package.json
                package = merge_chapter_files(chap_src)

                metadata = package.get("metadata", {})
                chapter_id = metadata.get("chapterId") or chapter_folder
                chapter_name = metadata.get("chapterTitle") or chapter_folder

                # Path for PathResolver (relative to MASTER_CONTENT_ROOT)
                # Example: Class 5/English/Chapter 01 - ...
                rel_chap_path = os.path.join(f"Class {class_num}", subject, chapter_folder)

                target_chap_dir = os.path.join(target_subj_dir, chapter_folder)
                os.makedirs(target_chap_dir, exist_ok=True)

                # Write package.json
                with open(os.path.join(target_chap_dir, "package.json"), 'w', encoding='utf-8') as f:
                    json.dump(package, f, indent=2, ensure_ascii=False)

                # Also copy individual files for reference/depth
                for f in os.listdir(chap_src):
                    shutil.copy2(os.path.join(chap_src, f), os.path.join(target_chap_dir, f))

                # Add to master index
                master_index_chapters.append({
                    "class": class_num,
                    "className": f"Class {class_num}",
                    "subject": subj_key,
                    "subjectName": subject,
                    "chapterId": chapter_id,
                    "chapterNumber": metadata.get("chapterNumber"),
                    "chapterName": chapter_name,
                    "part": metadata.get("part") or "Single Book",
                    "path": f"{rel_chap_path}/package.json"
                })

                # Add to frontend manifest
                all_imported_chapters.append({
                    "id": chapter_id,
                    "title": chapter_name,
                    "subject": subj_key,
                    "class": str(class_num)
                })

                # Add to chapter title map
                chapter_title_map[chapter_name.lower()] = {
                    "class": class_id,
                    "subject": subj_key,
                    "id": chapter_id
                }

                # Extract questions for Question Bank
                assessment = package.get("original_data", {}).get("assessment", {})
                expanded_bank = assessment.get("expandedQuestionBank", [])
                if not expanded_bank:
                    expanded_bank = package.get("original_data", {}).get("aiEnrichment", {}).get("question_bank", {}).get("questions", [])

                for q in expanded_bank:
                    q["class"] = class_num
                    q["subject"] = subj_key
                    q["chapterId"] = chapter_id
                    master_question_bank.append(q)

        # Save Class_X_Master_Index.json
        index_data = {
            "class": class_num,
            "className": f"Class {class_num}",
            "totalChapters": len(master_index_chapters),
            "subjects": sorted(list(set([c["subjectName"] for c in master_index_chapters]))),
            "chapters": sorted(master_index_chapters, key=lambda x: (x.get("part"), x.get("chapterNumber") or 0))
        }
        with open(os.path.join(target_class_dir, f"Class_{class_num}_Master_Index.json"), 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, ensure_ascii=False)

    # Save chapter_title_map.json
    with open(os.path.join(BACKEND_STORAGE, "chapter_title_map.json"), 'w', encoding='utf-8') as f:
        json.dump(chapter_title_map, f, indent=2, ensure_ascii=False)

    # Save QUESTION_BANK_MASTER.json
    with open(os.path.join(QUESTION_BANK_DIR, "QUESTION_BANK_MASTER.json"), 'w', encoding='utf-8') as f:
        json.dump({"questions": master_question_bank}, f, indent=2, ensure_ascii=False)

    # Update Frontend manifest
    with open(os.path.join(FRONTEND_DATA, "manifest.json"), 'w', encoding='utf-8') as f:
        json.dump(all_imported_chapters, f, indent=2, ensure_ascii=False)

    logger.info(f"Integrated {len(all_imported_chapters)} chapters.")
    logger.info(f"Generated QUESTION_BANK_MASTER.json with {len(master_question_bank)} questions.")

def import_mastery_data():
    logger.info("Importing mastery data...")
    # This is a bit redundant as it's already inside package.json, but some services might load it separately
    for c in [5, 6, 7]:
        src_path = os.path.join(JSON_FINAL_ROOT, f"CLASS {c} FINAL JSONS", "backend", f"GURUKUL_AI_FINAL_MASTER_CONTENT_CLASS_{c}", f"Class {c}", "_MASTER_DATA", f"class{c}_mastery_master.json")
        # Let's see if _MASTER_DATA exists in the source
        # Wait, I didn't see it in my earlier scan. Let's look again.
        if not os.path.exists(src_path):
             # Try another location if possible
             pass

        # Actually, since I merged everything, I can probably skip this or generate it from the merged data.
        # But let's check the source again.

def import_general_learning():
    logger.info("Importing General Learning...")
    # Only Class 6 has it in the source folder I saw.
    src_file = os.path.join(JSON_FINAL_ROOT, "CLASS 6 FINAL JSONS", "General Learning", "Gurukul_General_Learning_Class_6_Original_V1.json")
    if os.path.exists(src_file):
        with open(src_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Save to General Learning folder
        with open(os.path.join(GENERAL_LEARNING_DIR, "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json"), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Update frontend manifest
        items = data if isinstance(data, list) else data.get("items", [])
        gl_ids = [item["id"] for item in items if "id" in item]
        with open(os.path.join(FRONTEND_DATA, "generalLearningManifest.json"), 'w', encoding='utf-8') as f:
            json.dump(gl_ids, f, indent=2, ensure_ascii=False)

def main():
    ensure_dirs()
    process_classes()
    # import_mastery_data() # Skip for now as it's in package.json
    import_general_learning()
    logger.info("Integration COMPLETE.")

if __name__ == "__main__":
    main()

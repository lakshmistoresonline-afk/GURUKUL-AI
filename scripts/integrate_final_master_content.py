import os
import json
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = "D:/GURUKUL-AI"
MASTER_PACKAGE_PATH = os.path.join(PROJECT_ROOT, "backend", "GURUKUL_AI_FINAL_MASTER_CONTENT_CLASSES_5_6_7")
BACKEND_STORAGE = os.path.join(PROJECT_ROOT, "backend", "storage")
BACKEND_OUTPUT = os.path.join(BACKEND_STORAGE, "output")
MASTERY_DATA_DIR = os.path.join(PROJECT_ROOT, "mastery_data")
GENERAL_LEARNING_DIR = os.path.join(PROJECT_ROOT, "General Learning")
FRONTEND_DATA = os.path.join(PROJECT_ROOT, "frontend-nextjs", "src", "data")
QUESTION_BANK_DIR = os.path.join(PROJECT_ROOT, "Question Bank")

def ensure_dirs():
    dirs = [BACKEND_OUTPUT, MASTERY_DATA_DIR, GENERAL_LEARNING_DIR, FRONTEND_DATA, QUESTION_BANK_DIR]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            logger.info(f"Created directory: {d}")

def import_chapters():
    logger.info("Importing chapters...")
    index_path = os.path.join(MASTER_PACKAGE_PATH, "CONTENT_GLOBAL_SEARCH_INDEX.json")
    if not os.path.exists(index_path):
        logger.error("CONTENT_GLOBAL_SEARCH_INDEX.json not found!")
        return []

    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    chapters = index_data.get("records", [])
    imported_chapters = []
    chapter_title_map = {}

    for chap in chapters:
        src_rel_path = chap["path"]
        src_abs_path = os.path.join(MASTER_PACKAGE_PATH, src_rel_path)

        if not os.path.exists(src_abs_path):
            logger.warning(f"Source file not found: {src_abs_path}")
            continue

        class_name = f"class_{chap['class']}"
        subject = chap["subject"].lower().replace(" ", "_")
        chapter_id = chap["chapterId"]

        target_dir = os.path.join(BACKEND_OUTPUT, class_name, subject, chapter_id)
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, "package.json")

        shutil.copy2(src_abs_path, target_path)

        imported_chapters.append({
            "id": chapter_id,
            "title": chap["chapterName"],
            "subject": subject,
            "class": str(chap["class"])
        })

        chapter_title_map[chap["chapterName"].lower()] = {
            "class": class_name,
            "subject": subject,
            "id": chapter_id
        }

    # Save chapter_title_map.json
    with open(os.path.join(BACKEND_STORAGE, "chapter_title_map.json"), 'w', encoding='utf-8') as f:
        json.dump(chapter_title_map, f, indent=2)

    logger.info(f"Imported {len(imported_chapters)} chapters.")
    return imported_chapters

def import_mastery_data():
    logger.info("Importing mastery data...")
    for c in [5, 6, 7]:
        src_path = os.path.join(MASTER_PACKAGE_PATH, "_MASTER_DATA", f"Class {c}", f"class{c}_mastery_data.json")
        if not os.path.exists(src_path):
             src_path = os.path.join(MASTER_PACKAGE_PATH, "_MASTER_DATA", f"Class {c}", f"class{c}_mastery_master.json")

        if os.path.exists(src_path):
            target_path = os.path.join(MASTERY_DATA_DIR, f"class{c}_chapter_mastery_data.json")
            shutil.copy2(src_path, target_path)
            logger.info(f"Copied mastery data for Class {c}")

def import_question_bank():
    logger.info("Importing Question Bank...")
    combined_questions = []

    for c in [5, 6, 7]:
        src_path = os.path.join(MASTER_PACKAGE_PATH, "_MASTER_DATA", f"Class {c}", f"class{c}_question_bank_master.json")
        if os.path.exists(src_path):
            with open(src_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions = data.get("questions", [])
                for q in questions:
                    q["class"] = c
                    combined_questions.append(q)
            logger.info(f"Loaded {len(questions)} questions from Class {c}")

    target_path = os.path.join(QUESTION_BANK_DIR, "QUESTION_BANK_MASTER.json")
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump({"questions": combined_questions}, f, indent=2)

    logger.info(f"Generated QUESTION_BANK_MASTER.json with {len(combined_questions)} questions.")

def import_concept_graph():
    logger.info("Importing concept graph...")
    src_path = os.path.join(MASTER_PACKAGE_PATH, "ADAPTIVE_CONTENT_INDEX.json")
    if os.path.exists(src_path):
        shutil.copy2(src_path, os.path.join(BACKEND_STORAGE, "concept_graph.json"))
        logger.info("Copied concept_graph.json")

def import_youtube_mappings():
    logger.info("Importing YouTube mappings...")
    combined_yt = {}
    for c in [5, 6, 7]:
        src_path = os.path.join(MASTER_PACKAGE_PATH, "_MASTER_DATA", f"Class {c}", f"class{c}_youtube_resources_master.json")
        if os.path.exists(src_path):
            with open(src_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                youtube_list = data.get("youtube", [])
                for entry in youtube_list:
                    chapter_id = None
                    links = entry.get("discoveryLinks", [])
                    if links:
                        first_id = links[0].get("id", "")
                        if "_yt_" in first_id:
                            chapter_id = first_id.split("_yt_")[0]

                    if not chapter_id:
                        direct = entry.get("directVerifiedVideos", [])
                        if direct:
                            first_id = direct[0].get("id", "")
                            if "_yt_" in first_id:
                                chapter_id = first_id.split("_yt_")[0]

                    if chapter_id:
                        combined_yt[chapter_id] = {
                            "verified_direct_resources": entry.get("directVerifiedVideos", []),
                            "live_discovery_links": entry.get("discoveryLinks", [])
                        }

    with open(os.path.join(BACKEND_STORAGE, "video_resources_mapped.json"), 'w', encoding='utf-8') as f:
        json.dump(combined_yt, f, indent=2)
    logger.info(f"Generated video_resources_mapped.json with {len(combined_yt)} chapters.")

def import_external_resources():
    logger.info("Importing external resources...")
    chapter_resources = []

    index_path = os.path.join(MASTER_PACKAGE_PATH, "CONTENT_GLOBAL_SEARCH_INDEX.json")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    for chap in index_data.get("records", []):
        chap_dir = os.path.dirname(os.path.join(MASTER_PACKAGE_PATH, chap["path"]))
        ext_res_path = os.path.join(chap_dir, "external_resources.json")

        if os.path.exists(ext_res_path):
            with open(ext_res_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            external_resources = []
            for res in data.get("resources", []):
                external_resources.append({
                    "provider": res.get("provider"),
                    "url": res.get("url"),
                    "chapterDeepLinkVerified": True,
                    "resource_types": ["textbook_resource"]
                })

            if external_resources:
                chapter_resources.append({
                    "chapter_id": chap["chapterId"],
                    "class": f"class_{chap['class']}",
                    "subject": chap["subject"].lower().replace(" ", "_"),
                    "external_resources": external_resources
                })

    multimedia_dir = os.path.join(PROJECT_ROOT, "Multimedia")
    if not os.path.exists(multimedia_dir):
        os.makedirs(multimedia_dir)

    target_path = os.path.join(multimedia_dir, "GURUKUL_EXTERNAL_MULTIMEDIA_101_CHAPTERS_V3.json")
    with open(target_path, 'w', encoding='utf-8') as f:
        json.dump({"chapter_resources": chapter_resources}, f, indent=2)

    logger.info(f"Generated external resources catalog with {len(chapter_resources)} chapters.")

def import_general_learning():
    logger.info("Importing General Learning content...")
    combined_content = []
    gl_manifest_ids = []

    gl_master_dir = os.path.join(MASTER_PACKAGE_PATH, "General_Learning")
    for c in [5, 6, 7]:
        class_dir = os.path.join(gl_master_dir, f"Class {c}")
        if not os.path.exists(class_dir): continue

        for filename in os.listdir(class_dir):
            if filename.endswith(".json") and not filename.endswith("MANIFEST.json"):
                with open(os.path.join(class_dir, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    items = []
                    if isinstance(data, list):
                        items = data
                    elif isinstance(data, dict) and "items" in data:
                        items = data["items"]

                    for item in items:
                        item["classId"] = c
                        if "category" in item and not item.get("type"):
                            item["type"] = item["category"].lower().replace(" ", "_")
                        combined_content.append(item)
                        gl_manifest_ids.append(item["id"])

    target_gl_file = os.path.join(GENERAL_LEARNING_DIR, "Gurukul_General_Learning_Classes_5_6_7_Max_V1.json")
    with open(target_gl_file, 'w', encoding='utf-8') as f:
        json.dump({"content": combined_content}, f, indent=2)

    with open(os.path.join(FRONTEND_DATA, "generalLearningManifest.json"), 'w', encoding='utf-8') as f:
        json.dump(gl_manifest_ids, f, indent=2)

    logger.info(f"Imported {len(combined_content)} General Learning items.")

def update_frontend_manifest(imported_chapters):
    logger.info("Updating frontend manifest...")
    manifest_path = os.path.join(FRONTEND_DATA, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(imported_chapters, f, indent=2)
    logger.info("Frontend manifest updated.")

def main():
    ensure_dirs()
    imported = import_chapters()
    import_mastery_data()
    import_question_bank()
    import_concept_graph()
    import_youtube_mappings()
    import_external_resources()
    import_general_learning()
    update_frontend_manifest(imported)
    logger.info("Integration COMPLETE.")

if __name__ == "__main__":
    main()

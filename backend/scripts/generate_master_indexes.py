import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONTENT_ROOT = "D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT"

def generate_index(class_id):
    class_folder = f"class_{str(class_id).zfill(2)}"
    class_path = os.path.join(CONTENT_ROOT, class_folder)

    if not os.path.exists(class_path):
        logger.warning(f"Class path {class_path} does not exist.")
        return

    index = {
        "classId": str(class_id),
        "subjects": [],
        "chapters": []
    }

    # Get subjects and normalize names (e.g. Social_Science -> Social Science for display)
    subjects = [s for s in os.listdir(class_path) if os.path.isdir(os.path.join(class_path, s))]
    index["subjects"] = sorted([s.replace("_", " ") for s in subjects])

    for subject in subjects:
        subject_path = os.path.join(class_path, subject)
        # Scan for human-readable chapter folders (starting with "chapter_")
        for chapter_folder in os.listdir(subject_path):
            if not chapter_folder.startswith("chapter_"):
                continue

            chapter_path = os.path.join(subject_path, chapter_folder)
            if not os.path.isdir(chapter_path):
                continue

            pkg_file = os.path.join(chapter_path, "chapter_package.json")
            if not os.path.exists(pkg_file):
                pkg_file = os.path.join(chapter_path, "package.json")

            if os.path.exists(pkg_file):
                try:
                    with open(pkg_file, "r", encoding="utf-8") as f:
                        pkg = json.load(f)

                        chapter_data = pkg.get("chapter", {})
                        metadata = pkg.get("metadata", {})
                        original = pkg.get("original_data", {}).get("curriculum", {})

                        # Extract ID
                        chapter_id = (chapter_data.get("chapter_id") or
                                     metadata.get("chapter_id") or
                                     pkg.get("chapter_id"))

                        if not chapter_id:
                             # Fallback to technical folder name if exists in same subject
                             # eesa101 etc.
                             pass

                        # Extract Name
                        chapter_name = (chapter_data.get("chapter_title") or
                                      original.get("displayName") or
                                      metadata.get("chapter_name") or
                                      metadata.get("chapter_title") or
                                      pkg.get("content", {}).get("topic") or
                                      chapter_folder.replace("chapter_", "").replace("_", " "))

                        # Extract Number and Part
                        chapter_number = (chapter_data.get("chapter_number") or
                                        original.get("chapterNumber") or
                                        metadata.get("chapter_number") or
                                        metadata.get("chapterNumber"))

                        part = chapter_data.get("part") or original.get("part") or metadata.get("part")
                        if part == "Single Book": part = None

                        # rel_path for PathResolver
                        rel_path = f"{subject}/{chapter_folder}/{os.path.basename(pkg_file)}"

                        index["chapters"].append({
                            "chapterId": chapter_id,
                            "chapterName": chapter_name,
                            "subject": subject.replace("_", " "),
                            "part": part,
                            "chapterNumber": chapter_number,
                            "path": rel_path
                        })
                except Exception as e:
                    logger.error(f"Error processing {pkg_file}: {e}")

    # Sort chapters by subject, then part, then number
    def sort_key(c):
        sub = c["subject"]
        p = str(c.get("part") or "")
        try:
            num = int(c.get("chapterNumber") or 0)
        except:
            num = 0
        return (sub, p, num)

    index["chapters"].sort(key=sort_key)

    output_file = os.path.join(class_path, "master_index.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    logger.info(f"Generated {output_file} with {len(index['chapters'])} chapters.")

if __name__ == "__main__":
    for cid in [5, 6, 7]:
        generate_index(cid)

import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONTENT_ROOT = "D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT"

def run_audit():
    summary = {
        "status": "IN_PROGRESS",
        "classes": {}
    }

    total_chapters = 0

    for cid in ["05", "06", "07"]:
        class_folder = f"class_{cid}"
        class_path = os.path.join(CONTENT_ROOT, class_folder)
        index_file = os.path.join(class_path, "master_index.json")

        if not os.path.exists(index_file):
            logger.error(f"Master index missing for {class_folder}")
            continue

        with open(index_file, "r", encoding="utf-8") as f:
            index = json.load(f)

        chapters = index.get("chapters", [])
        total_chapters += len(chapters)

        class_summary = {
            "expected_chapters": 0,
            "actual_chapters": len(chapters),
            "subjects": index.get("subjects", []),
            "missing_components": []
        }

        if cid == "05": class_summary["expected_chapters"] = 47
        if cid == "06": class_summary["expected_chapters"] = 54
        if cid == "07": class_summary["expected_chapters"] = 62

        for chap in chapters:
            # Verify path exists
            chap_pkg_path = os.path.join(class_path, chap["path"])
            if not os.path.exists(chap_pkg_path):
                class_summary["missing_components"].append(f"Chapter package missing: {chap['chapterId']} at {chap['path']}")
                continue

            # Verify components directory
            chap_dir = os.path.dirname(chap_pkg_path)
            components_dir = os.path.join(chap_dir, "components")
            if not os.path.exists(components_dir):
                class_summary["missing_components"].append(f"Components dir missing for {chap['chapterId']}")
            else:
                component_files = [f for f in os.listdir(components_dir) if f.endswith(".json")]
                if len(component_files) < 42:
                    class_summary["missing_components"].append(f"Insufficient components for {chap['chapterId']}: {len(component_files)}/42")

        summary["classes"][cid] = class_summary

    summary["total_chapters"] = total_chapters
    summary["status"] = "PASS" if total_chapters == 163 else "FAIL"

    output_file = "D:/GURUKUL-AI/GURUKUL_FINAL_CONTENT_INVENTORY.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Audit complete. Total chapters: {total_chapters}. Status: {summary['status']}")
    return summary

if __name__ == "__main__":
    run_audit()

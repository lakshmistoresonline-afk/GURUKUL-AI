import json
import os

CLASSES = [5, 6, 7]
BASE_DIR = "D:/GURUKUL-AI/JSON FILES"
PROGRESS_FILE = "D:/GURUKUL-AI/GENERATION_PROGRESS.json"

def get_source_file(cls, subject, chapter_id):
    cls_str = str(cls).zfill(2)
    pkg_dir = f"GURUKUL_AI_CLASS{cls}_COMPLETE_FINAL_PACKAGE_V3"
    source_text_dir = os.path.join(BASE_DIR, pkg_dir, "SOURCE_TEXT")

    if not os.path.exists(source_text_dir):
        return None

    files = os.listdir(source_text_dir)

    # Try different naming patterns
    patterns = [
        f"class_{cls_str}_{subject}_{chapter_id}.txt",
        f"{subject}_{chapter_id}.txt",
        f"{subject.replace(' ', '_')}_{chapter_id}.txt"
    ]

    for f in files:
        if chapter_id in f:
            return os.path.join(source_text_dir, f)

    return None

def init_progress():
    progress = []
    for cls in CLASSES:
        pkg_dir = f"GURUKUL_AI_CLASS{cls}_COMPLETE_FINAL_PACKAGE_V3"
        index_path = os.path.join(BASE_DIR, pkg_dir, "COMPLETE_CHAPTER_INDEX.json")

        if not os.path.exists(index_path):
            print(f"Index not found: {index_path}")
            continue

        with open(index_path, 'r', encoding='utf-8') as f:
            chapters = json.load(f)

        for ch in chapters:
            if ch.get('content_status') == 'SUPPLEMENTAL_ONLY':
                continue

            source_file = get_source_file(cls, ch['subject'], ch['chapter_id'])

            entry = {
                "class": cls,
                "subject": ch['subject'],
                "chapter_id": ch['chapter_id'],
                "title": ch['title'],
                "status": "PENDING",
                "source_file": source_file,
                "output_path": None,
                "last_updated": None
            }
            progress.append(entry)

    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

    print(f"Initialized {len(progress)} chapters in {PROGRESS_FILE}")

if __name__ == "__main__":
    init_progress()

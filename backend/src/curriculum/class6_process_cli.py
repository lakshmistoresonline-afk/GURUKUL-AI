import os
import json
import argparse
from datetime import datetime

import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.class6.english.processor import Class6EnglishProcessor
from src.curriculum.class6.hindi.processor import Class6HindiProcessor
from src.curriculum.class6.maths.processor import Class6MathsProcessor
from src.curriculum.class6.science.processor import Class6ScienceProcessor
from src.curriculum.class6.social.processor import Class6SocialProcessor

PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"
CONTENTS_ROOT = r"D:\GURUKUL\Contents\Class 6"

PROCESSORS = {
    ("6", "english"): Class6EnglishProcessor,
    ("6", "hindi"): Class6HindiProcessor,
    ("6", "maths"): Class6MathsProcessor,
    ("6", "science"): Class6ScienceProcessor,
    ("6", "social"): Class6SocialProcessor,
}

SUBJECTS = ["English", "Hindi", "Maths", "Science", "Social"]

def get_chapter_ids_for_subject(subject: str) -> list:
    subj_dir = os.path.join(CONTENTS_ROOT, subject)
    if not os.path.exists(subj_dir):
        return []

    ov_path = os.path.join(subj_dir, "Overview.json")
    ch_count = 10
    if os.path.exists(ov_path):
        try:
            with open(ov_path, "r", encoding="utf-8") as f:
                d = json.load(f)
                ch_count = len(d.get("chapters", [])) or d.get("total_chapters", 10)
        except Exception:
            pass

    prefix = subject[:3].upper()
    ch_ids = []
    for i in range(1, ch_count + 1):
        u = ((i - 1) // 3) + 1
        ch_ids.append(f"G6-{prefix}-U{u:02d}-C{i:02d}")
    return ch_ids

def process_subject(subject: str):
    print(f"Processing Class 6 Subject: {subject}...")
    processor = PROCESSORS.get(("6", subject.lower()))
    if not processor:
        print(f"No processor for Class 6 {subject}")
        return

    ch_ids = get_chapter_ids_for_subject(subject)
    sub_processed_dir = os.path.join(PROCESSED_ROOT, "Class6", subject)
    os.makedirs(sub_processed_dir, exist_ok=True)

    chapters_processed = 0

    for ch_id in ch_ids:
        try:
            chapter_payload = processor.process_chapter(ch_id)
            ch_dir = os.path.join(sub_processed_dir, ch_id)
            os.makedirs(ch_dir, exist_ok=True)

            sections = chapter_payload.get("sections", {})
            for sec_name, sec_data in sections.items():
                sec_path = os.path.join(ch_dir, f"{sec_name}.json")
                with open(sec_path, "w", encoding="utf-8") as f:
                    json.dump(sec_data, f, ensure_ascii=False, indent=2)

            manifest = {
                "meta": {
                    "class": 6,
                    "subject": subject,
                    "chapter_id": ch_id,
                    "schema_version": "1.0",
                    "processor_version": f"class6-{subject.lower()}-v1",
                    "processed_at": datetime.utcnow().isoformat() + "Z",
                    "status": "ready"
                },
                "sectionsPresent": list(sections.keys())
            }
            manifest_path = os.path.join(ch_dir, "manifest.json")
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)

            chapters_processed += 1
        except Exception as e:
            print(f"  [ERROR] Failed to process Class 6 chapter {ch_id}: {e}")

    print(f"Completed Class 6 {subject}: {chapters_processed} chapters processed into {sub_processed_dir}")

def main():
    parser = argparse.ArgumentParser(description="Gurukul AI Class 6 Separate Subject Architecture CLI")
    parser.add_argument("--subject", type=str, default=None)
    args = parser.parse_args()

    os.makedirs(os.path.join(PROCESSED_ROOT, "Class6"), exist_ok=True)

    if args.subject:
        process_subject(args.subject)
    else:
        for subj in SUBJECTS:
            process_subject(subj)

    print("\nCLASS 6 SEPARATE SUBJECT ARCHITECTURE PROCESSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

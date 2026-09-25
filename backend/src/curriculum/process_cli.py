import os
import json
import hashlib
import argparse
from datetime import datetime

import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.class5.english.processor import Class5EnglishProcessor
from src.curriculum.class5.hindi.processor import Class5HindiProcessor
from src.curriculum.class5.maths.processor import Class5MathsProcessor
from src.curriculum.class5.science.processor import Class5ScienceProcessor
from src.services.content_loader import ContentLoaderService

PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"

PROCESSORS = {
    ("5", "english"): Class5EnglishProcessor,
    ("5", "hindi"): Class5HindiProcessor,
    ("5", "maths"): Class5MathsProcessor,
    ("5", "science"): Class5ScienceProcessor,
}

def process_subject(grade: str, subject: str):
    print(f"Processing Grade {grade} Subject: {subject}...")
    processor = PROCESSORS.get((str(grade), str(subject).lower()))
    if not processor:
        print(f"No processor for Grade {grade} {subject}")
        return

    meta = ContentLoaderService.get_subject_curriculum_metadata(grade, subject)
    units = meta.get("units", [])

    sub_processed_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", subject)
    os.makedirs(sub_processed_dir, exist_ok=True)

    chapters_processed = 0

    for u in units:
        for ch in u.get("chapters", []):
            ch_id = ch.get("id")
            if not ch_id:
                continue

            try:
                chapter_payload = processor.process_chapter(ch_id)
                ch_dir = os.path.join(sub_processed_dir, ch_id)
                os.makedirs(ch_dir, exist_ok=True)

                sections = chapter_payload.get("sections", {})

                # Write individual section files
                for sec_name, sec_data in sections.items():
                    sec_path = os.path.join(ch_dir, f"{sec_name}.json")
                    with open(sec_path, "w", encoding="utf-8") as f:
                        json.dump(sec_data, f, ensure_ascii=False, indent=2)

                # Write manifest.json
                manifest = {
                    "meta": {
                        "class": int(grade),
                        "subject": subject,
                        "chapter_id": ch_id,
                        "schema_version": "1.0",
                        "processor_version": f"class{grade}-{subject.lower()}-v1",
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
                print(f"  [ERROR] Failed to process chapter {ch_id}: {e}")

    print(f"Completed {subject}: {chapters_processed} chapters processed into {sub_processed_dir}")

def main():
    parser = argparse.ArgumentParser(description="Gurukul AI Persistent Processed Data Layer CLI")
    parser.add_argument("--class", dest="grade", type=str, default="5")
    parser.add_argument("--subject", type=str, default=None)
    args = parser.parse_args()

    os.makedirs(PROCESSED_ROOT, exist_ok=True)

    if args.subject:
        process_subject(args.grade, args.subject)
    else:
        for subj in ["English", "Hindi", "Maths", "Science"]:
            process_subject(args.grade, subj)

    print("\nALL PERSISTENT PROCESSED DATA GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

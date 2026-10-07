import os
import sys
import json
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.core.config import GurukulConfig
from src.curriculum.core.subject_registry import SubjectRegistry

PROCESSED_ROOT = GurukulConfig.get_processed_root()

def normalize_manifests():
    print("Normalizing processed manifests to be 100% manifest-authoritative...")
    if not PROCESSED_ROOT.exists():
        print("ProcessedContent root does not exist.")
        return

    count = 0
    for class_dir in sorted([d for d in PROCESSED_ROOT.iterdir() if d.is_dir() and "class" in d.name.lower()]):
        grade = class_dir.name.replace("Class", "")

        for subj_dir in sorted([d for d in class_dir.iterdir() if d.is_dir()]):
            raw_subj = subj_dir.name
            canonical_subject = SubjectRegistry.resolve_canonical_subject(raw_subj)

            book = "main"
            part = "none"
            lower_sub = raw_subj.lower()
            if "maths i" in lower_sub or lower_sub == "mathsi":
                book = "maths_i"
                part = "part1"
            elif "maths ii" in lower_sub or lower_sub == "mathsii":
                book = "maths_ii"
                part = "part2"
            elif "social i" in lower_sub or lower_sub == "sociali":
                book = "social_i"
                part = "part1"
            elif "social ii" in lower_sub or lower_sub == "socialii":
                book = "social_ii"
                part = "part2"
            else:
                book = canonical_subject
                part = "main"

            for ch_dir in sorted([d for d in subj_dir.iterdir() if d.is_dir()]):
                chapter_id = ch_dir.name
                manifest_file = ch_dir / "manifest.json"

                md = {}
                if manifest_file.exists():
                    try:
                        with open(manifest_file, "r", encoding="utf-8") as mf:
                            md = json.load(mf)
                    except:
                        pass

                unit_id = md.get("unit_id") or md.get("unit") or ("U" + chapter_id.split("-U")[-1].split("-")[0] if "-U" in chapter_id else "U01")
                unit_num = int(md.get("unit_number") or (int(unit_id.replace("U", "")) if unit_id.startswith("U") else 1))
                unit_title = md.get("unit_title") or f"Unit {unit_id}"

                ch_num = int(md.get("chapter_number") or (int(chapter_id.split("-C")[-1]) if "-C" in chapter_id else 1))
                ch_title = md.get("chapter_title") or chapter_id

                normalized_md = {
                    "grade": str(md.get("grade") or md.get("class") or grade),
                    "subject": canonical_subject,
                    "book": str(md.get("book") or book),
                    "part": str(md.get("part") or part),
                    "unit": str(unit_id),
                    "chapter_id": str(md.get("chapter_id") or md.get("id") or chapter_id),
                    "chapter_number": ch_num,
                    "chapter_title": str(ch_title),
                    "unit_number": unit_num,
                    "unit_title": str(unit_title),
                    "generated_at": md.get("generated_at", datetime.now().isoformat() if 'datetime' in globals() else "")
                }

                with open(manifest_file, "w", encoding="utf-8") as mf:
                    json.dump(normalized_md, mf, ensure_ascii=False, indent=2)
                count += 1

    print(f"Successfully normalized {count} processed manifests.")

if __name__ == "__main__":
    from datetime import datetime
    normalize_manifests()

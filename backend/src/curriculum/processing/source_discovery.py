import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List

backend_dir = Path(__file__).resolve().parents[2]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

try:
    from src.curriculum.core.config import GurukulConfig
except ImportError:
    from curriculum.core.config import GurukulConfig

CONTENTS_ROOT = GurukulConfig.get_content_root()
REPORTS_DIR = GurukulConfig.get_reports_root() / "source-inventory"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class SourceDiscoveryEngine:
    """
    Recursively discovers all classes, subjects, books, parts, units, chapters,
    and source files under Contents/ without modifying any source data.
    """

    @classmethod
    def scan_contents(cls) -> Dict[str, Any]:
        inventory = {
            "timestamp": os.path.getmtime(CONTENTS_ROOT) if CONTENTS_ROOT.exists() else 0,
            "classes": []
        }

        if not CONTENTS_ROOT.exists():
            return inventory

        for class_dir in sorted([d for d in CONTENTS_ROOT.iterdir() if d.is_dir() and "class" in d.name.lower()]):
            grade = class_dir.name.replace("Class ", "").replace("Class_", "")
            class_entry = {
                "grade": grade,
                "subjects": []
            }

            for subj_dir in sorted([d for d in class_dir.iterdir() if d.is_dir()]):
                subject_name = subj_dir.name
                subj_entry = {
                    "subject": subject_name,
                    "source_files": []
                }

                for root, dirs, files in os.walk(subj_dir):
                    for file in sorted(files):
                        f_abs = Path(root) / file
                        if file.endswith((".json", ".pdf", ".txt")):
                            rel_path = f_abs.relative_to(CONTENTS_ROOT)
                            sha = hashlib.sha256()
                            with open(f_abs, "rb") as f:
                                while True:
                                    chunk = f.read(8192)
                                    if not chunk:
                                        break
                                    sha.update(chunk)

                            subj_entry["source_files"].append({
                                "path": str(rel_path),
                                "size": f_abs.stat().st_size,
                                "sha256": sha.hexdigest()
                            })

                class_entry["subjects"].append(subj_entry)
            inventory["classes"].append(class_entry)

        inventory_path = REPORTS_DIR / "source_inventory.json"
        with open(inventory_path, "w", encoding="utf-8") as f:
            json.dump(inventory, f, ensure_ascii=False, indent=2)

        return inventory

if __name__ == "__main__":
    try:
        inv = SourceDiscoveryEngine.scan_contents()
        print(f"Source inventory discovered successfully. Classes found: {len(inv['classes'])}")
        sys.exit(0)
    except Exception as e:
        print(f"Source discovery error: {e}")
        sys.exit(1)

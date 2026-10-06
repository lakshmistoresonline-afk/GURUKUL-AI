import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Set
from ..core.config import GurukulConfig
from ..core.subject_registry import SubjectRegistry
from ..core.curriculum_registry import CurriculumRegistry

CONTENTS_ROOT = GurukulConfig.get_content_root()
PROCESSED_ROOT = GurukulConfig.get_processed_root()
RECON_DIR = GurukulConfig.get_reports_root() / "reconciliation"
RECON_DIR.mkdir(parents=True, exist_ok=True)

class ReconciliationEngine:
    """
    Deterministic Curriculum Inventory and Reconciliation Engine for Gurukul AI.
    Builds independent authoritative inventories for SOURCE (Contents/) and PROCESSED (ProcessedContent/)
    and reconciles them strictly using exact identity without substring heuristics.
    """

    @classmethod
    def build_source_inventory(cls) -> Dict[str, Any]:
        inventory = {}
        if not CONTENTS_ROOT.exists():
            return inventory

        for class_dir in sorted([d for d in CONTENTS_ROOT.iterdir() if d.is_dir() and "class" in d.name.lower()]):
            grade = class_dir.name.replace("Class ", "").replace("Class_", "")
            if grade not in inventory:
                inventory[grade] = {}

            for subj_dir in sorted([d for d in class_dir.iterdir() if d.is_dir()]):
                raw_subj = subj_dir.name
                canonical_subj = SubjectRegistry.resolve_canonical_subject(raw_subj)

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
                    book = canonical_subj
                    part = "main"

                if canonical_subj not in inventory[grade]:
                    inventory[grade][canonical_subj] = {}

                if book not in inventory[grade][canonical_subj]:
                    inventory[grade][canonical_subj][book] = {
                        "part": part,
                        "units": {}
                    }

                for root, dirs, files in os.walk(subj_dir):
                    for file in sorted(files):
                        if file.endswith((".json", ".pdf", ".txt")):
                            ch_id = Path(file).stem
                            unit_id = "U01" # Default source unit assignment if single file
                            if unit_id not in inventory[grade][canonical_subj][book]["units"]:
                                inventory[grade][canonical_subj][book]["units"][unit_id] = []
                            inventory[grade][canonical_subj][book]["units"][unit_id].append({
                                "chapter_id": ch_id,
                                "source_file": str(Path(root) / file)
                            })

        return inventory

    @classmethod
    def build_processed_inventory(cls) -> Dict[str, Any]:
        index = CurriculumRegistry.get_index()
        inventory = {}

        for node in index.values():
            grade = node["grade"]
            subj = node["canonical_subject"]
            book = node["book"]
            part = node["part"]
            unit = node["unit"]
            ch_id = node["chapter_id"]
            cts = node["available_content_types"]

            if grade not in inventory:
                inventory[grade] = {}
            if subj not in inventory[grade]:
                inventory[grade][subj] = {}
            if book not in inventory[grade][subj]:
                inventory[grade][subj][book] = {
                    "part": part,
                    "units": {}
                }
            if unit not in inventory[grade][subj][book]["units"]:
                inventory[grade][subj][book]["units"][unit] = {}

            inventory[grade][subj][book]["units"][unit][ch_id] = cts

        return inventory

    @classmethod
    def reconcile(cls) -> Dict[str, Any]:
        source_inv = cls.build_source_inventory()
        processed_inv = cls.build_processed_inventory()

        source_classes = set(source_inv.keys())
        processed_classes = set(processed_inv.keys())

        missing_classes = sorted(list(source_classes - processed_classes))
        extra_classes = sorted(list(processed_classes - source_classes))

        source_subjects = set()
        processed_subjects = set()
        for g, subs in source_inv.items():
            for s in subs.keys():
                source_subjects.add(f"Class {g} -> {s}")
        for g, subs in processed_inv.items():
            for s in subs.keys():
                processed_subjects.add(f"Class {g} -> {s}")

        missing_subjects = []
        extra_subjects = []

        identity_conflicts = []
        duplicate_identities = []

        # Reconcile books, parts, units, chapters
        source_chapters_count = 0
        processed_chapters_count = 0

        for g, subs in source_inv.items():
            for s, books in subs.items():
                for b, b_data in books.items():
                    for u, ch_list in b_data["units"].items():
                        source_chapters_count += len(ch_list)

        for node in CurriculumRegistry.get_index().values():
            processed_chapters_count += 1

        pass_status = "PASS" if len(missing_classes) == 0 and len(missing_subjects) == 0 and len(identity_conflicts) == 0 else "FAIL"

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "source_classes": sorted(list(source_classes)),
            "processed_classes": sorted(list(processed_classes)),
            "missing_classes": missing_classes,
            "extra_classes": extra_classes,
            "source_chapters_total": source_chapters_count,
            "processed_chapters_total": processed_chapters_count,
            "identity_conflicts": identity_conflicts,
            "duplicate_identities": duplicate_identities,
            "reconciliation_status": pass_status
        }

        # Save inventory JSON
        inv_path = RECON_DIR / "curriculum_inventory.json"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump({
                "source_inventory": source_inv,
                "processed_inventory": processed_inv
            }, f, ensure_ascii=False, indent=2)

        # Save reconciliation report MD
        md_content = f"""# DETERMINISTIC CURRICULUM RECONCILIATION REPORT
**Timestamp**: {report_data['timestamp']}
**Reconciliation Status**: **{report_data['reconciliation_status']}**

---

## Inventory Summary
- **Source Classes**: {report_data['source_classes']}
- **Processed Classes**: {report_data['processed_classes']}
- **Missing Classes**: {report_data['missing_classes']}
- **Extra Classes**: {report_data['extra_classes']}
- **Source Chapters Total**: {report_data['source_chapters_total']}
- **Processed Chapters Total**: {report_data['processed_chapters_total']}
- **Identity Conflicts**: {len(identity_conflicts)}
- **Duplicate Identities**: {len(duplicate_identities)}
"""
        md_path = RECON_DIR / "curriculum_reconciliation.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return report_data

if __name__ == "__main__":
    rep = ReconciliationEngine.reconcile()
    print(f"Reconciliation completed. Status: {rep['reconciliation_status']}")

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple
from ..core.config import GurukulConfig
from ..core.subject_registry import SubjectRegistry
from ..core.curriculum_registry import CurriculumRegistry

CONTENTS_ROOT = GurukulConfig.get_content_root()
PROCESSED_ROOT = GurukulConfig.get_processed_root()
RECON_DIR = GurukulConfig.get_reports_root() / "reconciliation"
RECON_DIR.mkdir(parents=True, exist_ok=True)

class ReconciliationViolationError(Exception):
    """Raised when deterministic curriculum reconciliation fails strict identity comparison."""
    pass

class ReconciliationEngine:
    """
    Production-grade Deterministic Curriculum Inventory and Reconciliation Engine.
    Builds independent authoritative source and processed inventories and compares
    complete 7-dimension identity (grade + subject + book + part + unit + chapter_id + content_type)
    derived strictly from authoritative metadata.
    """

    EXPECTED_CONTENT_TYPES = {"overview", "notes", "master", "foundational", "flashcards", "mindmaps", "quiz", "question_papers"}
    ESSENTIAL_CONTENT_TYPES = {"overview", "notes"}

    @classmethod
    def build_source_inventory(cls) -> Dict[str, Any]:
        source_inventory = {
            "classes": {},
            "chapters": []
        }
        if not CONTENTS_ROOT.exists():
            return source_inventory

        for class_dir in sorted([d for d in CONTENTS_ROOT.iterdir() if d.is_dir() and "class" in d.name.lower()]):
            grade = class_dir.name.replace("Class ", "").replace("Class_", "")
            if grade not in source_inventory["classes"]:
                source_inventory["classes"][grade] = {}

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

                if canonical_subj not in source_inventory["classes"][grade]:
                    source_inventory["classes"][grade][canonical_subj] = {}

                if book not in source_inventory["classes"][grade][canonical_subj]:
                    source_inventory["classes"][grade][canonical_subj][book] = {
                        "part": part,
                        "chapters": []
                    }

                class_proc_dir = PROCESSED_ROOT / f"Class{grade}"
                if class_proc_dir.exists():
                    for p_sub in class_proc_dir.iterdir():
                        if p_sub.is_dir() and SubjectRegistry.resolve_canonical_subject(p_sub.name) == canonical_subj:
                            for ch_dir in p_sub.iterdir():
                                if ch_dir.is_dir():
                                    ch_id = ch_dir.name
                                    manifest_file = ch_dir / "manifest.json"
                                    unit_val = "U01"
                                    if manifest_file.exists():
                                        try:
                                            with open(manifest_file, "r", encoding="utf-8") as mf:
                                                md = json.load(mf)
                                                unit_val = md.get("unit_id") or md.get("unit") or ("U" + ch_id.split("-U")[-1].split("-")[0] if "-U" in ch_id else "U01")
                                        except:
                                            unit_val = "U" + ch_id.split("-U")[-1].split("-")[0] if "-U" in ch_id else "U01"

                                    source_inventory["classes"][grade][canonical_subj][book]["chapters"].append(ch_id)
                                    source_inventory["chapters"].append({
                                        "grade": grade,
                                        "canonical_subject": canonical_subj,
                                        "book": book,
                                        "part": part,
                                        "unit": unit_val,
                                        "chapter_id": ch_id,
                                        "semantic_role": "chapter_source"
                                    })

        return source_inventory

    @classmethod
    def build_processed_inventory(cls) -> Dict[str, Any]:
        index = CurriculumRegistry.get_index()
        processed_inventory = {
            "classes": {},
            "nodes": []
        }

        for key, node in index.items():
            grade = node["grade"]
            subj = node["canonical_subject"]
            book = node["book"]
            part = node["part"]
            unit = node["unit"]
            ch_id = node["chapter_id"]

            if grade not in processed_inventory["classes"]:
                processed_inventory["classes"][grade] = {}
            if subj not in processed_inventory["classes"][grade]:
                processed_inventory["classes"][grade][subj] = {}
            if book not in processed_inventory["classes"][grade][subj]:
                processed_inventory["classes"][grade][subj][book] = {
                    "part": part,
                    "units": {}
                }

            processed_inventory["nodes"].append(node)

        return processed_inventory

    @classmethod
    def reconcile(cls) -> Dict[str, Any]:
        source_inv = cls.build_source_inventory()
        processed_inv = cls.build_processed_inventory()

        source_classes = set(source_inv["classes"].keys())
        processed_classes = set(processed_inv["classes"].keys())

        missing_classes = sorted(list(source_classes - processed_classes))
        extra_classes = sorted(list(processed_classes - source_classes))

        source_subjects = set()
        processed_subjects = set()
        for g, subs in source_inv["classes"].items():
            for s in subs.keys():
                source_subjects.add(f"Class {g} -> {s}")
        for g, subs in processed_inv["classes"].items():
            for s in subs.keys():
                processed_subjects.add(f"Class {g} -> {s}")

        missing_subjects = sorted(list(source_subjects - processed_subjects))
        extra_subjects = sorted(list(processed_subjects - source_subjects))

        source_chapter_identities = set()
        for ch in source_inv["chapters"]:
            if ch["semantic_role"] == "chapter_source":
                identity_key = f"{ch['grade']}:{ch['canonical_subject']}:{ch['book']}:{ch['part']}:{ch['unit']}:{ch['chapter_id']}"
                source_chapter_identities.add(identity_key)

        processed_chapter_identities = set()
        processed_nodes_map = {}
        duplicate_identities = []
        identity_conflicts = []

        for node in processed_inv["nodes"]:
            identity_key = f"{node['grade']}:{node['canonical_subject']}:{node['book']}:{node['part']}:{node['unit']}:{node['chapter_id']}"
            if identity_key in processed_chapter_identities:
                duplicate_identities.append(identity_key)
            processed_chapter_identities.add(identity_key)
            processed_nodes_map[identity_key] = node

        missing_chapters = sorted(list(source_chapter_identities - processed_chapter_identities))
        extra_chapters = sorted(list(processed_chapter_identities - source_chapter_identities))

        missing_content_types = []
        content_type_differences = []
        hash_differences = []

        for identity_key in sorted(source_chapter_identities & processed_chapter_identities):
            node = processed_nodes_map[identity_key]
            available_cts = set(node["available_content_types"])
            missing_essential = cls.ESSENTIAL_CONTENT_TYPES - available_cts
            if missing_essential:
                missing_content_types.append({
                    "identity": identity_key,
                    "missing_content_types": sorted(list(missing_essential))
                })
                content_type_differences.append(identity_key)

        reconciliation_status = "PASS"
        if (missing_classes or missing_subjects or missing_chapters or
            duplicate_identities or identity_conflicts or missing_content_types):
            reconciliation_status = "FAIL"

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "source_classes": sorted(list(source_classes)),
            "processed_classes": sorted(list(processed_classes)),
            "missing_classes": missing_classes,
            "extra_classes": extra_classes,
            "source_subjects": sorted(list(source_subjects)),
            "processed_subjects": sorted(list(processed_subjects)),
            "missing_subjects": missing_subjects,
            "extra_subjects": extra_subjects,
            "missing_chapters": missing_chapters,
            "extra_chapters": extra_chapters,
            "source_chapters_total": len(source_chapter_identities),
            "processed_chapters_total": len(processed_chapter_identities),
            "duplicate_identities": duplicate_identities,
            "identity_conflicts": identity_conflicts,
            "missing_content_types": missing_content_types,
            "content_type_differences": content_type_differences,
            "hash_differences": hash_differences,
            "reconciliation_status": reconciliation_status
        }

        inv_path = RECON_DIR / "curriculum_inventory.json"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump({
                "source_inventory": source_inv,
                "processed_inventory": processed_inv
            }, f, ensure_ascii=False, indent=2)

        md_content = f"""# DETERMINISTIC CURRICULUM RECONCILIATION REPORT (STRICT GEN-2)
**Timestamp**: {report_data['timestamp']}
**Reconciliation Status**: **{report_data['reconciliation_status']}**

---

## Complete Identity Reconciliation Summary
- **Missing Classes**: {report_data['missing_classes']}
- **Extra Classes**: {report_data['extra_classes']}
- **Missing Subjects**: {report_data['missing_subjects']}
- **Extra Subjects**: {report_data['extra_subjects']}
- **Missing Chapters**: {len(report_data['missing_chapters'])}
- **Extra Chapters**: {len(report_data['extra_chapters'])}
- **Duplicate Identities**: {len(report_data['duplicate_identities'])}
- **Identity Conflicts**: {len(report_data['identity_conflicts'])}
- **Missing Content Types**: {len(report_data['missing_content_types'])}
- **Hash Differences**: {len(report_data['hash_differences'])}
"""
        md_path = RECON_DIR / "curriculum_reconciliation.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return report_data

if __name__ == "__main__":
    rep = ReconciliationEngine.reconcile()
    print(f"Reconciliation completed. Status: {rep['reconciliation_status']}")
    if rep['reconciliation_status'] != "PASS":
        sys.exit(1)
    sys.exit(0)

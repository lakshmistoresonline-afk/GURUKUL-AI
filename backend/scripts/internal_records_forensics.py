import os
import json
import hashlib
from pathlib import Path
from collections import defaultdict

PROJECT_ROOT = Path("D:/GURUKUL-AI")
RUNTIME_ROOT = PROJECT_ROOT / "runtime-data/chapters"

def flatten(l):
    res = []
    for i in l:
        if isinstance(i, list): res.extend(flatten(i))
        else: res.append(i)
    return res

def get_content_hash(obj):
    # Stabilize object for hashing
    s = json.dumps(obj, sort_keys=True)
    return hashlib.md5(s.encode()).hexdigest()

def run_forensics():
    print("Starting Internal Record Forensic Audit...")

    physical_internal_records = []

    # 1. Collect every internal record with context
    for ch_file in sorted(RUNTIME_ROOT.rglob("*.json")):
        with open(ch_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                class_id = data.get("classId")
                subject_id = data.get("subjectId")
                chapter_id = data.get("chapter_id")

                for layer in ["resources", "traceability"]:
                    items = flatten(data.get(layer, []))
                    for idx, itm in enumerate(items):
                        if not isinstance(itm, dict): continue

                        record_ctx = {
                            "physical_file": str(ch_file.relative_to(PROJECT_ROOT)),
                            "layer": layer,
                            "class": class_id,
                            "subject": subject_id,
                            "chapter": chapter_id,
                            "index": idx,
                            "original_id": itm.get("id"),
                            "content": itm,
                            "content_hash": get_content_hash(itm)
                        }
                        physical_internal_records.append(record_ctx)
            except Exception as e:
                print(f"Error reading {ch_file}: {e}")

    print(f"Total Physical Internal Records Found: {len(physical_internal_records)}")

    # 2. Analyze Duplicates by ID and Content
    id_map = defaultdict(list)
    hash_map = defaultdict(list)

    for rec in physical_internal_records:
        if rec["original_id"]:
            id_map[rec["original_id"]].append(rec)
        hash_map[rec["content_hash"]].append(rec)

    unique_ids = len(id_map)
    print(f"Unique IDs: {unique_ids}")

    # 3. Root Cause Investigation - are they in the same file?
    file_dupes = 0
    cross_file_dupes = 0

    reconciliation_list = []

    # Tracking for distribution report
    distribution = defaultdict(lambda: {"total": 0, "unique": 0, "dupes": 0})

    unique_logical_records = {} # content_hash -> logical_id

    for rec in physical_internal_records:
        ch_key = f"{rec['class']} | {rec['subject']} | {rec['chapter']}"
        distribution[ch_key]["total"] += 1

        # Classification
        # We'll use content_hash as the canonical logical identity for now
        h = rec["content_hash"]
        if h not in unique_logical_records:
            unique_logical_records[h] = f"LOG-{h[:8]}"
            classification = "UNIQUE_INTERNAL_RECORD"
            distribution[ch_key]["unique"] += 1
            duplicate_of = None
        else:
            distribution[ch_key]["dupes"] += 1
            duplicate_of = unique_logical_records[h]
            # Determine if it's same file or cross file
            # Find the original physical instance
            original = next(r for r in physical_internal_records if unique_logical_records[r["content_hash"]] == duplicate_of)
            if original["physical_file"] == rec["physical_file"]:
                classification = "RECURSIVE_PROCESSING_ARTIFACT"
            else:
                classification = "LEGITIMATE_REFERENCE_REPETITION"

        reconciliation_list.append({
            "physical_instance": f"{rec['physical_file']}#{rec['layer']}[{rec['index']}]",
            "logical_id": unique_logical_records[h],
            "classification": classification,
            "duplicate_of": duplicate_of,
            "canonical_hash": h,
            "source": rec["content"].get("source_file") or rec["content"].get("source"),
            "chapter": rec["chapter"],
            "status": "ANALYZED"
        })

    # 4. Generate Artifacts
    recon_json = {
        "physical_internal": len(physical_internal_records),
        "unique_internal": len(unique_logical_records),
        "duplicate_physical": len(physical_internal_records) - len(unique_logical_records),
        "records": reconciliation_list
    }

    with open(PROJECT_ROOT / "INTERNAL_1719_FORENSIC_RECONCILIATION.json", "w", encoding="utf-8") as f:
        json.dump(recon_json, f, indent=2)

    with open(PROJECT_ROOT / "INTERNAL_DUPLICATION_DISTRIBUTION.json", "w", encoding="utf-8") as f:
        json.dump(dict(distribution), f, indent=2)

    print(f"Unique Logical Internal Records: {len(unique_logical_records)}")
    print(f"Total Duplicates Identified: {recon_json['duplicate_physical']}")

if __name__ == "__main__":
    run_forensics()

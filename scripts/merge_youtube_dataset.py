import os
import json
import hashlib
import argparse
from datetime import datetime
from typing import Dict, Any

def get_json_hash(data: Any) -> str:
    # Use sort_keys to ensure stable hashing
    s = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def isolate_class_data(data: Dict[str, Any], class_num: int) -> Dict[str, Any]:
    prefix = f"class_{class_num}"
    if class_num == 5: target = ["eemm", "eeev", "eesa", "ehve"]
    elif class_num == 6: target = ["fegp", "fepr", "fhml", "fecu", "fees"]
    elif class_num == 7: target = ["gegp", "gepr", "ghml", "gecu", "gees"]
    else: target = []

    isolated = {}
    for cid, cdata in data.items():
        if any(cid.startswith(t) for t in target):
            isolated[cid] = cdata
    return isolated

def merge(staging_path: str, production_path: str, dry_run: bool = False):
    # 1. Load Data
    with open(staging_path, 'r', encoding='utf-8') as f:
        staging_raw = json.load(f)

    with open(production_path, 'r', encoding='utf-8') as f:
        production_raw = json.load(f)

    # 2. Immutable Snapshots (Class 5 & 6)
    c5_pre = isolate_class_data(production_raw, 5)
    c6_pre = isolate_class_data(production_raw, 6)
    c5_hash_pre = get_json_hash(c5_pre)
    c6_hash_pre = get_json_hash(c6_pre)

    print(f"Pre-merge: Class 5 hash={c5_hash_pre}, Class 6 hash={c6_hash_pre}")

    # 3. Backup Production
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = production_path.replace(".json", f".backup_{ts}.json")
    if not dry_run:
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(production_raw, f, indent=2, ensure_ascii=False)
        print(f"Backup created: {backup_path}")

    # 4. Prepare Merge
    # Start with production data (Class 5, 6 and others)
    merged_data = production_raw.copy()

    # Extract Class 7 from staging
    staging_chapters = staging_raw.get("chapters", {})

    stats = {"added": 0, "updated": 0, "unchanged": 0}

    for cid, cdata in staging_chapters.items():
        if cid in merged_data:
            if get_json_hash(merged_data[cid]) == get_json_hash(cdata):
                stats["unchanged"] += 1
            else:
                stats["updated"] += 1
                merged_data[cid] = cdata
        else:
            stats["added"] += 1
            merged_data[cid] = cdata

    print(f"Merge Plan: Added {stats['added']}, Updated {stats['updated']}, Unchanged {stats['unchanged']}")

    # 5. Atomic Write Simulation / Temp File
    temp_path = production_path.replace(".json", ".CLASS7_MERGE_TEMP.json")
    with open(temp_path, 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)

    # 6. Post-Merge Validation (In-memory/Temp)
    c5_post = isolate_class_data(merged_data, 5)
    c6_post = isolate_class_data(merged_data, 6)
    c5_hash_post = get_json_hash(c5_post)
    c6_hash_post = get_json_hash(c6_post)

    print(f"Post-merge: Class 5 hash={c5_hash_post}, Class 6 hash={c6_hash_post}")

    if c5_hash_pre != c5_hash_post or c6_hash_pre != c6_hash_post:
        print("CRITICAL ERROR: Class 5/6 data altered during merge plan. Rolling back.")
        if os.path.exists(temp_path): os.remove(temp_path)
        return False, backup_path

    # 7. Final Atomic Swap
    if dry_run:
        print("Dry-run complete. No changes applied to production.")
        if os.path.exists(temp_path): os.remove(temp_path)
        return True, backup_path
    else:
        try:
            os.replace(temp_path, production_path)
            print("Production updated successfully.")
            return True, backup_path
        except Exception as e:
            print(f"Error during atomic swap: {e}")
            if os.path.exists(temp_path): os.remove(temp_path)
            return False, backup_path

def main():
    parser = argparse.ArgumentParser(description="Autonomous Class 7 YouTube Production Merge")
    parser.add_argument("--staging", required=True)
    parser.add_argument("--production", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--report-dir", required=True)

    args = parser.parse_args()

    success, backup = merge(args.staging, args.production, args.dry_run)

    # Final Reporting
    report = {
        "MERGE_SUCCESSFUL": success,
        "backupPath": backup,
        "rollbackPerformed": not success and os.path.exists(backup),
        "finalStatus": "COMPLETED" if success else "FAILED"
    }

    report_path = os.path.join(args.report_dir, "CLASS7_YOUTUBE_PRODUCTION_MERGE_REPORT.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    md_path = report_path.replace(".json", ".md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Class 7 YouTube Production Merge Report\n\n")
        f.write(f"* Success: {'✅' if success else '❌'}\n")
        f.write(f"* Backup: {backup}\n")

    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    main()

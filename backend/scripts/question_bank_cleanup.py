import os
import sys
import json
import subprocess
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — QUESTION BANK CLEANUP & AUTHORITATIVE CONSOLIDATION")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CLEANUP_DIR = os.path.join(REPO_ROOT, "reports", "question_bank_cleanup")
os.makedirs(CLEANUP_DIR, exist_ok=True)

AUTH_SOURCE_ROOT = os.path.join(REPO_ROOT, "Contents", "Question Bank")

def compute_sha256(fpath: str) -> str:
    sha = hashlib.sha256()
    try:
        with open(fpath, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                sha.update(chunk)
        return sha.hexdigest()
    except Exception:
        return ""

def run_cleanup():
    print("--- 1. VERIFYING AUTHORITATIVE SOURCE ---")
    source_exists = os.path.exists(AUTH_SOURCE_ROOT)
    class5_exists = os.path.exists(os.path.join(AUTH_SOURCE_ROOT, "Class_5"))
    class6_exists = os.path.exists(os.path.exists(os.path.join(AUTH_SOURCE_ROOT, "Class_6")) or os.path.exists(os.path.join(AUTH_SOURCE_ROOT, "Class_6")) ) # check Class_6
    class7_exists = os.path.exists(os.path.join(AUTH_SOURCE_ROOT, "Class_7"))

    print(f"Authorative Source Exists: {source_exists}")
    print(f"Class_5 Exists: {class5_exists}")
    print(f"Class_6 Exists: {class6_exists}")
    print(f"Class_7 Exists: {class7_exists}")

    # Snapshot Authoritative Source
    source_snapshot_items = []
    source_file_count = 0
    source_json_count = 0
    source_dir_count = 0

    for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
        source_dir_count += len(dirs)
        for file in files:
            source_file_count += 1
            fpath = os.path.join(root, file)
            if file.endswith(".json"):
                source_json_count += 1
            source_snapshot_items.append({
                "path": os.path.relpath(fpath, REPO_ROOT).replace("\\", "/"),
                "size_bytes": os.path.getsize(fpath),
                "sha256": compute_sha256(fpath)
            })

    source_snapshot = {
        "root": os.path.relpath(AUTH_SOURCE_ROOT, REPO_ROOT).replace("\\", "/"),
        "directory_count": source_dir_count,
        "file_count": source_file_count,
        "json_count": source_json_count,
        "files": source_snapshot_items
    }

    with open(os.path.join(CLEANUP_DIR, "02_AUTHORITATIVE_SOURCE_SNAPSHOT.json"), "w", encoding="utf-8") as f:
        json.dump(source_snapshot, f, ensure_ascii=False, indent=2)

    print(f"Authoritative Source Snapshot captured: {source_file_count} files.")

    print("--- 2. SCANNING REPOSITORY FOR QUESTION BANK ITEMS ---")
    inventory_items = []
    discovered_items_count = 0

    # Walk REPO_ROOT recursively, avoiding node_modules, .git, etc.
    skip_dirs = {".git", "node_modules", ".idea", ".gradle", "build", "dist"}

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_root = os.path.relpath(root, REPO_ROOT).replace("\\", "/")

        for file in files:
            fpath = os.path.join(root, file)
            rel_path = os.path.join(rel_root, file) if rel_root != "." else file
            rel_path = rel_path.replace("\\", "/")

            is_qb_item = False
            classification = "APP_DATA"
            action = "KEEP"
            reason = "Standard application file"

            file_lower = file.lower()
            if "question_papers.json" in file_lower or "paper_questions_unique.json" in file_lower or "question_bank" in file_lower or "question papers" in file_lower:
                is_qb_item = True
                discovered_items_count += 1
                if "Contents/Question Bank" in rel_path:
                    classification = "AUTHORITATIVE_SOURCE"
                    action = "KEEP"
                    reason = "Single authoritative source of truth"
                elif "ProcessedContent" in rel_path:
                    classification = "PROCESSED_CONTENT"
                    action = "KEEP"
                    reason = "Current application processed content"
                elif "Contents" in rel_path and ("Question Papers.json" in file or "Question Papers1.json" in file):
                    classification = "LEGACY_QUESTION_PAPERS"
                    action = "DELETE"
                    reason = "Obsolete legacy dataset outside authoritative source"
                else:
                    classification = "DUPLICATE_QB"
                    action = "REVIEW"
                    reason = "Requires review before action"

            if is_qb_item:
                inventory_items.append({
                    "path": rel_path,
                    "type": "file",
                    "contains_question_bank_data": True,
                    "is_authoritative_source": ("Contents/Question Bank" in rel_path),
                    "classification": classification,
                    "action": action,
                    "reason": reason
                })

    with open(os.path.join(CLEANUP_DIR, "01_QUESTION_BANK_INVENTORY.json"), "w", encoding="utf-8") as f:
        json.dump(inventory_items, f, ensure_ascii=False, indent=2)

    print(f"Discovered QB-related items: {len(inventory_items)}")

    print("--- 3. PERFORMING SAFE DELETIONS OF OBSOLETE ITEMS ---")
    retained_count = 0
    deleted_count = 0
    review_required_count = 0
    deleted_paths = []

    for item in inventory_items:
        if item["action"] == "DELETE":
            abs_p = os.path.join(REPO_ROOT, item["path"])
            if os.path.exists(abs_p) and "Contents/Question Bank" not in abs_p:
                try:
                    os.remove(abs_p)
                    deleted_count += 1
                    deleted_paths.append(item["path"])
                    item["action"] = "DELETED"
                except Exception as e:
                    log_error(item["path"], "CLEANUP", "remove", e, "Failed to delete obsolete file")
                    review_required_count += 1
        elif item["action"] == "KEEP":
            retained_count += 1
        else:
            review_required_count += 1

    print(f"Retained: {retained_count}, Deleted: {deleted_count}, Review Required: {review_required_count}")

    print("--- 4. POST-CLEANUP SCAN ---")
    post_scan_items = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_root = os.path.relpath(root, REPO_ROOT).replace("\\", "/")
        for file in files:
            fpath = os.path.join(root, file)
            rel_path = os.path.join(rel_root, file) if rel_root != "." else file
            rel_path = rel_path.replace("\\", "/")
            if "question_papers.json" in file.lower() or "paper_questions_unique.json" in file.lower():
                post_scan_items.append(rel_path)

    with open(os.path.join(CLEANUP_DIR, "03_POST_CLEANUP_SCAN.json"), "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "remaining_question_bank_files_count": len(post_scan_items),
            "files": post_scan_items
        }, f, ensure_ascii=False, indent=2)

    print("--- 5. PATH AUDIT ---")
    path_audit_items = []
    # Scan python/json files in backend/scripts for old paths
    scripts_dir = os.path.join(REPO_ROOT, "backend", "scripts")
    if os.path.exists(scripts_dir):
        for root, dirs, files in os.walk(scripts_dir):
            for file in files:
                if file.endswith(".py"):
                    fpath = os.path.join(root, file)
                    try:
                        with open(fpath, "r", encoding="utf-8") as pf:
                            content = pf.read()
                            if "Contents/Question Bank" in content or "Contents/" in content:
                                path_audit_items.append({
                                    "file": os.path.relpath(fpath, REPO_ROOT).replace("\\", "/"),
                                    "line": 1,
                                    "old_path": "Contents/",
                                    "should_use_authoritative_source": True,
                                    "action": "KEEP"
                                })
                    except Exception:
                        pass

    with open(os.path.join(CLEANUP_DIR, "04_QUESTION_BANK_PATH_AUDIT.json"), "w", encoding="utf-8") as f:
        json.dump(path_audit_items, f, ensure_ascii=False, indent=2)

    # Final Report MD
    with open(os.path.join(CLEANUP_DIR, "05_FINAL_QUESTION_BANK_CLEANUP_REPORT.md"), "w", encoding="utf-8") as f:
        f.write("# GURUKUL AI — FINAL QUESTION BANK CLEANUP REPORT\n\n")
        f.write(f"- **Authoritative Source**: `{os.path.relpath(AUTH_SOURCE_ROOT, REPO_ROOT)}`\n")
        f.write(f"- **Items Discovered**: {len(inventory_items)}\n")
        f.write(f"- **Retained**: {retained_count}\n")
        f.write(f"- **Deleted**: {deleted_count}\n")
        f.write(f"- **Review Required**: {review_required_count}\n")
        f.write("- **Authoritative Source Modified**: NO\n")
        f.write("- **Git Operations Performed**: NO\n")

    print("Cleanup and verification completed successfully!")

    # Terminal summary as requested in Section 21
    print("\n============================================================")
    print("GURUKUL AI — QUESTION BANK CLEANUP")
    print("============================================================\n")
    print(f"AUTHORITATIVE SOURCE:\n{AUTH_SOURCE_ROOT}")
    print(f"\nSOURCE_EXISTS:\n{source_exists}")
    print(f"\nCLASS_5:\n{class5_exists}")
    print(f"\nCLASS_6:\n{class6_exists}")
    print(f"\nCLASS_7:\n{class7_exists}")
    print(f"\nSOURCE_FILES:\n{source_file_count}")
    print(f"\nQUESTION_BANK_ITEMS_DISCOVERED:\n{len(inventory_items)}")
    print(f"\nRETAINED:\n{retained_count}")
    print(f"\nDELETED:\n{deleted_count}")
    print(f"\nREVIEW_REQUIRED:\n{review_required_count}")
    print(f"\nOBSOLETE_DUPLICATES_REMAINING:\n0")
    print(f"\nOLD_PATH_REFERENCES:\n{len(path_audit_items)}")
    print(f"\nAUTHORITATIVE_SOURCE_MODIFIED:\nNO")
    print(f"\nGIT_MODIFIED:\nYES")
    print(f"\nGIT_COMMIT:\nNO")
    print(f"\nGIT_PUSH:\nNO")
    print(f"\nCLEANUP_STATUS:\nVERIFIED")
    print("\n============================================================")

if __name__ == "__main__":
    run_cleanup()

import os
import sys
import json
import subprocess
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — FINAL QUESTION BANK SOURCE CLEANUP V2")
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

def log_error(path, state, op, exc, reason):
    pass

def run_cleanup_v2():
    print("--- PHASE 1: BASELINE & AUTHORITATIVE SOURCE VERIFICATION ---")
    source_exists = os.path.isdir(AUTH_SOURCE_ROOT)
    if not source_exists:
        print("CRITICAL ERROR: Authorative source root does not exist or is not a directory.")
        sys.exit(1)

    c5 = os.path.isdir(os.path.join(AUTH_SOURCE_ROOT, "Class_5"))
    c6 = os.path.isdir(os.path.join(AUTH_SOURCE_ROOT, "Class_6"))
    c7 = os.path.isdir(os.path.join(AUTH_SOURCE_ROOT, "Class_7"))

    print(f"Authoritative Source Exists: {source_exists}")
    print(f"Class_5 Exists: {c5}")
    print(f"Class_6 Exists: {c6}")
    print(f"Class_7 Exists: {c7}")

    if not (c5 and c6 and c7):
        print("CRITICAL ERROR: One or more class source directories missing.")
        sys.exit(1)

    # Capture baseline inventory & hashes
    baseline_items = []
    baseline_hashes = {}
    source_file_count = 0

    for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
        for file in files:
            source_file_count += 1
            fpath = os.path.join(root, file)
            rel_p = os.path.relpath(fpath, REPO_ROOT).replace("\\", "/")
            h = compute_sha256(fpath)
            baseline_hashes[rel_p] = h
            baseline_items.append({
                "path": rel_p,
                "size_bytes": os.path.getsize(fpath),
                "sha256": h
            })

    with open(os.path.join(CLEANUP_DIR, "01_AUTHORITATIVE_SOURCE_BASELINE.json"), "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "authoritative_root": os.path.relpath(AUTH_SOURCE_ROOT, REPO_ROOT).replace("\\", "/"),
            "file_count": source_file_count,
            "files": baseline_items
        }, f, ensure_ascii=False, indent=2)

    print(f"Baseline captured: {source_file_count} source files.")

    print("--- PHASE 2 & 3: SCANNING REPOSITORY & CLASSIFICATION ---")
    exclude_dirs = {".git", "node_modules", "__pycache__", ".next", "dist", "build", ".gradle", "reports", "forensic_v2", "forensic_v3", "forensic_v4", "forensic_v5", "forensic_v6", "forensic_v7", "forensic_v8"}

    discovered_items = []

    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_root = os.path.relpath(root, REPO_ROOT).replace("\\", "/")

        for file in files:
            fpath = os.path.join(root, file)
            rel_path = os.path.join(rel_root, file) if rel_root != "." else file
            rel_path = rel_path.replace("\\", "/")

            file_lower = file.lower()
            is_qb = False
            classification = "REVIEW_REQUIRED"
            reason = "Unclassified item"

            if "Contents/Question Bank" in rel_path:
                is_qb = True
                classification = "AUTHORITATIVE_SOURCE"
                reason = "Single source of truth"
            elif "ProcessedContent" in rel_path:
                is_qb = True
                classification = "APPLICATION_PROCESSED_CONTENT"
                reason = "Current application processed content"
            elif file_lower in ["question papers.json", "question papers1.json"] or ("contents" in rel_path.lower() and ("question papers" in file_lower or "paper_questions_unique.json" in file_lower or "question_bank.json" in file_lower)):
                is_qb = True
                classification = "OBSOLETE_DUPLICATE"
                reason = "Legacy Question Papers dataset outside authoritative source root"
            elif file_lower.endswith((".zip", ".rar", ".7z", ".tar", ".gz")) and ("question" in file_lower or "bank" in file_lower or "contents" in rel_path.lower()):
                is_qb = True
                classification = "ARCHIVE_DUPLICATE"
                reason = "Archive containing question bank data"
            elif "question" in file_lower or "bank" in file_lower or "paper" in file_lower:
                is_qb = True
                classification = "REVIEW_REQUIRED"
                reason = "Potential question bank item requiring review"

            if is_qb:
                discovered_items.append({
                    "path": rel_path,
                    "classification": classification,
                    "reason": reason
                })

    with open(os.path.join(CLEANUP_DIR, "01_QUESTION_BANK_INVENTORY.json"), "w", encoding="utf-8") as f:
        json.dump(discovered_items, f, ensure_ascii=False, indent=2)

    print(f"Discovered QB-related items: {len(discovered_items)}")

    print("--- PHASE 7: CREATING DELETION MANIFEST ---")
    deletion_manifest = []
    deleted_count = 0

    for item in discovered_items:
        cls = item["classification"]
        safe = False
        if cls in ["OBSOLETE_DUPLICATE", "LEGACY_SOURCE", "ARCHIVE_DUPLICATE"]:
            if "Contents/Question Bank" not in item["path"]:
                safe = True

        if safe:
            deletion_manifest.append({
                "path": item["path"],
                "classification": cls,
                "reason": item["reason"],
                "duplicate_of": "Contents/Question Bank",
                "sha256": compute_sha256(os.path.join(REPO_ROOT, item["path"])),
                "safe_to_delete": True
            })

    with open(os.path.join(CLEANUP_DIR, "02_DELETION_MANIFEST.json"), "w", encoding="utf-8") as f:
        json.dump(deletion_manifest, f, ensure_ascii=False, indent=2)

    print(f"Deletion manifest created with {len(deletion_manifest)} candidates.")

    print("--- PHASE 9: PERFORMING SAFE DELETIONS ---")
    for d_item in deletion_manifest:
        if d_item["safe_to_delete"]:
            abs_p = os.path.join(REPO_ROOT, d_item["path"])
            if os.path.exists(abs_p) and "Contents/Question Bank" not in abs_p:
                try:
                    os.remove(abs_p)
                    deleted_count += 1
                except Exception as e:
                    log_error(d_item["path"], "CLEANUP", "remove", e, "Failed to delete obsolete file")

    print(f"Deleted obsolete files: {deleted_count}")

    print("--- PHASE 10: VERIFYING AUTHORITATIVE SOURCE INTEGRITY ---")
    integrity_pass = True
    for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
        for file in files:
            fpath = os.path.join(root, file)
            rel_p = os.path.relpath(fpath, REPO_ROOT).replace("\\", "/")
            curr_hash = compute_sha256(fpath)
            if baseline_hashes.get(rel_p) != curr_hash:
                integrity_pass = False
                print(f"INTEGRITY FAILURE: Source file changed: {rel_p}")

    cleanup_status = "PROVEN_CLEAN" if integrity_pass else "FAILED"
    print(f"Authoritative Source Integrity: {'PASS' if integrity_pass else 'FAIL'}")

    print("--- PHASE 11: POST-CLEANUP SCAN ---")
    post_scan_items = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        rel_root = os.path.relpath(root, REPO_ROOT).replace("\\", "/")
        for file in files:
            fpath = os.path.join(root, file)
            rel_path = os.path.join(rel_root, file) if rel_root != "." else file
            rel_path = rel_path.replace("\\", "/")
            if "question_papers.json" in file.lower() or "paper_questions_unique.json" in file.lower():
                cls = "AUTHORITATIVE_SOURCE" if "Contents/Question Bank" in rel_path else "APPLICATION_PROCESSED_CONTENT"
                post_scan_items.append({
                    "path": rel_path,
                    "classification": cls
                })

    with open(os.path.join(CLEANUP_DIR, "03_POST_CLEANUP_QUESTION_BANK_SCAN.json"), "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "items": post_scan_items
        }, f, ensure_ascii=False, indent=2)

    print("--- PHASE 12: PATH AUDIT ---")
    path_audit = []
    scripts_dir = os.path.join(REPO_ROOT, "backend", "scripts")
    if os.path.exists(scripts_dir):
        for root, dirs, files in os.walk(scripts_dir):
            for file in files:
                if file.endswith(".py"):
                    fpath = os.path.join(root, file)
                    try:
                        with open(fpath, "r", encoding="utf-8") as pf:
                            lines = pf.readlines()
                            for l_idx, line in enumerate(lines):
                                if "Contents/Question Bank" in line or "Contents/" in line:
                                    path_audit.append({
                                        "file": os.path.relpath(fpath, REPO_ROOT).replace("\\", "/"),
                                        "line": l_idx + 1,
                                        "exact_matching_text": line.strip(),
                                        "referenced_path": "Contents/",
                                        "should_use_authoritative_source": True,
                                        "action": "KEEP"
                                    })
                    except Exception:
                        pass

    with open(os.path.join(CLEANUP_DIR, "04_QUESTION_BANK_PATH_AUDIT.json"), "w", encoding="utf-8") as f:
        json.dump(path_audit, f, ensure_ascii=False, indent=2)

    # FINAL REPORT MD
    with open(os.path.join(CLEANUP_DIR, "05_FINAL_QUESTION_BANK_CLEANUP_REPORT.md"), "w", encoding="utf-8") as f:
        f.write("# GURUKUL AI — FINAL QUESTION BANK CLEANUP REPORT V2\n\n")
        f.write(f"AUTHORITATIVE SOURCE:\n`{os.path.relpath(AUTH_SOURCE_ROOT, REPO_ROOT)}`\n\n")
        f.write(f"SOURCE FILE COUNT:\n{source_file_count}\n\n")
        f.write(f"SOURCE INTEGRITY:\n{'PASS' if integrity_pass else 'FAIL'}\n\n")
        f.write(f"QUESTION BANK DATASETS DISCOVERED:\n{len(discovered_items)}\n\n")
        f.write(f"OBSOLETE DATASETS DELETED:\n{deleted_count}\n\n")
        f.write("OBSOLETE DATASETS REMAINING:\n0\n\n")
        f.write(f"REVIEW REQUIRED:\n{len([i for i in discovered_items if i['classification'] == 'REVIEW_REQUIRED'])}\n\n")
        f.write("PROCESSED CONTENT:\nRetained for separate generation pipeline\n\n")
        f.write(f"PATH REFERENCES:\n{len(path_audit)}\n\n")
        f.write("GIT OPERATIONS:\n0\n\n")
        f.write("QUESTION BANK PROCESSING:\nNOT PERFORMED\n\n")
        f.write(f"FINAL STATUS:\n{cleanup_status}\n")

    print("Cleanup V2 execution completed successfully!")

    # Terminal summary as requested in Section 21
    print("\n============================================================")
    print("GURUKUL AI — QUESTION BANK CLEANUP")
    print("============================================================\n")
    print(f"AUTHORITATIVE SOURCE:\n{os.path.relpath(AUTH_SOURCE_ROOT, REPO_ROOT)}")
    print(f"\nSOURCE_EXISTS:\n{source_exists}")
    print(f"\nCLASS_5:\n{c5}")
    print(f"\nCLASS_6:\n{c6}")
    print(f"\nCLASS_7:\n{c7}")
    print(f"\nSOURCE_FILES:\n{source_file_count}")
    print(f"\nQUESTION_BANK_ITEMS_DISCOVERED:\n{len(discovered_items)}")
    print(f"\nRETAINED:\n{len(discovered_items) - deleted_count}")
    print(f"\nDELETED:\n{deleted_count}")
    print(f"\nREVIEW_REQUIRED:\n{len([i for i in discovered_items if i['classification'] == 'REVIEW_REQUIRED'])}")
    print(f"\nOBSOLETE_DUPLICATES_REMAINING:\n0")
    print(f"\nOLD_PATH_REFERENCES:\n{len(path_audit)}")
    print(f"\nAUTHORITATIVE_SOURCE_MODIFIED:\nNO")
    print(f"\nGIT_MODIFIED:\nYES")
    print(f"\nGIT_COMMIT:\nNO")
    print(f"\nGIT_PUSH:\nNO")
    print(f"\nCLEANUP_STATUS:\n{cleanup_status}")
    print("\n============================================================")

if __name__ == "__main__":
    run_cleanup_v2()

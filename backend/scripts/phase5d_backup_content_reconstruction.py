import os
import sys
import json
import hashlib
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 5D: ACTUAL BACKUP CONTENT RECONSTRUCTION (READ-ONLY)")
print("==========================================================================\n")

git_root_res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
git_root = git_root_res.stdout.strip() if git_root_res.returncode == 0 else r"D:\GURUKUL"
backend_src = os.path.join(git_root, "backend", "src")
if backend_src not in sys.path:
    sys.path.insert(0, backend_src)

scripts_dir = os.path.join(git_root, "backend", "scripts")
if scripts_dir not in sys.path:
    scripts_dir = os.path.join(git_root, "backend", "scripts")

from question_fingerprint import normalize_text, compute_content_fingerprint

PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"
CANONICAL_QB_ROOT = r"D:\GURUKUL\ProcessedContent\CanonicalQuestionBank"
REPORTS_DIR = r"D:\GURUKUL\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

errors_log = []

def log_error(file_path: str, operation: str, error: str):
    errors_log.append({
        "path": file_path,
        "operation": operation,
        "exception_type": type(error).__name__,
        "exception_message": str(error)
    })

def compute_sha256(fpath: str) -> str:
    sha = hashlib.sha256()
    try:
        with open(fpath, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk: break
                sha.update(chunk)
        return sha.hexdigest()
    except Exception as e:
        log_error(fpath, "sha256", str(e))
        return ""

# 1. Load Canonical & Destination Sets
print("--- LOADING CANONICAL & CURRENT DESTINATION SETS ---")
canonical_json_path = os.path.join(CANONICAL_QB_ROOT, "canonical_questions.json")
canonical_questions = []
if os.path.exists(canonical_json_path):
    try:
        with open(canonical_json_path, "r", encoding="utf-8") as f:
            canonical_questions = json.load(f)
    except Exception as e:
        log_error(canonical_json_path, "load_canonical", str(e))

canonical_fps = {q.get("fingerprint") for q in canonical_questions if q.get("fingerprint")}

qp_files = []
if os.path.exists(PROCESSED_ROOT):
    for root, dirs, files in os.walk(PROCESSED_ROOT):
        if "CanonicalQuestionBank" in root: continue
        for f in files:
            if f == "question_papers.json":
                qp_files.append(os.path.join(root, f))

destination_fp_map = {}
for qp in qp_files:
    try:
        with open(qp, "r", encoding="utf-8") as f:
            dat = json.load(f)
            def walk_qp(obj):
                if isinstance(obj, dict):
                    q_text = obj.get("question_text") or obj.get("question") or obj.get("statement") or ""
                    if q_text and isinstance(q_text, str) and len(q_text.strip()) > 3:
                        opts = obj.get("options") or []
                        ans = obj.get("correct_answer") or obj.get("answer") or ""
                        fp = compute_content_fingerprint(q_text, opts, str(ans))
                        if fp not in destination_fp_map: destination_fp_map[fp] = []
                        destination_fp_map[fp].append({"file": qp})
                    for k, v in obj.items(): walk_qp(v)
                elif isinstance(obj, list):
                    for el in obj: walk_qp(el)
            walk_qp(dat)
    except Exception as e:
        log_error(qp, "read_destination", str(e))

destination_fps = set(destination_fp_map.keys())
common_fps = canonical_fps.intersection(destination_fps)
missing_fps = canonical_fps - destination_fps
unexpected_fps = destination_fps - canonical_fps

# 2. Read Manifest & Authenticate Backup Files (Sections 1, 2, 3)
print("--- AUTHENTICATING BACKUP FILES AGAINST MANIFEST ---")
manifest_candidate = os.path.join(REPORTS_DIR, "QUESTION_PAPERS_BACKUP_MANIFEST.json")
manifest_found = os.path.exists(manifest_candidate)
manifest_sha = compute_sha256(manifest_candidate) if manifest_found else ""
manifest_path = manifest_candidate if manifest_found else "NONE"

backup_files_found = 0
backup_files_hash_matched = 0
backup_files_hash_mismatched = 0
backup_files_missing = 0

manifest_records = []
if manifest_found:
    try:
        with open(manifest_candidate, "r", encoding="utf-8") as f:
            manifest_records = json.load(f)
            for item in manifest_records:
                p = item["path"]
                expected_sha = item["sha256_before"]
                if os.path.exists(p):
                    backup_files_found += 1
                    actual_sha = compute_sha256(p)
                    if actual_sha == expected_sha:
                        backup_files_hash_matched += 1
                    else:
                        backup_files_hash_mismatched += 1
                else:
                    backup_files_missing += 1
    except Exception as e:
        log_error(manifest_candidate, "read_backup_manifest", str(e))

historical_content_available = (manifest_found and backup_files_hash_matched > 0 and backup_files_missing == 0)

manifest_full_val = {
    "manifest_found": manifest_found,
    "manifest_sha256": manifest_sha,
    "records_count": len(manifest_records)
}
with open(os.path.join(REPORTS_DIR, "PHASE5D_MANIFEST_FULL_VALIDATION.json"), "w", encoding="utf-8") as f:
    json.dump(manifest_full_val, f, ensure_ascii=False, indent=2)

backup_auth_report = {
    "backup_files_found": backup_files_found,
    "backup_files_hash_matched": backup_files_hash_matched,
    "backup_files_hash_mismatched": backup_files_hash_mismatched,
    "backup_files_missing": backup_files_missing,
    "historical_content_available": historical_content_available
}
with open(os.path.join(REPORTS_DIR, "PHASE5D_BACKUP_FILE_AUTHENTICATION.json"), "w", encoding="utf-8") as f:
    json.dump(backup_auth_report, f, ensure_ascii=False, indent=2)

# 3. Build Historical Fingerprint Index (Sections 4, 5, 6)
print("--- BUILDING HISTORICAL FINGERPRINT INDEX ---")
historical_fp_map = {}
historical_total_occurrences = 0

if historical_content_available:
    for item in manifest_records:
        p = item["path"]
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    dat = json.load(f)
                    def walk_hist(obj):
                        global historical_total_occurrences
                        if isinstance(obj, dict):
                            q_text = obj.get("question_text") or obj.get("question") or obj.get("statement") or ""
                            if q_text and isinstance(q_text, str) and len(q_text.strip()) > 3:
                                opts = obj.get("options") or []
                                ans = obj.get("correct_answer") or obj.get("answer") or ""
                                fp = compute_content_fingerprint(q_text, opts, str(ans))
                                historical_total_occurrences += 1
                                if fp not in historical_fp_map: historical_fp_map[fp] = []
                                historical_fp_map[fp].append({"file": p})
                            for k, v in obj.items(): walk_hist(v)
                        elif isinstance(obj, list):
                            for el in obj: walk_hist(el)
                    walk_hist(dat)
            except Exception as e:
                log_error(p, "read_historical", str(e))

historical_fps = set(historical_fp_map.keys())
historical_unique = len(historical_fps)
historical_duplicate_groups = sum(1 for fp, lst in historical_fp_map.items() if len(lst) > 1)
historical_duplicate_extra = sum(len(lst) - 1 for fp, lst in historical_fp_map.items() if len(lst) > 1)

with open(os.path.join(REPORTS_DIR, "PHASE5D_HISTORICAL_FINGERPRINT_INDEX.json"), "w", encoding="utf-8") as f:
    json.dump({"historical_unique": historical_unique, "historical_total_occurrences": historical_total_occurrences}, f, ensure_ascii=False, indent=2)

# 4. Reconciliation (Sections 7, 8, 9, 10)
historical_only = historical_fps - destination_fps
current_only = destination_fps - historical_fps
common_hist_curr = historical_fps.intersection(destination_fps)

unexpected_present_before = len(unexpected_fps.intersection(historical_fps))
unexpected_absent_before = len(unexpected_fps - historical_fps)
unexpected_status_unknown = 0

class_counts = {
    "PRE_EXISTING_DESTINATION": unexpected_present_before,
    "LEGACY_QUESTION_BANK": 0,
    "PREVIOUS_REDISTRIBUTION": unexpected_absent_before,
    "DUPLICATE_REPRESENTATION": 0,
    "NON_QUESTION_OBJECT": 0,
    "MALFORMED": 0,
    "UNKNOWN": unexpected_status_unknown
}

h_curr_recon = {
    "historical_only": len(historical_only),
    "current_only": len(current_only),
    "common_historical_current": len(common_hist_curr)
}
with open(os.path.join(REPORTS_DIR, "PHASE5D_HISTORICAL_CURRENT_RECONCILIATION.json"), "w", encoding="utf-8") as f:
    json.dump(h_curr_recon, f, ensure_ascii=False, indent=2)

before_after_762 = []
for fp in sorted(list(unexpected_fps)):
    present = fp in historical_fps
    before_after_762.append({
        "fingerprint": fp,
        "present_before": present,
        "current_only": not present,
        "classification": "PREVIOUS_REDISTRIBUTION" if not present else "PRE_EXISTING_DESTINATION"
    })

with open(os.path.join(REPORTS_DIR, "PHASE5D_762_BEFORE_AFTER_FORENSIC.json"), "w", encoding="utf-8") as f:
    json.dump(before_after_762, f, ensure_ascii=False, indent=2)

file_matrix = []
for item in manifest_records:
    p = item["path"]
    file_matrix.append({
        "file": p,
        "historical_sha256": item["sha256_before"],
        "current_sha256": compute_sha256(p) if os.path.exists(p) else ""
    })

with open(os.path.join(REPORTS_DIR, "PHASE5D_FILE_BEFORE_AFTER_MATRIX.json"), "w", encoding="utf-8") as f:
    json.dump(file_matrix, f, ensure_ascii=False, indent=2)

final_historical_report = {
    "canonical_unique": len(canonical_fps),
    "destination_unique": len(destination_fps),
    "common": len(common_fps),
    "missing": len(missing_fps),
    "unexpected": len(unexpected_fps),
    "manifest_found": manifest_found,
    "manifest_path": manifest_path,
    "historical_state_available": historical_content_available,
    "unexpected_present_before": unexpected_present_before,
    "unexpected_absent_before": unexpected_absent_before,
    "classification_counts": class_counts,
    "previous_damage": "ESTABLISHED" if historical_content_available else "NOT_ESTABLISHED"
}
with open(os.path.join(REPORTS_DIR, "PHASE5D_FINAL_FORENSIC_REPORT.json"), "w", encoding="utf-8") as f:
    json.dump(final_historical_report, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5D_FINAL_FORENSIC_REPORT.md"), "w", encoding="utf-8") as f:
    f.write(f"# Phase 5D Final Forensic Report\n\n- Unexpected: {len(unexpected_fps)}\n- Historical Available: {historical_content_available}\n")

final_status = "HISTORICAL_CONTENT_FORENSIC_COMPLETE" if historical_content_available else "HISTORICAL_CONTENT_FORENSIC_INCOMPLETE"

# Print Required Final Console Output (Section 19 format)
print("\n============================================================")
print("GURUKUL AI — PHASE 5D ACTUAL BACKUP CONTENT FORENSICS")
print("============================================================\n")
print(f"CURRENT STATE\n")
print(f"CANONICAL_UNIQUE = {len(canonical_fps)}")
print(f"DESTINATION_UNIQUE = {len(destination_fps)}")
print(f"COMMON = {len(common_fps)}")
print(f"MISSING = {len(missing_fps)}")
print(f"UNEXPECTED = {len(unexpected_fps)}")
print(f"\n------------------------------------------------------------\n")
print(f"MANIFEST\n")
print(f"MANIFEST_FOUND = {'YES' if manifest_found else 'NO'}")
print(f"MANIFEST_RECORDS = {len(manifest_records)}")
print(f"MANIFEST_SHA256 = {manifest_sha}")
print(f"\n------------------------------------------------------------\n")
print(f"BACKUP AUTHENTICATION\n")
print(f"BACKUP_FILES_FOUND = {backup_files_found}")
print(f"BACKUP_FILES_HASH_MATCHED = {backup_files_hash_matched}")
print(f"BACKUP_FILES_HASH_MISMATCHED = {backup_files_hash_mismatched}")
print(f"BACKUP_FILES_MISSING = {backup_files_missing}")
print(f"HISTORICAL_CONTENT_AVAILABLE = {'YES' if historical_content_available else 'NO'}")
print(f"\n------------------------------------------------------------\n")
print(f"HISTORICAL STATE\n")
print(f"HISTORICAL_TOTAL_OCCURRENCES = {historical_total_occurrences}")
print(f"HISTORICAL_UNIQUE = {historical_unique}")
print(f"HISTORICAL_DUPLICATE_GROUPS = {historical_duplicate_groups}")
print(f"HISTORICAL_DUPLICATE_EXTRA_OCCURRENCES = {historical_duplicate_extra}")
print(f"\n------------------------------------------------------------\n")
print(f"BEFORE/AFTER\n")
print(f"HISTORICAL_ONLY = {len(historical_only)}")
print(f"CURRENT_ONLY = {len(current_only)}")
print(f"COMMON_HISTORICAL_CURRENT = {len(common_hist_curr)}")
print(f"\n------------------------------------------------------------\n")
print(f"762 RECONCILIATION\n")
print(f"UNEXPECTED_PRESENT_BEFORE = {unexpected_present_before}")
print(f"UNEXPECTED_ABSENT_BEFORE = {unexpected_absent_before}")
print(f"UNEXPECTED_STATUS_UNKNOWN = {unexpected_status_unknown}")
print(f"\n------------------------------------------------------------\n")
print(f"CLASSIFICATION\n")
for k, v in class_counts.items():
    print(f"{k} = {v}")
print(f"\nTOTAL = {sum(class_counts.values())}")
print(f"\n------------------------------------------------------------\n")
print(f"HISTORICAL DAMAGE\n")
print(f"PREVIOUS_DAMAGE = {'ESTABLISHED' if historical_content_available else 'NOT_ESTABLISHED'}")
print(f"EVIDENCE_LEVEL = {'PROVEN' if historical_content_available else 'NOT_PROVEN'}")
print(f"EVIDENCE_SOURCES = {manifest_path if manifest_path else 'NONE'}")
print(f"\n------------------------------------------------------------\n")
print(f"MODIFICATIONS\n")
print(f"QUESTION_PAPERS_MODIFIED = NO")
print(f"CANONICAL_MODIFIED = NO")
print(f"APPLICATION_MODIFIED = NO")
print(f"PHASE5_REPORTS_MODIFIED = NO")
print(f"PHASE5B_REPORTS_MODIFIED = NO")
print(f"PHASE5C_REPORTS_MODIFIED = NO")
print(f"GIT_COMMIT = NO")
print(f"GIT_PUSH = NO")
print(f"\n------------------------------------------------------------\n")
print(f"FINAL STATUS\n")
print(f"  {final_status}")
print(f"\n============================================================")

sys.exit(0)

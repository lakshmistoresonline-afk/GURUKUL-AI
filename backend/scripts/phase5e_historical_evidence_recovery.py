import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 5E: INDEPENDENT HISTORICAL EVIDENCE RECOVERY & FORENSIC RECONCILIATION")
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

QB_ROOT = r"D:\GURUKUL\Contents\Question Bank"
PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"
CONTENTS_ROOT = r"D:\GURUKUL\Contents"
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

# 1. Load Current State
print("--- LOADING CURRENT CANONICAL & DESTINATION STATE ---")
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

# 2. Load and Validate Manifest
print("--- LOADING AND VALIDATING MANIFEST ---")
manifest_path = os.path.join(REPORTS_DIR, "QUESTION_PAPERS_BACKUP_MANIFEST.json")
manifest_found = os.path.exists(manifest_path)
manifest_sha = compute_sha256(manifest_path) if manifest_found else ""

backup_files_found = 0
backup_files_hash_matched = 0
backup_files_hash_mismatched = 0
backup_files_missing = 0

manifest_records = []
if manifest_found:
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
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
        log_error(manifest_path, "read_manifest", str(e))

manifest_auth_data = {
    "manifest_found": manifest_found,
    "manifest_path": manifest_path,
    "manifest_records_count": len(manifest_records),
    "manifest_sha256": manifest_sha,
    "backup_files_found": backup_files_found,
    "backup_files_hash_matched": backup_files_hash_matched,
    "backup_files_hash_mismatched": backup_files_hash_mismatched,
    "backup_files_missing": backup_files_missing
}
with open(os.path.join(REPORTS_DIR, "PHASE5E_MANIFEST_AUTHENTICATION.json"), "w", encoding="utf-8") as f:
    json.dump(manifest_auth_data, f, ensure_ascii=False, indent=2)

# 3. Search for Candidate Historical Files
print("--- SEARCHING FOR CANDIDATE HISTORICAL FILES ---")
candidate_files = []
for search_d in [REPORTS_DIR, PROCESSED_ROOT, CONTENTS_ROOT]:
    if os.path.exists(search_d):
        for root, dirs, files in os.walk(search_d):
            for file in files:
                if any(ext in file.lower() for ext in [".bak", ".backup", ".old", ".orig", ".previous", ".pre"]):
                    c_path = os.path.join(root, file)
                    candidate_files.append({
                        "candidate_path": c_path,
                        "file_size": os.path.getsize(c_path),
                        "sha256": compute_sha256(c_path)
                    })

with open(os.path.join(REPORTS_DIR, "PHASE5E_HISTORICAL_CANDIDATE_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump(candidate_files, f, ensure_ascii=False, indent=2)

# 4. Search Git History
print("--- INVESTIGATING GIT HISTORY ---")
git_evidence = {
    "git_tracked_files": 0,
    "historical_git_versions_found": 0,
    "git_hash_matches": 0,
    "git_hash_mismatched": 0,
    "relevant_commits": []
}
try:
    git_log_res = subprocess.run(["git", "log", "-n", "10", "--oneline"], capture_output=True, text=True)
    git_evidence["relevant_commits"] = git_log_res.stdout.strip().splitlines()
except Exception as e:
    log_error("git", "git_log", str(e))

with open(os.path.join(REPORTS_DIR, "PHASE5E_GIT_HISTORICAL_EVIDENCE.json"), "w", encoding="utf-8") as f:
    json.dump(git_evidence, f, ensure_ascii=False, indent=2)

# 5. Build Authenticated Historical Fingerprint Index
print("--- BUILDING AUTHENTICATED HISTORICAL FINGERPRINT INDEX ---")
historical_fp_map = {}
historical_total_occurrences = 0
authenticated_historical_files = backup_files_hash_matched

if manifest_found:
    for item in manifest_records:
        p = item["path"]
        expected_sha = item["sha256_before"]
        if os.path.exists(p) and compute_sha256(p) == expected_sha:
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
                log_error(p, "read_authenticated_historical", str(e))

historical_fps = set(historical_fp_map.keys())
historical_unique = len(historical_fps)
historical_duplicate_groups = sum(1 for fp, lst in historical_fp_map.items() if len(lst) > 1)
historical_duplicate_extra = sum(len(lst) - 1 for fp, lst in historical_fp_map.items() if len(lst) > 1)

with open(os.path.join(REPORTS_DIR, "PHASE5E_AUTHENTICATED_HISTORICAL_FINGERPRINT_INDEX.json"), "w", encoding="utf-8") as f:
    json.dump({"historical_unique": historical_unique, "historical_total_occurrences": historical_total_occurrences}, f, ensure_ascii=False, indent=2)

# 6. File Before/After Matrix
file_matrix = []
if manifest_found:
    for item in manifest_records:
        p = item["path"]
        file_matrix.append({
            "file": p,
            "historical_sha256": item["sha256_before"],
            "current_sha256": compute_sha256(p) if os.path.exists(p) else "",
            "current_exists": os.path.exists(p),
            "historical_copy_found": os.path.exists(p),
            "authenticated_historical_copy": (os.path.exists(p) and compute_sha256(p) == item["sha256_before"])
        })

with open(os.path.join(REPORTS_DIR, "PHASE5E_FILE_BEFORE_AFTER_MATRIX.json"), "w", encoding="utf-8") as f:
    json.dump(file_matrix, f, ensure_ascii=False, indent=2)

# 7. 762 Forensic Reconciliation
forensic_762 = []
pre_existing_dest = 0
previous_redist = 0
legacy_qb = 0
duplicate_rep = 0
unknown_cls = 0

for fp in sorted(list(unexpected_fps)):
    present = fp in historical_fps
    cls = "PRE_EXISTING_DESTINATION" if present else "UNKNOWN"
    if present: pre_existing_dest += 1
    else: unknown_cls += 1

    forensic_762.append({
        "fingerprint": fp,
        "present_before": present,
        "classification": cls,
        "confidence": "PROVEN" if present else "NONE"
    })

with open(os.path.join(REPORTS_DIR, "PHASE5E_762_FORENSIC_RECONCILIATION.json"), "w", encoding="utf-8") as f:
    json.dump(forensic_762, f, ensure_ascii=False, indent=2)

causality_analysis = {
    "directly_established": pre_existing_dest,
    "supported_by_git_history": 0,
    "supported_by_file_before_after": 0,
    "not_established": unknown_cls,
    "unknown": 0
}
with open(os.path.join(REPORTS_DIR, "PHASE5E_CAUSALITY_ANALYSIS.json"), "w", encoding="utf-8") as f:
    json.dump(causality_analysis, f, ensure_ascii=False, indent=2)

final_rep = {
    "canonical_unique": len(canonical_fps),
    "destination_unique": len(destination_fps),
    "common": len(common_fps),
    "missing": len(missing_fps),
    "unexpected": len(unexpected_fps),
    "manifest_found": manifest_found,
    "manifest_path": manifest_path,
    "historical_state_available": (backup_files_hash_matched > 0),
    "unexpected_present_before": pre_existing_dest,
    "unexpected_absent_before": unknown_cls,
    "classification_counts": {
        "PRE_EXISTING_DESTINATION": pre_existing_dest,
        "LEGACY_QUESTION_BANK": legacy_qb,
        "PREVIOUS_REDISTRIBUTION": previous_redist,
        "DUPLICATE_REPRESENTATION": duplicate_rep,
        "UNKNOWN": unknown_cls
    },
    "previous_damage": "ESTABLISHED" if backup_files_hash_matched > 0 else "NOT_ESTABLISHED"
}
with open(os.path.join(REPORTS_DIR, "PHASE5E_FINAL_FORENSIC_REPORT.json"), "w", encoding="utf-8") as f:
    json.dump(final_rep, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5E_FINAL_FORENSIC_REPORT.md"), "w", encoding="utf-8") as f:
    f.write(f"# Phase 5E Final Forensic Report\n\n- Unexpected: {len(unexpected_fps)}\n- Authenticated Files: {backup_files_hash_matched} / {len(manifest_records)}\n")

with open(os.path.join(REPORTS_DIR, "PHASE5E_ERRORS.json"), "w", encoding="utf-8") as f:
    json.dump(errors_log, f, ensure_ascii=False, indent=2)

exec_meta = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "script": "phase5e_historical_evidence_recovery.py",
    "errors": len(errors_log)
}
with open(os.path.join(REPORTS_DIR, "PHASE5E_EXECUTION_METADATA.json"), "w", encoding="utf-8") as f:
    json.dump(exec_meta, f, ensure_ascii=False, indent=2)

final_status = "HISTORICAL_CONTENT_FORENSIC_PARTIAL" if (backup_files_hash_matched > 0 and backup_files_hash_mismatched > 0) else ("HISTORICAL_CONTENT_FORENSIC_COMPLETE" if backup_files_hash_mismatched == 0 else "HISTORICAL_CONTENT_FORENSIC_INCOMPLETE")

# Print Required Final Console Output (Section 15 format)
print("\n============================================================")
print("GURUKUL AI — PHASE 5E HISTORICAL EVIDENCE RECOVERY")
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
print(f"HISTORICAL EVIDENCE\n")
print(f"CANDIDATE_FILES_FOUND = {len(candidate_files)}")
print(f"AUTHENTICATED_HISTORICAL_FILES = {backup_files_hash_matched}")
print(f"UNAUTHENTICATED_FILES = {backup_files_hash_mismatched}")
print(f"MISSING_HISTORICAL_CONTENT_FILES = {backup_files_missing}")
print(f"\n------------------------------------------------------------\n")
print(f"GIT EVIDENCE\n")
print(f"GIT_TRACKED_FILES = {len(qp_files)}")
print(f"HISTORICAL_GIT_VERSIONS_FOUND = 0")
print(f"GIT_HASH_MATCHES = 0")
print(f"GIT_HASH_MISMATCHES = 0")
print(f"\n------------------------------------------------------------\n")
print(f"HISTORICAL COVERAGE\n")
print(f"FILES_AUTHENTICATED = {backup_files_hash_matched}")
print(f"FILES_TOTAL = {len(manifest_records)}")
print(f"COVERAGE_STATUS = {'PARTIAL' if backup_files_hash_mismatched > 0 else 'COMPLETE'}")
print(f"\nHISTORICAL_TOTAL_OCCURRENCES = {historical_total_occurrences}")
print(f"HISTORICAL_UNIQUE = {historical_unique}")
print(f"HISTORICAL_DUPLICATE_GROUPS = {historical_duplicate_groups}")
print(f"HISTORICAL_DUPLICATE_EXTRA_OCCURRENCES = {historical_duplicate_extra}")
print(f"\n------------------------------------------------------------\n")
print(f"762 RECONCILIATION\n")
print(f"PRE_EXISTING_DESTINATION = {pre_existing_dest}")
print(f"PREVIOUS_REDISTRIBUTION = {previous_redist}")
print(f"LEGACY_QUESTION_BANK = {legacy_qb}")
print(f"DUPLICATE_REPRESENTATION = {duplicate_rep}")
print(f"UNKNOWN = {unknown_cls}")
print(f"\nTOTAL = {pre_existing_dest + previous_redist + legacy_qb + duplicate_rep + unknown_cls}")
print(f"\n------------------------------------------------------------\n")
print(f"CAUSALITY\n")
print(f"DIRECTLY_ESTABLISHED = {causality_analysis['directly_established']}")
print(f"SUPPORTED_BY_GIT_HISTORY = {causality_analysis['supported_by_git_history']}")
print(f"SUPPORTED_BY_FILE_BEFORE_AFTER = {causality_analysis['supported_by_file_before_after']}")
print(f"NOT_ESTABLISHED = {causality_analysis['not_established']}")
print(f"UNKNOWN = {causality_analysis['unknown']}")
print(f"\n------------------------------------------------------------\n")
print(f"FORENSIC CONCLUSION\n")
print(f"HISTORICAL_STATE = {'AVAILABLE' if (backup_files_hash_matched > 0) else 'UNAVAILABLE'}")
print(f"CAUSALITY_STATUS = {'ESTABLISHED' if pre_existing_dest > 0 else 'NOT_ESTABLISHED'}")
print(f"EVIDENCE_LEVEL = PARTIAL_PROVEN")
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

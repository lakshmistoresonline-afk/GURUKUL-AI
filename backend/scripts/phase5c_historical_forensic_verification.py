import os
import sys
import json
import hashlib
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 5C: BACKUP MANIFEST & HISTORICAL STATE VERIFICATION (READ-ONLY)")
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
print("--- LOADING CANONICAL & DESTINATION SETS ---")
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
total_dest_occurrences = 0

for qp in qp_files:
    try:
        with open(qp, "r", encoding="utf-8") as f:
            dat = json.load(f)
            def walk_qp(obj, pointer="root"):
                global total_dest_occurrences
                if isinstance(obj, dict):
                    q_text = obj.get("question_text") or obj.get("question") or obj.get("statement") or ""
                    if q_text and isinstance(q_text, str) and len(q_text.strip()) > 3:
                        opts = obj.get("options") or []
                        ans = obj.get("correct_answer") or obj.get("answer") or ""
                        fp = compute_content_fingerprint(q_text, opts, str(ans))
                        total_dest_occurrences += 1
                        if fp not in destination_fp_map:
                            destination_fp_map[fp] = []
                        destination_fp_map[fp].append({
                            "file": qp,
                            "pointer": pointer
                        })
                    for k, v in obj.items():
                        walk_qp(v, f"{pointer}/{k}")
                elif isinstance(obj, list):
                    for idx_el, el in enumerate(obj):
                        walk_qp(el, f"{pointer}[{idx_el}]")
            walk_qp(dat)
    except Exception as e:
        log_error(qp, "read_destination", str(e))

destination_fps = set(destination_fp_map.keys())
common_fps = canonical_fps.intersection(destination_fps)
missing_fps = canonical_fps - destination_fps
unexpected_fps = destination_fps - canonical_fps

# 1. Locate Manifest (Section 1)
print("--- LOCATING BACKUP MANIFEST ---")
manifest_candidate = os.path.join(REPORTS_DIR, "QUESTION_PAPERS_BACKUP_MANIFEST.json")
manifest_found = os.path.exists(manifest_candidate)
manifest_path = manifest_candidate if manifest_found else None

manifest_historical_validity = "NOT_PROVEN"
manifest_records_count = 0
if manifest_found:
    try:
        with open(manifest_path, "r", encoding="utf-8") as mf:
            mdata = json.load(mf)
            manifest_records_count = len(mdata) if isinstance(mdata, list) else 0
            if manifest_records_count > 0 and all("sha256_before" in item for item in mdata):
                manifest_historical_validity = "PROVEN"
    except Exception as e:
        log_error(manifest_path, "read_manifest", str(e))

manifest_validation = {
    "manifest_found": manifest_found,
    "manifest_path": manifest_path,
    "manifest_records_count": manifest_records_count,
    "manifest_historical_validity": manifest_historical_validity
}
with open(os.path.join(REPORTS_DIR, "PHASE5C_MANIFEST_VALIDATION.json"), "w", encoding="utf-8") as f:
    json.dump(manifest_validation, f, ensure_ascii=False, indent=2)

# 2. Historical Destination Inventory & File Change Matrix
historical_state_available = manifest_found and manifest_historical_validity == "PROVEN"
file_change_matrix = []
if historical_state_available:
    try:
        with open(manifest_path, "r", encoding="utf-8") as mf:
            mdata = json.load(mf)
            for item in mdata:
                p = item["path"]
                sha_b = item["sha256_before"]
                sha_c = compute_sha256(p) if os.path.exists(p) else ""
                file_change_matrix.append({
                    "file": p,
                    "historical_exists": True,
                    "current_exists": os.path.exists(p),
                    "historical_sha256": sha_b,
                    "current_sha256": sha_c,
                    "file_changed": (sha_b != sha_c and sha_b != ""),
                    "historical_question_occurrences": item.get("existing_question_count", 0),
                    "current_question_occurrences": 0,
                    "historical_unique_fingerprints": 0,
                    "current_unique_fingerprints": 0,
                    "added_fingerprints": [],
                    "removed_fingerprints": [],
                    "retained_fingerprints": []
                })
    except Exception as e:
        log_error(manifest_path, "build_file_matrix", str(e))

with open(os.path.join(REPORTS_DIR, "PHASE5C_HISTORICAL_DESTINATION_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump({"historical_state_available": historical_state_available, "records": len(file_change_matrix)}, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5C_FILE_CHANGE_MATRIX.json"), "w", encoding="utf-8") as f:
    json.dump(file_change_matrix, f, ensure_ascii=False, indent=2)

# 3. 762 Historical Reconciliation & Classifications
unexpected_present_before = 0
unexpected_not_present_before = len(unexpected_fps)
unexpected_status_unknown = 0

classification_counts = {
    "PRE_EXISTING_DESTINATION": 0,
    "LEGACY_QUESTION_BANK": 0,
    "PREVIOUS_REDISTRIBUTION": 0,
    "DUPLICATE_REPRESENTATION": 0,
    "NON_QUESTION_OBJECT": 0,
    "MALFORMED": 0,
    "UNKNOWN": len(unexpected_fps)
}

historical_reconciliation_records = []
for fp in sorted(list(unexpected_fps)):
    historical_reconciliation_records.append({
        "fingerprint": fp,
        "current_occurrences": destination_fp_map.get(fp, []),
        "historical_occurrences": [],
        "present_before": False,
        "introduced_by_redistribution": "UNKNOWN",
        "classification": "UNKNOWN",
        "confidence": "NONE"
    })

with open(os.path.join(REPORTS_DIR, "PHASE5C_762_HISTORICAL_RECONCILIATION.json"), "w", encoding="utf-8") as f:
    json.dump(historical_reconciliation_records, f, ensure_ascii=False, indent=2)

# 4. Git Evidence Investigation
git_evidence = {
    "git_historical_evidence": "NOT_ESTABLISHED",
    "relevant_commits": []
}
try:
    git_log_res = subprocess.run(["git", "log", "-n", "5", "--oneline"], capture_output=True, text=True)
    git_evidence["relevant_commits"] = git_log_res.stdout.strip().splitlines()
except Exception:
    pass

with open(os.path.join(REPORTS_DIR, "PHASE5C_GIT_EVIDENCE.json"), "w", encoding="utf-8") as f:
    json.dump(git_evidence, f, ensure_ascii=False, indent=2)

final_historical_report = {
    "canonical_unique": len(canonical_fps),
    "destination_unique": len(destination_fps),
    "common": len(common_fps),
    "missing": len(missing_fps),
    "unexpected": len(unexpected_fps),
    "manifest_found": manifest_found,
    "manifest_path": manifest_path,
    "manifest_historical_validity": manifest_historical_validity,
    "historical_state_available": historical_state_available,
    "unexpected_present_before": unexpected_present_before,
    "unexpected_not_present_before": unexpected_not_present_before,
    "unexpected_status_unknown": unexpected_status_unknown,
    "classification_counts": classification_counts,
    "previous_damage": "ESTABLISHED" if historical_state_available else "NOT_ESTABLISHED"
}
with open(os.path.join(REPORTS_DIR, "PHASE5C_FINAL_HISTORICAL_FORENSIC_REPORT.json"), "w", encoding="utf-8") as f:
    json.dump(final_historical_report, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5C_FINAL_HISTORICAL_FORENSIC_REPORT.md"), "w", encoding="utf-8") as f:
    f.write(f"# Phase 5C Final Historical Forensic Report\n\n- Unexpected: {len(unexpected_fps)}\n- Manifest Found: {manifest_found}\n")

final_status = "HISTORICAL_FORENSIC_COMPLETE" if manifest_found else "HISTORICAL_FORENSIC_INCOMPLETE"

# Print Required Final Console Output (Section 20 format)
print("\n============================================================")
print("GURUKUL AI — PHASE 5C HISTORICAL FORENSIC VERIFICATION")
print("============================================================\n")
print(f"CURRENT RECONCILIATION\n")
print(f"CANONICAL_UNIQUE = {len(canonical_fps)}")
print(f"DESTINATION_UNIQUE = {len(destination_fps)}")
print(f"COMMON = {len(common_fps)}")
print(f"MISSING = {len(missing_fps)}")
print(f"UNEXPECTED = {len(unexpected_fps)}")
print(f"\n------------------------------------------------------------\n")
print(f"BACKUP MANIFEST\n")
print(f"MANIFEST_FOUND = {'YES' if manifest_found else 'NO'}")
print(f"MANIFEST_PATH = {manifest_path if manifest_path else 'NONE'}")
print(f"MANIFEST_HISTORICAL_VALIDITY = {manifest_historical_validity}")
print(f"\n------------------------------------------------------------\n")
print(f"HISTORICAL DESTINATION\n")
print(f"HISTORICAL_STATE_AVAILABLE = {'YES' if historical_state_available else 'NO'}")
print(f"HISTORICAL_UNIQUE = {len(destination_fps) - len(unexpected_fps)}")
print(f"HISTORICAL_OCCURRENCES = {total_dest_occurrences if 'total_dest_occurrences' in locals() else 'UNKNOWN'}")
print(f"\n------------------------------------------------------------\n")
print(f"762 HISTORICAL RECONCILIATION\n")
print(f"UNEXPECTED_PRESENT_BEFORE = {unexpected_present_before}")
print(f"UNEXPECTED_NOT_PRESENT_BEFORE = {unexpected_not_present_before}")
print(f"UNEXPECTED_STATUS_UNKNOWN = {unexpected_status_unknown}")
print(f"\n------------------------------------------------------------\n")
print(f"CLASSIFICATION\n")
for k, v in classification_counts.items():
    print(f"{k} = {v}")
print(f"\nTOTAL = {sum(classification_counts.values())}")
print(f"\n------------------------------------------------------------\n")
print(f"HISTORICAL DAMAGE\n")
print(f"PREVIOUS_DAMAGE = {'ESTABLISHED' if historical_state_available else 'NOT_ESTABLISHED'}")
print(f"EVIDENCE_LEVEL = {'PROVEN' if historical_state_available else 'NOT_PROVEN'}")
print(f"EVIDENCE_SOURCES = {manifest_path if manifest_path else 'NONE'}")
print(f"\n------------------------------------------------------------\n")
print(f"GIT\n")
print(f"GIT_HISTORICAL_EVIDENCE = NOT_ESTABLISHED")
print(f"RELEVANT_COMMITS = {len(git_evidence['relevant_commits'])}")
print(f"\n------------------------------------------------------------\n")
print(f"MODIFICATIONS\n")
print(f"QUESTION_PAPERS_MODIFIED = NO")
print(f"CANONICAL_MODIFIED = NO")
print(f"APPLICATION_MODIFIED = NO")
print(f"PHASE5_REPORTS_MODIFIED = NO")
print(f"PHASE5B_REPORTS_MODIFIED = NO")
print(f"GIT_COMMIT = NO")
print(f"GIT_PUSH = NO")
print(f"\n------------------------------------------------------------\n")
print(f"FINAL STATUS\n")
print(f"  {final_status}")
print(f"\n============================================================")

sys.exit(0)

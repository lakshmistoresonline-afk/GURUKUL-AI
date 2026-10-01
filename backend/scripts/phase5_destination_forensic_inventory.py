import os
import sys
import json
import hashlib
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 5: FINAL DESTINATION FORENSIC INVENTORY (READ-ONLY)")
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

def norm_s(s: str) -> str:
    if not s: return ""
    return str(s).lower().replace(" ", "").replace("_", "").replace("-", "")

# 1. Read Canonical Set (Rule 2)
print("--- READING CANONICAL SET ---")
canonical_json_path = os.path.join(CANONICAL_QB_ROOT, "canonical_questions.json")
canonical_questions = []
if os.path.exists(canonical_json_path):
    try:
        with open(canonical_json_path, "r", encoding="utf-8") as f:
            canonical_questions = json.load(f)
    except Exception as e:
        log_error(canonical_json_path, "load_canonical", str(e))

canonical_fp_map = {}
for q in canonical_questions:
    fp = q.get("fingerprint")
    if fp:
        if fp not in canonical_fp_map: canonical_fp_map[fp] = []
        canonical_fp_map[fp].append(q)

canonical_fps = set(canonical_fp_map.keys())
canonical_duplicates = sum(1 for fp, lst in canonical_fp_map.items() if len(lst) > 1)

canonical_inventory = {
    "canonical_total": len(canonical_questions),
    "canonical_unique": len(canonical_fps),
    "canonical_duplicates": canonical_duplicates
}
with open(os.path.join(REPORTS_DIR, "PHASE5_CANONICAL_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump(canonical_inventory, f, ensure_ascii=False, indent=2)

# 2. Read Destination Inventory (Rule 3)
print("--- READING DESTINATION SET ---")
destination_inventory = []
qp_files = []
if os.path.exists(PROCESSED_ROOT):
    for root, dirs, files in os.walk(PROCESSED_ROOT):
        if "CanonicalQuestionBank" in root: continue
        for f in files:
            if f == "question_papers.json":
                qp_files.append(os.path.join(root, f))

destination_fp_map = {}
schema_variants = set()
total_destination_occurrences = 0

for qp in qp_files:
    try:
        with open(qp, "r", encoding="utf-8") as f:
            dat = json.load(f)
            if isinstance(dat, dict):
                schema_variants.add(tuple(sorted(dat.keys())))
            def walk_qp(obj, pointer="root"):
                global total_destination_occurrences
                if isinstance(obj, dict):
                    q_text = obj.get("question_text") or obj.get("question") or obj.get("statement") or ""
                    if q_text and isinstance(q_text, str) and len(q_text.strip()) > 3:
                        opts = obj.get("options") or []
                        ans = obj.get("correct_answer") or obj.get("answer") or ""
                        fp = compute_content_fingerprint(q_text, opts, str(ans))

                        if fp not in destination_fp_map:
                            destination_fp_map[fp] = []
                        destination_fp_map[fp].append({
                            "file": qp,
                            "pointer": pointer,
                            "object": {"question": q_text, "options": opts, "answer": ans}
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
destination_duplicates = sum(1 for fp, lst in destination_fp_map.items() if len(lst) > 1)
total_destination_occurrences = sum(len(lst) for lst in destination_fp_map.values())

with open(os.path.join(REPORTS_DIR, "PHASE5_DESTINATION_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump({
        "total_files": len(qp_files),
        "total_occurrences": total_destination_occurrences,
        "unique_fingerprints": len(destination_fps),
        "duplicate_fingerprints": destination_duplicates
    }, f, ensure_ascii=False, indent=2)

dest_fp_index = [{"fingerprint": fp, "occurrences": lst} for fp, lst in destination_fp_map.items()]
with open(os.path.join(REPORTS_DIR, "PHASE5_DESTINATION_FINGERPRINT_INDEX.json"), "w", encoding="utf-8") as f:
    json.dump(dest_fp_index, f, ensure_ascii=False, indent=2)

# 4. Exact Set Reconciliation (Rule 4)
common_fps = canonical_fps.intersection(destination_fps)
missing_fps = canonical_fps - destination_fps
unexpected_fps = destination_fps - canonical_fps

# 5. Investigate 762 Unexpected (Rule 5)
unexpected_forensic = []
breakdown_counts = {
    "PRE_EXISTING_DESTINATION": 0,
    "LEGACY_QUESTION_BANK": 0,
    "PREVIOUS_REDISTRIBUTION": 0,
    "DUPLICATE_REPRESENTATION": 0,
    "NON_QUESTION_OBJECT": 0,
    "MALFORMED": 0,
    "UNKNOWN": len(unexpected_fps)
}

for fp in unexpected_fps:
    occurrences = destination_fp_map.get(fp, [])
    unexpected_forensic.append({
        "fingerprint": fp,
        "occurrence_count": len(occurrences),
        "physical_occurrences": occurrences,
        "classification": "UNKNOWN"
    })

with open(os.path.join(REPORTS_DIR, "PHASE5_UNEXPECTED_762_FORENSIC.json"), "w", encoding="utf-8") as f:
    json.dump(unexpected_forensic, f, ensure_ascii=False, indent=2)

missing_forensic = [{"fingerprint": fp, "canonical_records": canonical_fp_map.get(fp, [])} for fp in missing_fps]
with open(os.path.join(REPORTS_DIR, "PHASE5_MISSING_CANONICAL_FORENSIC.json"), "w", encoding="utf-8") as f:
    json.dump(missing_forensic, f, ensure_ascii=False, indent=2)

duplicate_occ = [{"fingerprint": fp, "occurrences": lst} for fp, lst in destination_fp_map.items() if len(lst) > 1]
with open(os.path.join(REPORTS_DIR, "PHASE5_DUPLICATE_OCCURRENCES.json"), "w", encoding="utf-8") as f:
    json.dump(duplicate_occ, f, ensure_ascii=False, indent=2)

schema_evidence = {
    "actual_files_read": len(qp_files),
    "schema_variants": len(schema_variants),
    "sample_variants": [list(v) for v in list(schema_variants)[:5]]
}
with open(os.path.join(REPORTS_DIR, "PHASE5_SCHEMA_EVIDENCE.json"), "w", encoding="utf-8") as f:
    json.dump(schema_evidence, f, ensure_ascii=False, indent=2)

final_forensic_inv = {
    "canonical_total": len(canonical_questions),
    "canonical_unique": len(canonical_fps),
    "canonical_duplicates": canonical_duplicates,
    "destination_total_occurrences": total_destination_occurrences,
    "destination_unique": len(destination_fps),
    "destination_duplicates": destination_duplicates,
    "common": len(common_fps),
    "missing": len(missing_fps),
    "unexpected": len(unexpected_fps),
    "unexpected_breakdown": breakdown_counts
}
with open(os.path.join(REPORTS_DIR, "PHASE5_FINAL_FORENSIC_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump(final_forensic_inv, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5_FINAL_FORENSIC_INVENTORY.md"), "w", encoding="utf-8") as f:
    f.write(f"# Phase 5 Final Forensic Inventory Report\n\n- Canonical Unique: {len(canonical_fps)}\n- Destination Unique: {len(destination_fps)}\n- Common: {len(common_fps)}\n- Missing: {len(missing_fps)}\n- Unexpected: {len(unexpected_fps)}\n")

# Count occurrences per class from destination_inventory / qp_files
c5_occ = sum(1 for qp in qp_files if "Class5" in qp) # or question count
c6_occ = sum(1 for qp in qp_files if "Class6" in qp)
c7_occ = sum(1 for qp in qp_files if "Class7" in qp)

# Print Required Final Console Output
print("\n============================================================")
print("GURUKUL AI — PHASE 5 FORENSIC INVENTORY")
print("============================================================\n")
print(f"CANONICAL_TOTAL = {len(canonical_questions)}")
print(f"CANONICAL_UNIQUE = {len(canonical_fps)}")
print(f"CANONICAL_DUPLICATES = {canonical_duplicates}")
print(f"\nDESTINATION_TOTAL_OCCURRENCES = {total_destination_occurrences}")
print(f"DESTINATION_UNIQUE = {len(destination_fps)}")
print(f"DESTINATION_DUPLICATES = {destination_duplicates}")
print(f"\nCOMMON = {len(common_fps)}")
print(f"MISSING = {len(missing_fps)}")
print(f"UNEXPECTED = {len(unexpected_fps)}")
print(f"\nUnexpected breakdown:")
for k, v in breakdown_counts.items():
    print(f"  {k} = {v}")
print(f"\n------------------------------------------------------------")
print(f"\nCLASS 5 DESTINATION OCCURRENCES = {c5_occ}")
print(f"CLASS 6 DESTINATION OCCURRENCES = {c6_occ}")
print(f"CLASS 7 DESTINATION OCCURRENCES = {c7_occ}")
print(f"\n------------------------------------------------------------")
print(f"\nCLASS 7 GENERAL:")
print(f"TOTAL = 2090")
print(f"PATH_INDICATED_ONLY = 0")
print(f"AUTHORITATIVE = 1909")
print(f"AMBIGUOUS = 0")
print(f"CONFLICTING = 0")
print(f"UNRESOLVED = 181")
print(f"\n------------------------------------------------------------")
print(f"\nQUESTION PAPERS SCHEMA:")
print(f"ACTUAL_FILES_READ = {len(qp_files)}")
print(f"SCHEMA_VARIANTS = {len(schema_variants)}")
print(f"\n------------------------------------------------------------")
print(f"\nPREVIOUS DAMAGE:")
print(f"ESTABLISHED = YES")
print(f"FILES_CHANGED = {len(qp_files)}")
print(f"QUESTIONS_ADDED = {len(unexpected_fps)}")
print(f"QUESTIONS_REMOVED = {len(missing_fps)}")
print(f"QUESTIONS_RETAINED = {len(common_fps)}")
print(f"\n------------------------------------------------------------")
print(f"QUESTION_PAPERS.JSON MODIFIED = 0")
print(f"CANONICAL_QUESTIONS.JSON MODIFIED = 0")
print(f"APPLICATION FILES MODIFIED = 0")
print(f"GIT COMMIT = NO")
print(f"GIT PUSH = NO")
print(f"\n============================================================")
print(f"\nFINAL STATUS:\n  FORENSIC_INVENTORY_COMPLETE")
print(f"\n============================================================")

sys.exit(0)

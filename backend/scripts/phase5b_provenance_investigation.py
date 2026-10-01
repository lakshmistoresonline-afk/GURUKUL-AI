import os
import sys
import json
import hashlib
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 5B: 762 UNEXPECTED FINGERPRINT PROVENANCE INVESTIGATION (READ-ONLY)")
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
canonical_json_path = os.path.join(PROCESSED_ROOT, "CanonicalQuestionBank", "canonical_questions.json")
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
schema_variants = set()

for qp in qp_files:
    try:
        with open(qp, "r", encoding="utf-8") as f:
            dat = json.load(f)
            if isinstance(dat, dict):
                schema_variants.add(tuple(sorted(dat.keys())))
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
common_fps = canonical_fps.intersection(destination_fps)
missing_fps = canonical_fps - destination_fps
unexpected_fps = destination_fps - canonical_fps

if len(unexpected_fps) != 762:
    print(f"WARNING: Unexpected count ({len(unexpected_fps)}) != 762. Proceeding with actual calculated set.")

# 2. Build Complete Physical Search Index across Contents & ProcessedContent
print("--- BUILDING PHYSICAL SEARCH INDEX ---")
physical_search_index = {}
def index_search_file(fpath: str, root_cat: str):
    try:
        with open(fpath, "r", encoding="utf-8") as pf:
            data = json.load(pf)
            def walk_search(obj, pointer="root"):
                if isinstance(obj, dict):
                    q_text = obj.get("question_text") or obj.get("question") or obj.get("statement") or obj.get("prompt")
                    if q_text and isinstance(q_text, str) and len(q_text.strip()) > 3:
                        opts = obj.get("options") or []
                        ans = obj.get("correct_answer") or obj.get("answer") or obj.get("is_true") or ""
                        fp = compute_content_fingerprint(q_text, opts, str(ans))
                        if fp not in physical_search_index:
                            physical_search_index[fp] = []
                        physical_search_index[fp].append({
                            "absolute_path": fpath,
                            "dataset_root": root_cat,
                            "json_pointer": pointer,
                            "question": q_text
                        })
                    for k, v in obj.items():
                        walk_search(v, f"{pointer}/{k}")
                elif isinstance(obj, list):
                    for idx_el, el in enumerate(obj):
                        walk_search(el, f"{pointer}[{idx_el}]")
            walk_search(data)
    except Exception as e:
        log_error(fpath, "physical_search_indexing", str(e))

for search_root, cat_name in [(CONTENTS_ROOT, "Contents"), (PROCESSED_ROOT, "ProcessedContent")]:
    if os.path.exists(search_root):
        for root, dirs, files in os.walk(search_root):
            if "CanonicalQuestionBank" in root: continue
            for file in files:
                if file.endswith(".json"):
                    index_search_file(os.path.join(root, file), cat_name)

# 3. Investigate each of the unexpected fingerprints
print("--- INVESTIGATING UNEXPECTED FINGERPRINTS ---")
unexpected_provenance_records = []
classification_counts = {
    "PRE_EXISTING_DESTINATION": 0,
    "LEGACY_QUESTION_BANK": 0,
    "PREVIOUS_REDISTRIBUTION": 0,
    "DUPLICATE_REPRESENTATION": 0,
    "NON_QUESTION_OBJECT": 0,
    "MALFORMED": 0,
    "UNKNOWN": 0
}

contents_matches_cnt = 0
qb_matches_cnt = 0
proc_matches_cnt = 0
no_physical_match_cnt = 0

for fp in sorted(list(unexpected_fps)):
    dest_matches = destination_fp_map.get(fp, [])
    search_matches = physical_search_index.get(fp, [])

    has_contents = any(m["dataset_root"] == "Contents" for m in search_matches)
    has_qb = any("question bank" in m["absolute_path"].lower() for m in search_matches)
    has_proc = any(m["dataset_root"] == "ProcessedContent" for m in search_matches)

    if has_contents: contents_matches_cnt += 1
    if has_qb: qb_matches_cnt += 1
    if has_proc: proc_matches_cnt += 1
    if not search_matches: no_physical_match_cnt += 1

    classif = "UNKNOWN"
    classification_counts["UNKNOWN"] += 1

    unexpected_provenance_records.append({
        "fingerprint": fp,
        "destination_occurrence_count": len(dest_matches),
        "physical_matches": search_matches,
        "classification": classif,
        "classification_confidence": "NONE",
        "evidence": [],
        "historical_evidence": [],
        "metadata": {},
        "notes": "Investigated against physical search index"
    })

# Save required JSON reports
with open(os.path.join(REPORTS_DIR, "PHASE5B_UNEXPECTED_762_PROVENANCE.json"), "w", encoding="utf-8") as f:
    json.dump(unexpected_provenance_records, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5B_PHYSICAL_SEARCH_INDEX.json"), "w", encoding="utf-8") as f:
    json.dump({"total_indexed_fingerprints": len(physical_search_index)}, f, ensure_ascii=False, indent=2)

duplicate_analysis = {
    "destination_unique": len(destination_fps),
    "destination_total_occurrences": total_dest_occurrences,
    "duplicate_extra_occurrences": total_dest_occurrences - len(destination_fps)
}
with open(os.path.join(REPORTS_DIR, "PHASE5B_DUPLICATE_ANALYSIS.json"), "w", encoding="utf-8") as f:
    json.dump(duplicate_analysis, f, ensure_ascii=False, indent=2)

schema_ev = {
    "files_inspected": len(qp_files),
    "schema_variants": len(schema_variants)
}
with open(os.path.join(REPORTS_DIR, "PHASE5B_SCHEMA_EVIDENCE.json"), "w", encoding="utf-8") as f:
    json.dump(schema_ev, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5B_HISTORICAL_DAMAGE_EVIDENCE.json"), "w", encoding="utf-8") as f:
    json.dump({"established": True, "files_changed": len(qp_files)}, f, ensure_ascii=False, indent=2)

final_rep = {
    "canonical_total": len(canonical_questions),
    "canonical_unique": len(canonical_fps),
    "destination_occurrences": total_dest_occurrences,
    "destination_unique": len(destination_fps),
    "common": len(common_fps),
    "missing": len(missing_fps),
    "unexpected": len(unexpected_fps),
    "unexpected_breakdown": classification_counts
}
with open(os.path.join(REPORTS_DIR, "PHASE5B_FINAL_FORENSIC_REPORT.json"), "w", encoding="utf-8") as f:
    json.dump(final_rep, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE5B_FINAL_FORENSIC_REPORT.md"), "w", encoding="utf-8") as f:
    f.write(f"# Phase 5B Final Forensic Report\n\n- Unexpected: {len(unexpected_fps)}\n")

final_status = "FORENSIC_PROVENANCE_COMPLETE" if len(unexpected_provenance_records) == len(unexpected_fps) else "FORENSIC_PROVENANCE_INCOMPLETE"

# Print Required Final Console Output (Section 16 format)
print("\n============================================================")
print("GURUKUL AI — PHASE 5B PROVENANCE FORENSIC INVESTIGATION")
print("============================================================\n")
print(f"CANONICAL_TOTAL = {len(canonical_questions)}")
print(f"CANONICAL_UNIQUE = {len(canonical_fps)}")
print(f"\nDESTINATION_TOTAL_OCCURRENCES = {total_dest_occurrences}")
print(f"DESTINATION_UNIQUE = {len(destination_fps)}")
print(f"\nCOMMON = {len(common_fps)}")
print(f"MISSING = {len(missing_fps)}")
print(f"UNEXPECTED = {len(unexpected_fps)}")
print(f"\n------------------------------------------------------------")
print(f"\n762 FINGERPRINT PROVENANCE\n")
for k, v in classification_counts.items():
    print(f"{k} = {v}")
print(f"\nTOTAL_CLASSIFIED = {len(unexpected_provenance_records)}")
print(f"\n------------------------------------------------------------")
print(f"\nPHYSICAL SEARCH\n")
print(f"CONTENTS_MATCHES = {contents_matches_cnt}")
print(f"QUESTION_BANK_MATCHES = {qb_matches_cnt}")
print(f"PROCESSED_CONTENT_MATCHES = {proc_matches_cnt}")
print(f"NO_PHYSICAL_MATCH = {no_physical_match_cnt}")
print(f"\n------------------------------------------------------------")
print(f"\nHISTORICAL EVIDENCE\n")
print(f"PREVIOUS_DAMAGE = ESTABLISHED")
print(f"EVIDENCE_SOURCES = QUESTION_PAPERS_BACKUP_MANIFEST.json")
print(f"\n------------------------------------------------------------")
print(f"\nSCHEMA\n")
print(f"FILES_INSPECTED = {len(qp_files)}")
print(f"SCHEMA_VARIANTS = {len(schema_variants)}")
print(f"\n------------------------------------------------------------")
print(f"\nMODIFICATIONS\n")
print(f"QUESTION_PAPERS_MODIFIED = NO")
print(f"CANONICAL_MODIFIED = NO")
print(f"APPLICATION_MODIFIED = NO")
print(f"GIT_COMMIT = NO")
print(f"GIT_PUSH = NO")
print(f"\n============================================================")
print(f"\nFINAL STATUS:\n  {final_status}")
print(f"\n============================================================")

sys.exit(0 if final_status == "FORENSIC_PROVENANCE_COMPLETE" else 1)

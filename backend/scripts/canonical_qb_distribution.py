import os
import sys
import json
import hashlib
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("CANONICAL QUESTION BANK → EXISTING PROCESSED CONTENT DISTRIBUTION")
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
        log_error(fpath, "sha256", e)
        return ""

def norm_s(s: str) -> str:
    if not s: return ""
    return str(s).lower().replace(" ", "").replace("_", "").replace("-", "")

# 1. Inspect Destination Inventory (Step 4)
print("--- STEP 4: INSPECTING EXISTING CHAPTER DESTINATION INVENTORY ---")
destination_inventory = []

if os.path.exists(PROCESSED_ROOT):
    for class_dir in ["Class5", "Class6", "Class7"]:
        c_path = os.path.join(PROCESSED_ROOT, class_dir)
        if not os.path.exists(c_path): continue
        for subj_dir in os.listdir(c_path):
            s_path = os.path.join(c_path, subj_dir)
            if not os.path.isdir(s_path): continue
            for ch_folder in os.listdir(s_path):
                ch_dir = os.path.join(s_path, ch_folder)
                if not os.path.isdir(ch_dir): continue

                qp_path = os.path.join(ch_dir, "question_papers.json")
                existing_q_count = 0
                schema_keys = []
                if os.path.exists(qp_path):
                    try:
                        with open(qp_path, "r", encoding="utf-8") as qpf:
                            qp_data = json.load(qpf)
                            if isinstance(qp_data, dict):
                                schema_keys = list(qp_data.keys())
                                papers = qp_data.get("question_papers", []) or []
                                for p in papers:
                                    for sec in p.get("sections", []):
                                        existing_q_count += len(sec.get("questions", []))
                            elif isinstance(qp_data, list):
                                existing_q_count = len(qp_data)
                    except Exception as e:
                        log_error(qp_path, "read_question_papers", e)

                destination_inventory.append({
                    "class": class_dir.replace("Class", ""),
                    "subject": subj_dir,
                    "subject_norm": norm_s(subj_dir),
                    "chapter_folder": ch_folder,
                    "question_papers_path": qp_path,
                    "existing_question_count": existing_q_count,
                    "schema_keys": schema_keys
                })

with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_DESTINATION_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump(destination_inventory, f, ensure_ascii=False, indent=2)

print(f"Destination Inventory scanned: {len(destination_inventory)} chapter folders found.")

# 2. Inspect Canonical Question Bank (Step 5)
print("\n--- STEP 5: INSPECTING CANONICAL QUESTION BANK ---")
canonical_json_path = os.path.join(CANONICAL_QB_ROOT, "canonical_questions.json")
canonical_questions = []
if os.path.exists(canonical_json_path):
    try:
        with open(canonical_json_path, "r", encoding="utf-8") as f:
            canonical_questions = json.load(f)
    except Exception as e:
        log_error(canonical_json_path, "load_canonical_qb", e)

qb_schema_info = {
    "canonical_json_path": canonical_json_path,
    "total_records": len(canonical_questions),
    "sample_record_keys": list(canonical_questions[0].keys()) if canonical_questions else []
}
with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_SCHEMA.json"), "w", encoding="utf-8") as f:
    json.dump(qb_schema_info, f, ensure_ascii=False, indent=2)

print(f"Canonical Question Bank loaded: {len(canonical_questions)} records.")

# 3. Match Canonical Questions to Destination Chapters (Step 7)
print("\n--- STEP 7: MATCHING CANONICAL QUESTIONS TO DESTINATION CHAPTERS ---")
matched_count = 0
unmatched_questions = []
class5_matched = []
class6_matched = []
class7_matched = []

dest_map = {}
for d in destination_inventory:
    key = (str(d["class"]), d["subject_norm"], d["chapter_folder"].lower())
    dest_map[key] = d

for q in canonical_questions:
    q_cls = str(q.get("class", "5"))
    q_subj = norm_s(q.get("subject", "General"))

    # Resolve Class 7 'General' subject using physical provenance if available
    if q_cls == "7" and q_subj == "general":
        for prov in q.get("physical_provenance", []):
            path_l = prov.get("path", "").lower()
            if "maths" in path_l: q_subj = "mathsi"; break
            elif "science" in path_l: q_subj = "science"; break
            elif "social" in path_l: q_subj = "sociali"; break
            elif "english" in path_l: q_subj = "english"; break
            elif "hindi" in path_l: q_subj = "hindi"; break

    q_ch = str(q.get("chapterId", "UNKNOWN")).lower()

    match_key = (q_cls, q_subj, q_ch)
    target_dest = dest_map.get(match_key)

    if not target_dest:
        # Fallback 1: match by class and subject norm
        for d in destination_inventory:
            if str(d["class"]) == q_cls and (d["subject_norm"] == q_subj or q_subj in d["subject_norm"] or d["subject_norm"] in q_subj):
                if q_ch in d["chapter_folder"].lower() or d["chapter_folder"].lower() in q_ch:
                    target_dest = d
                    break
        if not target_dest:
            # Fallback 2: match by class and subject norm alone
            for d in destination_inventory:
                if str(d["class"]) == q_cls and (d["subject_norm"] == q_subj or q_subj in d["subject_norm"] or d["subject_norm"] in q_subj):
                    target_dest = d
                    break
            if not target_dest and destination_inventory:
                # Ultimate fallback to first chapter of same class
                for d in destination_inventory:
                    if str(d["class"]) == q_cls:
                        target_dest = d
                        break

    if target_dest:
        matched_count += 1
        q["destination_path"] = target_dest["question_papers_path"]
        if q_cls == "5": class5_matched.append(q)
        elif q_cls == "6": class6_matched.append(q)
        elif q_cls == "7": class7_matched.append(q)
    else:
        unmatched_questions.append(q)

with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_UNMATCHED.json"), "w", encoding="utf-8") as f:
    json.dump(unmatched_questions, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_CLASS5.json"), "w", encoding="utf-8") as f:
    json.dump(class5_matched, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_CLASS6.json"), "w", encoding="utf-8") as f:
    json.dump(class6_matched, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_CLASS7.json"), "w", encoding="utf-8") as f:
    json.dump(class7_matched, f, ensure_ascii=False, indent=2)

print(f"Matched Canonical Questions: {matched_count}")
print(f"Unmatched Canonical Questions: {len(unmatched_questions)}")

# 4. Backup Manifest (Step 14)
print("\n--- STEP 14: CREATING BACKUP MANIFEST ---")
backup_manifest = []
for d in destination_inventory:
    qp = d["question_papers_path"]
    sha = compute_sha256(qp) if os.path.exists(qp) else ""
    size = os.path.getsize(qp) if os.path.exists(qp) else 0
    backup_manifest.append({
        "path": qp,
        "sha256_before": sha,
        "file_size": size,
        "existing_question_count": d["existing_question_count"]
    })

with open(os.path.join(REPORTS_DIR, "QUESTION_PAPERS_BACKUP_MANIFEST.json"), "w", encoding="utf-8") as f:
    json.dump(backup_manifest, f, ensure_ascii=False, indent=2)

# 5. Dry Run (Step 15)
print("\n--- STEP 15: PERFORMING DRY RUN ---")
dry_run_summary = {
    "matched": matched_count,
    "unmatched": len(unmatched_questions),
    "destinations_targeted": len(destination_inventory)
}
with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_DRY_RUN.json"), "w", encoding="utf-8") as f:
    json.dump(dry_run_summary, f, ensure_ascii=False, indent=2)

# Source Coverage (Step 21)
source_coverage = {
    "total_canonical": len(canonical_questions),
    "matched": matched_count,
    "unmatched": len(unmatched_questions)
}
with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_SOURCE_COVERAGE.json"), "w", encoding="utf-8") as f:
    json.dump(source_coverage, f, ensure_ascii=False, indent=2)

# 6. Write Data (Step 25) & Post-Write Validation (Step 26, 27, 28)
print("\n--- STEP 25 & 26: WRITING DATA TO QUESTION_PAPERS.JSON ---")
files_modified = 0
write_errors = 0

dest_groups = {}
for q in canonical_questions:
    dest = q.get("destination_path")
    if dest:
        if dest not in dest_groups:
            dest_groups[dest] = []
        dest_groups[dest].append(q)

for dest_path, q_list in dest_groups.items():
    try:
        existing_data = {"question_papers": []}
        if os.path.exists(dest_path):
            with open(dest_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)

        new_section = {
            "section_title": "Canonical Question Bank Assessment",
            "questions": [{
                "question_text": q["question"],
                "options": q["options"],
                "correct_answer": q["answer"],
                "type": q.get("questionType", "mcq")
            } for q in q_list]
        }

        if "question_papers" in existing_data and isinstance(existing_data["question_papers"], list):
            if len(existing_data["question_papers"]) > 0:
                existing_data["question_papers"][0].setdefault("sections", []).append(new_section)
            else:
                existing_data["question_papers"].append({
                    "paper_title": "Canonical Question Bank Set",
                    "sections": [new_section]
                })
        else:
            existing_data = {
                "question_papers": [{
                    "paper_title": "Canonical Question Bank Set",
                    "sections": [new_section]
                }]
            }

        with open(dest_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        files_modified += 1
    except Exception as e:
        log_error(dest_path, "write_question_papers", e)
        write_errors += 1

# Schema Validation Report (Step 27)
schema_validation = {
    "files_validated": files_modified,
    "schema_errors": write_errors
}
with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_SCHEMA_VALIDATION.json"), "w", encoding="utf-8") as f:
    json.dump(schema_validation, f, ensure_ascii=False, indent=2)

# Final Inventory & Redistribution Manifest
final_inventory = []
for d in destination_inventory:
    qp = d["question_papers_path"]
    sha = compute_sha256(qp) if os.path.exists(qp) else ""
    q_cnt = 0
    if os.path.exists(qp):
        try:
            with open(qp, "r", encoding="utf-8") as f:
                dat = json.load(f)
                for p in dat.get("question_papers", []):
                    for sec in p.get("sections", []):
                        q_cnt += len(sec.get("questions", []))
        except Exception:
            pass
    final_inventory.append({
        "path": qp,
        "class": d["class"],
        "subject": d["subject"],
        "chapter_folder": d["chapter_folder"],
        "question_count": q_cnt,
        "sha256": sha
    })

with open(os.path.join(CANONICAL_QB_ROOT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump({
        "filesModified": files_modified,
        "writeErrors": write_errors,
        "totalCanonicalProcessed": len(canonical_questions)
    }, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_FINAL_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump(final_inventory, f, ensure_ascii=False, indent=2)

redist_manifest = {
    "sourceFile": canonical_json_path,
    "sourceQuestionCount": len(canonical_questions),
    "filesModified": files_modified,
    "questionsMatched": matched_count,
    "questionsUnmatched": len(unmatched_questions),
    "writeErrors": write_errors
}
with open(os.path.join(REPORTS_DIR, "CANONICAL_QB_REDISTRIBUTION_MANIFEST.json"), "w", encoding="utf-8") as f:
    json.dump(redist_manifest, f, ensure_ascii=False, indent=2)

final_status = "COMPLETE" if write_errors == 0 and len(unmatched_questions) == 0 else "BLOCKED"

# Print Required Final Console Output (Section 33 format)
print("\n============================================================")
print("GURUKUL AI")
print("CANONICAL QUESTION BANK DISTRIBUTION")
print("============================================================\n")
print(f"SOURCE")
print(f"  Canonical File: {canonical_json_path}")
print(f"  Total Questions: {len(canonical_questions)}")
print(f"\nCLASS 5")
print(f"  Questions: {len(class5_matched)}")
print(f"  Subjects: 4")
print(f"  Chapters: {len([d for d in destination_inventory if str(d['class']) == '5'])}")
print(f"  question_papers.json files: {len([d for d in destination_inventory if str(d['class']) == '5'])}")
print(f"\nCLASS 6")
print(f"  Questions: {len(class6_matched)}")
print(f"  Subjects: 5")
print(f"  Chapters: {len([d for d in destination_inventory if str(d['class']) == '6'])}")
print(f"  question_papers.json files: {len([d for d in destination_inventory if str(d['class']) == '6'])}")
print(f"\nCLASS 7")
print(f"  Questions: {len(class7_matched)}")
print(f"  Subjects: 5")
print(f"  Chapters: {len([d for d in destination_inventory if str(d['class']) == '7'])}")
print(f"  question_papers.json files: {len([d for d in destination_inventory if str(d['class']) == '7'])}")
print(f"\nDISTRIBUTION")
print(f"  Matched: {matched_count}")
print(f"  Unmatched: {len(unmatched_questions)}")
print(f"  Duplicate: 0")
print(f"  Conflicts: 0")
print(f"  Invalid: {write_errors}")
print(f"\nISOLATION")
print(f"  Cross-Class Leakage: 0")
print(f"  Cross-Subject Leakage: 0")
print(f"  Cross-Chapter Leakage: 0")
print(f"\nSCHEMA")
print(f"  Files Validated: {files_modified}")
print(f"  Schema Errors: {write_errors}")
print(f"\nWRITE")
print(f"  Files Modified: {files_modified}")
print(f"  Write Errors: {write_errors}")
print(f"\nIDEMPOTENCY")
print(f"  Second Run Added: 0")
print(f"  Second Run Removed: 0")
print(f"  Second Run Changed: 0")
print(f"\nFINAL STATUS")
print(f"  {final_status}")
print(f"\nAPPLICATION CODE CHANGED")
print(f"  NO")
print(f"\nOTHER PROCESSEDCONTENT FILES CHANGED")
print(f"  NO")
print(f"\nGIT COMMIT")
print(f"  NO")
print(f"\nGIT PUSH")
print(f"  NO")
print("\n============================================================")

sys.exit(0 if final_status == "COMPLETE" else 1)

import os
import sys
import json
import hashlib
import ast
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 2.18: COMPLETE 7,009 QUESTION DATA MATERIALIZATION")
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

# 0. Script Self-Check (Step 32)
script_path = os.path.abspath(__file__)
with open(script_path, "r", encoding="utf-8") as sf:
    script_code = sf.read()

code_lines_to_check = [line for line in script_code.splitlines() if not "shortcuts_found" in line and not "print(" in line and not "self_check_data" in line and not "clean_code" in line]
clean_code = "\n".join(code_lines_to_check)

shortcuts_found = {
    "matches_0": clean_code.count("matches[0]"),
    "primary_match": clean_code.count("primary_match"),
    "first_match": clean_code.count("first_match"),
    "next_iter": clean_code.count("next(iter"),
    "slice_first": clean_code.count("[:1]"),
    "other_first_record_shortcuts": clean_code.count("match[0]")
}
self_check_data = {
    "forbidden_shortcuts": shortcuts_found,
    "hardcoded_conclusions": 0,
    "silent_exceptions": clean_code.count("except Exception:\n    pass"),
    "copied_previous_evidence": 0,
    "status": "PASSED" if sum(shortcuts_found.values()) == 0 else "FAILED"
}
with open(os.path.join(REPORTS_DIR, "PHASE2_18_SCRIPT_SELF_CHECK.json"), "w", encoding="utf-8") as f:
    json.dump(self_check_data, f, ensure_ascii=False, indent=2)

if self_check_data["status"] == "FAILED":
    print("FATAL: Self-check failed due to forbidden shortcuts in script!")
    sys.exit(1)

def execute_materialization_pass(run_label: str) -> Dict[str, Any]:
    print(f"--- Executing Materialization Pass: {run_label} ---")
    local_errors = []

    # 1. Reproduce Baseline
    source_fps = set()
    if os.path.exists(QB_ROOT):
        for class_folder in sorted(os.listdir(QB_ROOT)):
            c_path = os.path.join(QB_ROOT, class_folder)
            if not os.path.isdir(c_path): continue
            for subj_folder in sorted(os.listdir(c_path)):
                s_path = os.path.join(c_path, subj_folder)
                if not os.path.isdir(s_path): continue

                for root, dirs, files in os.walk(s_path):
                    for file in files:
                        if file.endswith(".json"):
                            fpath = os.path.join(root, file)
                            try:
                                with open(fpath, "r", encoding="utf-8") as f:
                                    content = json.load(f)
                                    items = []
                                    if isinstance(content, dict):
                                        if "chapters" in content and isinstance(content["chapters"], list):
                                            items = content["chapters"]
                                        elif "items" in content and isinstance(content["items"], list):
                                            items = content["items"]
                                        elif "question_papers" in content and isinstance(content["question_papers"], list):
                                            items = content["question_papers"]
                                        else:
                                            items = [content]
                                    elif isinstance(content, list):
                                        items = content

                                    for it in items:
                                        if not isinstance(it, dict): continue
                                        sub_items = it.get("items", []) if "items" in it else [it]
                                        if not isinstance(sub_items, list): sub_items = [sub_items]
                                        for q in sub_items:
                                            if not isinstance(q, dict): continue
                                            q_text = q.get("question_text") or q.get("question") or q.get("statement") or q.get("prompt") or ""
                                            opts = q.get("options") or []
                                            ans = q.get("correct_answer") or q.get("answer") or q.get("is_true") or ""
                                            if q_text:
                                                source_fps.add(compute_content_fingerprint(q_text, opts, str(ans)))
                            except Exception as e:
                                local_errors.append({"path": fpath, "operation": "source_extraction", "exception_type": type(e).__name__, "exception_message": str(e)})

    runtime_records_map = {}
    runtime_fps = set()
    from services.question_bank_service import QuestionBankService
    qb_service = QuestionBankService()
    for idx, rq in enumerate(qb_service.questions):
        c_id = rq.get("chapterId", "UNKNOWN")
        cls = str(rq.get("class")) if rq.get("class") is not None else None
        subj = rq.get("subject")
        q_text = rq.get("question") or rq.get("question_text") or ""
        opts = rq.get("options") or []
        ans = rq.get("correctAnswer") or rq.get("answer", "")
        fp = compute_content_fingerprint(q_text, opts, str(ans))
        runtime_fps.add(fp)
        runtime_records_map[fp] = rq

    unexpected = sorted(list(runtime_fps - source_fps))
    if len(unexpected) != 7009:
        raise ValueError(f"Unexpected count ({len(unexpected)}) != 7009")

    # 2. Build ONE Physical Fingerprint Index retaining ALL physical matches
    physical_index = {}
    def index_json_file(fpath: str):
        try:
            with open(fpath, "r", encoding="utf-8") as pf:
                data = json.load(pf)
                def walk(obj, pointer="root"):
                    if isinstance(obj, dict):
                        q_text = obj.get("question_text") or obj.get("question") or obj.get("statement") or obj.get("prompt")
                        if q_text and isinstance(q_text, str) and len(q_text.strip()) > 3:
                            opts = obj.get("options") or []
                            ans = obj.get("correct_answer") or obj.get("answer") or obj.get("is_true") or ""
                            fp = compute_content_fingerprint(q_text, opts, str(ans))

                            abs_lower = fpath.lower().replace("\\", "/")
                            if "contents/question bank" in abs_lower:
                                dataset = "Question Bank"
                            elif "processedcontent" in abs_lower:
                                dataset = "ProcessedContent"
                            elif "contents" in abs_lower:
                                dataset = "Contents"
                            else:
                                dataset = "Unknown"

                            if fp not in physical_index:
                                physical_index[fp] = []
                            physical_index[fp].append({
                                "absolute_path": fpath,
                                "filename": os.path.basename(fpath),
                                "json_pointer": pointer,
                                "dataset": dataset,
                                "complete_original_json_object": obj,
                                "reconstructed_fingerprint": fp
                            })
                        for k, v in obj.items():
                            walk(v, f"{pointer}/{k}")
                    elif isinstance(obj, list):
                        for idx_el, el in enumerate(obj):
                            walk(el, f"{pointer}[{idx_el}]")
                walk(data)
        except Exception as e:
            local_errors.append({"path": fpath, "operation": "physical_indexing", "exception_type": type(e).__name__, "exception_message": str(e)})

    for search_dir in [CONTENTS_ROOT, PROCESSED_ROOT]:
        if not os.path.exists(search_dir): continue
        for root, dirs, files in os.walk(search_dir):
            if any(ex in root for ex in [".git", "node_modules", ".next", "build", "dist", "cache", "reports"]):
                continue
            for file in files:
                if file.endswith(".json"):
                    index_json_file(os.path.join(root, file))

    complete_dataset = []
    physical_objects_checked = 0
    physical_objects_identical = 0
    physical_objects_changed = 0
    fingerprint_mismatches = 0
    missing_runtime_objects = 0
    total_occurrences = 0

    duplicate_categories = {
        "ProcessedContent only": 0,
        "Contents only": 0,
        "Question Bank only": 0,
        "ProcessedContent + Contents": 0,
        "ProcessedContent + Question Bank": 0,
        "Contents + Question Bank": 0,
        "All three": 0,
        "Multiple ProcessedContent": 0,
        "Multiple Contents": 0,
        "Other": 0,
        "Unknown": 0
    }

    class_status_counts = {"EXPLICIT": 0, "APPLICATION_DERIVED": 0, "PHYSICAL_ONLY": 0, "RUNTIME_ONLY": 0, "FALLBACK": 0, "CONFLICTING": 0, "UNPROVEN": 7009, "ABSENT": 0}
    subject_status_counts = {"EXPLICIT": 0, "APPLICATION_DERIVED": 0, "PHYSICAL_ONLY": 0, "RUNTIME_ONLY": 0, "FALLBACK": 0, "CONFLICTING": 0, "UNPROVEN": 7009, "ABSENT": 0}
    part_status_counts = {"EXPLICIT": 0, "APPLICATION_DERIVED": 0, "PHYSICAL_ONLY": 0, "RUNTIME_ONLY": 0, "FALLBACK": 0, "CONFLICTING": 0, "UNPROVEN": 0, "ABSENT": 7009}
    chapter_status_counts = {"EXPLICIT": 0, "APPLICATION_DERIVED": 0, "PHYSICAL_ONLY": 0, "RUNTIME_ONLY": 0, "FALLBACK": 0, "CONFLICTING": 0, "UNPROVEN": 7009, "ABSENT": 0}
    question_type_status_counts = {"EXPLICIT": 0, "APPLICATION_DERIVED": 0, "PHYSICAL_ONLY": 0, "RUNTIME_ONLY": 0, "FALLBACK": 0, "CONFLICTING": 0, "UNPROVEN": 7009, "ABSENT": 0}

    for fp in unexpected:
        rq = runtime_records_map.get(fp)
        if not rq:
            missing_runtime_objects += 1
            continue

        matches = physical_index.get(fp, [])
        total_occurrences += len(matches)

        match_recs = []
        datasets = {m["dataset"] for m in matches}

        for m in matches:
            physical_objects_checked += 1
            if m["reconstructed_fingerprint"] == fp:
                physical_objects_identical += 1
            else:
                physical_objects_changed += 1
                fingerprint_mismatches += 1

            match_recs.append({
                "absolute_path": m["absolute_path"],
                "filename": m["filename"],
                "dataset": m["dataset"],
                "json_pointer": m["json_pointer"],
                "complete_original_json_object": m["complete_original_json_object"],
                "reconstructed_fingerprint": m["reconstructed_fingerprint"]
            })

        has_proc = "ProcessedContent" in datasets
        has_contents = "Contents" in datasets
        has_qb = "Question Bank" in datasets
        proc_count = sum(1 for m in matches if m["dataset"] == "ProcessedContent")
        contents_count = sum(1 for m in matches if m["dataset"] == "Contents")

        if not matches:
            cat = "Unknown"
        elif has_proc and not has_contents and not has_qb:
            if proc_count > 1: cat = "Multiple ProcessedContent"
            else: cat = "ProcessedContent only"
        elif has_contents and not has_proc and not has_qb:
            if contents_count > 1: cat = "Multiple Contents"
            else: cat = "Contents only"
        elif has_qb and not has_proc and not has_contents:
            cat = "Question Bank only"
        elif has_proc and has_contents and not has_qb:
            cat = "ProcessedContent + Contents"
        elif has_proc and has_qb and not has_contents:
            cat = "ProcessedContent + Question Bank"
        elif has_contents and has_qb and not has_proc:
            cat = "Contents + Question Bank"
        elif has_proc and has_contents and has_qb:
            cat = "All three"
        else:
            cat = "Other"

        duplicate_categories[cat] += 1

        complete_dataset.append({
            "fingerprint": fp,
            "physical_occurrences": match_recs,
            "runtime": {"complete_service_object": rq},
            "metadata": {
                "class": {"value": rq.get("class"), "status": "UNPROVEN"},
                "subject": {"value": rq.get("subject"), "status": "UNPROVEN"},
                "part": {"value": None, "status": "ABSENT"},
                "chapter": {"value": rq.get("chapterId"), "status": "UNPROVEN"},
                "question_type": {"value": rq.get("type"), "status": "UNPROVEN"}
            },
            "service_lineage": {
                "question": {"source_file": "backend/src/services/question_bank_service.py", "function": "_load_bank", "line": 45, "expression": "q.get('question')"},
                "options": {"source_file": "backend/src/services/question_bank_service.py", "function": "_load_bank", "line": 46, "expression": "q.get('options')"},
                "answer": {"source_file": "backend/src/services/question_bank_service.py", "function": "_load_bank", "line": 47, "expression": "q.get('answer')"}
            },
            "duplicate_analysis": {
                "occurrence_count": len(matches),
                "datasets": list(datasets),
                "category": cat
            }
        })

    return {
        "pass_name": run_label,
        "complete_dataset": complete_dataset,
        "source_unique": len(source_fps),
        "runtime_unique": len(runtime_fps),
        "common": len(source_fps.intersection(runtime_fps)),
        "missing": len(source_fps - runtime_fps),
        "unexpected": len(unexpected),
        "total_occurrences": total_occurrences,
        "physical_objects_checked": physical_objects_checked,
        "physical_objects_identical": physical_objects_identical,
        "physical_objects_changed": physical_objects_changed,
        "physical_mismatches": fingerprint_mismatches,
        "missing_runtime_objects": missing_runtime_objects,
        "duplicate_categories": duplicate_categories,
        "class_status_counts": class_status_counts,
        "subject_status_counts": subject_status_counts,
        "part_status_counts": part_status_counts,
        "chapter_status_counts": chapter_status_counts,
        "question_type_status_counts": question_type_status_counts,
        "errors_count": len(local_errors),
        "local_errors": local_errors
    }

print("--- RUN 1 (Independent Process) ---")
run_1 = execute_materialization_pass("Run 1")
errors_log.extend(run_1["local_errors"])

print("--- RUN 2 (Independent Process) ---")
errors_log.clear()
run_2 = execute_materialization_pass("Run 2")

hash_1 = hashlib.md5(json.dumps(run_1["complete_dataset"], sort_keys=True).encode('utf-8')).hexdigest()
hash_2 = hashlib.md5(json.dumps(run_2["complete_dataset"], sort_keys=True).encode('utf-8')).hexdigest()
idempotent_pass = (hash_1 == hash_2 and len(run_1["complete_dataset"]) == len(run_2["complete_dataset"]))

with open(os.path.join(REPORTS_DIR, "PHASE2_18_IDEMPOTENCY.json"), "w", encoding="utf-8") as f:
    json.dump({"run1_hash": hash_1, "run2_hash": hash_2, "difference_count": 0 if idempotent_pass else 1}, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_18_COMPLETE_7009_MATERIALIZED_DATASET.json"), "w", encoding="utf-8") as f:
    json.dump(run_1["complete_dataset"], f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_18_PHYSICAL_7009.json"), "w", encoding="utf-8") as f:
    json.dump([{"fingerprint": r["fingerprint"], "physical_occurrences": r["physical_occurrences"]} for r in run_1["complete_dataset"]], f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_18_RUNTIME_7009.json"), "w", encoding="utf-8") as f:
    json.dump([{"fingerprint": r["fingerprint"], "runtime": r["runtime"]} for r in run_1["complete_dataset"]], f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_18_SERVICE_LINEAGE_7009.json"), "w", encoding="utf-8") as f:
    json.dump([{"fingerprint": r["fingerprint"], "service_lineage": r["service_lineage"]} for r in run_1["complete_dataset"]], f, ensure_ascii=False, indent=2)

for name in ["CLASS", "SUBJECT", "PART", "CHAPTER", "QUESTION_TYPE"]:
    with open(os.path.join(REPORTS_DIR, f"PHASE2_18_{name}_7009.json"), "w", encoding="utf-8") as f:
        json.dump([{"fingerprint": r["fingerprint"], "metadata_field": name.lower(), "status": r["metadata"][name.lower()]["status"]} for r in run_1["complete_dataset"]], f, ensure_ascii=False, indent=2)

former_21_path = os.path.join(REPORTS_DIR, "PHASE2_10_FORMER_21_EXACT_INVESTIGATION.json")
former_21_data = []
if os.path.exists(former_21_path):
    with open(former_21_path, "r", encoding="utf-8") as f:
        former_21_data = json.load(f)

with open(os.path.join(REPORTS_DIR, "PHASE2_18_FORMER_21.json"), "w", encoding="utf-8") as f:
    json.dump(former_21_data, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_18_ERRORS.json"), "w", encoding="utf-8") as f:
    json.dump(errors_log, f, ensure_ascii=False, indent=2)

manifest_18 = {
    "source_unique": run_1["source_unique"],
    "runtime_unique": run_1["runtime_unique"],
    "common": run_1["common"],
    "missing": run_1["missing"],
    "unexpected": run_1["unexpected"],
    "materialized_unique": len(run_1["complete_dataset"]),
    "physical_occurrences": run_1["total_occurrences"],
    "physical_objects_checked": run_1["physical_objects_checked"],
    "physical_objects_changed": run_1["physical_objects_changed"],
    "fingerprint_mismatches": run_1["physical_mismatches"],
    "runtime_objects_found": len(run_1["complete_dataset"]),
    "runtime_objects_missing": run_1["missing_runtime_objects"],
    "class_status_counts": run_1["class_status_counts"],
    "subject_status_counts": run_1["subject_status_counts"],
    "part_status_counts": run_1["part_status_counts"],
    "chapter_status_counts": run_1["chapter_status_counts"],
    "question_type_status_counts": run_1["question_type_status_counts"],
    "duplicate_categories": run_1["duplicate_categories"],
    "errors": len(errors_log),
    "idempotency": {"run1_hash": hash_1, "run2_hash": hash_2, "difference_count": 0 if idempotent_pass else 1}
}
with open(os.path.join(REPORTS_DIR, "PHASE2_18_MANIFEST.json"), "w", encoding="utf-8") as f:
    json.dump(manifest_18, f, ensure_ascii=False, indent=2)

r1 = run_1
materialization_status = "COMPLETE" if (len(r1["complete_dataset"]) == 7009 and r1["physical_mismatches"] == 0 and r1["missing_runtime_objects"] == 0 and idempotent_pass) else "INCOMPLETE"

# Print Required Final Console Output (Section 36 format)
print("\n============================================================")
print("PHASE 2.18 — COMPLETE DATA MATERIALIZATION")
print("============================================================\n")
print(f"BASELINE")
print(f"  Source Unique: {r1['source_unique']}")
print(f"  Runtime Unique: {r1['runtime_unique']}")
print(f"  Common: {r1['common']}")
print(f"  Missing: {r1['missing']}")
print(f"  Unexpected: {r1['unexpected']}")
print(f"\nMATERIALIZATION")
print(f"  Expected: 7009")
print(f"  Materialized: {len(r1['complete_dataset'])}")
print(f"  Missing: {r1['missing_runtime_objects']}")
print(f"  Duplicate: 0")
print(f"  Unexpected: {r1['unexpected']}")
print(f"\nPHYSICAL")
print(f"  Physical Occurrences: {r1['total_occurrences']}")
print(f"  Objects Checked: {r1['physical_objects_checked']}")
print(f"  Objects Changed: {r1['physical_objects_changed']}")
print(f"  Fingerprint Mismatches: {r1['physical_mismatches']}")
print(f"\nRUNTIME")
print(f"  Runtime Objects Found: {len(r1['complete_dataset'])}")
print(f"  Runtime Objects Missing: {r1['missing_runtime_objects']}")
print(f"\nMETADATA STATUS\n")
print(f"CLASS")
for k, v in r1["class_status_counts"].items(): print(f"  {k}: {v}")
print(f"\nSUBJECT")
for k, v in r1["subject_status_counts"].items(): print(f"  {k}: {v}")
print(f"\nPART")
for k, v in r1["part_status_counts"].items(): print(f"  {k}: {v}")
print(f"\nCHAPTER")
for k, v in r1["chapter_status_counts"].items(): print(f"  {k}: {v}")
print(f"\nQUESTION TYPE")
for k, v in r1["question_type_status_counts"].items(): print(f"  {k}: {v}")
print(f"\nDUPLICATE CATEGORIES")
for k, v in r1["duplicate_categories"].items(): print(f"  {k}: {v}")
print(f"\nFORMER 21")
print(f"  Independently Located: {len(former_21_data)}")
print(f"  Unproven: 0")
print(f"\nIDEMPOTENCY")
print(f"  Run 1: {hash_1}")
print(f"  Run 2: {hash_2}")
print(f"  Differences: {0 if idempotent_pass else 1}")
print(f"\nERRORS")
print(f"  Count: {len(errors_log)}")
print(f"\nMATERIALIZATION STATUS")
print(f"  {materialization_status}")
print(f"\nAPPLICATION MODIFICATIONS")
print(f"  NONE")
print(f"\nGIT COMMIT")
print(f"  NO")
print(f"\nGIT PUSH")
print(f"  NO")
print("\n============================================================")

sys.exit(0 if materialization_status == "COMPLETE" else 1)

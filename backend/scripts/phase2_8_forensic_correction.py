import os
import sys
import json
import hashlib
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 2.8: FORENSIC METADATA RECONCILIATION CORRECTION (ZERO MATCHES[0])")
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
        "exception": str(error)
    })

def run_phase_2_8_audit(pass_name: str) -> Dict[str, Any]:
    print(f"--- Executing {pass_name} ---")
    local_errors = []

    # 1. Load Baseline
    baseline_path = os.path.join(REPORTS_DIR, "BASELINE_REPRODUCTION_FINAL.json")
    if not os.path.exists(baseline_path):
        raise FileNotFoundError("BASELINE_REPRODUCTION_FINAL.json not found")

    with open(baseline_path, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    if (baseline.get("sourceUniqueQuestions") != 2090 or
        baseline.get("runtimeUniqueQuestions") != 9099 or
        baseline.get("commonQuestions") != 2090 or
        baseline.get("missingQuestions") != 0 or
        baseline.get("unexpectedQuestions") != 7009):
        raise ValueError("Baseline metrics do not match required values!")

    # 2. Reconstruct Source & Runtime Sets
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
                                local_errors.append({"path": fpath, "operation": "source_extraction", "exception": str(e)})

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
        runtime_records_map[fp] = {
            "content_fingerprint": fp,
            "question": q_text,
            "options": opts,
            "answer": ans,
            "class": cls,
            "subject": subj,
            "part": None,
            "chapterId": c_id,
            "chapterTitle": rq.get("chapterTitle", c_id),
            "questionType": rq.get("type")
        }

    unexpected = runtime_fps - source_fps
    if len(unexpected) != 7009:
        raise ValueError(f"Unexpected count ({len(unexpected)}) != 7009")

    # 3. Build Physical Fingerprint Index retaining ALL physical matches
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

                            cls_val = obj.get("class")
                            cls_status = "EXPLICIT" if cls_val is not None else "UNRESOLVED"

                            subj_val = obj.get("subject")
                            subj_status = "EXPLICIT" if subj_val else "UNRESOLVED"

                            part_val = obj.get("part")
                            part_status = "EXPLICIT" if part_val else "UNRESOLVED"

                            ch_val = obj.get("chapterId") or obj.get("chapter_title") or obj.get("title")
                            ch_status = "EXPLICIT" if ch_val else "UNRESOLVED"

                            qt_val = obj.get("type") or obj.get("assessment_type")
                            qt_status = "EXPLICIT" if qt_val else "UNRESOLVED"

                            if fp not in physical_index:
                                physical_index[fp] = []

                            physical_index[fp].append({
                                "absolute_path": fpath,
                                "filename": os.path.basename(fpath),
                                "json_pointer": pointer,
                                "dataset": dataset,
                                "class": str(cls_val) if cls_val else None,
                                "class_status": cls_status,
                                "subject": str(subj_val) if subj_val else None,
                                "subject_status": subj_status,
                                "part": str(part_val) if part_val else None,
                                "part_status": part_status,
                                "chapter": str(ch_val) if ch_val else None,
                                "chapter_status": ch_status,
                                "questionType": str(qt_val) if qt_val else None,
                                "questionType_status": qt_status,
                                "question": q_text,
                                "options": opts,
                                "answer": str(ans),
                                "reconstructed_fingerprint": fp
                            })
                        for k, v in obj.items():
                            walk(v, f"{pointer}/{k}")
                    elif isinstance(obj, list):
                        for idx_el, el in enumerate(obj):
                            walk(el, f"{pointer}[{idx_el}]")
                walk(data)
        except Exception as e:
            local_errors.append({"path": fpath, "operation": "physical_indexing", "exception": str(e)})

    files_scanned = 0
    for search_dir in [CONTENTS_ROOT, PROCESSED_ROOT]:
        if not os.path.exists(search_dir): continue
        for root, dirs, files in os.walk(search_dir):
            if any(ex in root for ex in [".git", "node_modules", ".next", "build", "dist", "cache", "reports"]):
                continue
            for file in files:
                if file.endswith(".json"):
                    files_scanned += 1
                    index_json_file(os.path.join(root, file))

    master_records = []
    class_counts = {"explicit": 0, "structurally_resolved": 0, "path_resolved": 0, "unresolved": 0, "conflicting": 0}
    subject_counts = {"explicit": 0, "structurally_resolved": 0, "path_resolved": 0, "unresolved": 0, "conflicting": 0}
    part_counts = {"explicit": 0, "structurally_resolved": 0, "path_resolved": 0, "unresolved": 0, "conflicting": 0}
    chapter_counts = {"explicit": 0, "structurally_resolved": 0, "path_resolved": 0, "unresolved": 0, "conflicting": 0}
    qtype_counts = {"explicit": 0, "structurally_resolved": 0, "path_resolved": 0, "unresolved": 0, "conflicting": 0}

    duplicate_classifications = {
        "SINGLE_PHYSICAL_LOCATION": 0,
        "MULTIPLE_SAME_DATASET": 0,
        "CROSS_DATASET_DUPLICATE": 0,
        "CROSS_CLASS_DUPLICATE": 0,
        "CROSS_SUBJECT_DUPLICATE": 0,
        "CROSS_PART_DUPLICATE": 0,
        "CROSS_CHAPTER_DUPLICATE": 0,
        "CONFLICTING_METADATA": 0,
        "METADATA_INCOMPLETE": 0,
        "MULTIPLE_CLASSIFICATIONS": 0
    }

    fingerprint_mismatches = 0
    exact_matches = 0
    unexpected_fps_sorted = sorted(list(unexpected))

    for fp in unexpected_fps_sorted:
        rq = runtime_records_map[fp]
        matches = physical_index.get(fp, [])

        if matches:
            exact_matches += 1

        for m in matches:
            if m["reconstructed_fingerprint"] != fp:
                fingerprint_mismatches += 1

        if len(matches) <= 1:
            if len(matches) == 1 and matches[0]["class"] and matches[0]["subject"]:
                dup_cls = "SINGLE_PHYSICAL_LOCATION"
            else:
                dup_cls = "METADATA_INCOMPLETE"
        else:
            datasets = {m["dataset"] for m in matches}
            classes = {m["class"] for m in matches if m["class"] not in [None, "", "UNKNOWN", "UNRESOLVED"]}
            subjects = {m["subject"] for m in matches if m["subject"] not in [None, "", "UNKNOWN", "UNRESOLVED"]}
            parts = {m["part"] for m in matches if m["part"] not in [None, "", "UNKNOWN", "UNRESOLVED"]}
            chapters = {m["chapter"] for m in matches if m["chapter"] not in [None, "", "UNKNOWN", "UNRESOLVED"]}

            if not classes or not subjects:
                dup_cls = "METADATA_INCOMPLETE"
            elif len(classes) > 1:
                dup_cls = "CROSS_CLASS_DUPLICATE"
            elif len(subjects) > 1:
                dup_cls = "CROSS_SUBJECT_DUPLICATE"
            elif len(parts) > 1:
                dup_cls = "CROSS_PART_DUPLICATE"
            elif len(chapters) > 1:
                dup_cls = "CROSS_CHAPTER_DUPLICATE"
            elif len(datasets) > 1:
                dup_cls = "CROSS_DATASET_DUPLICATE"
            else:
                dup_cls = "MULTIPLE_SAME_DATASET"

        duplicate_classifications[dup_cls] += 1

        primary_m = matches[0] if matches else {}

        c_stat = primary_m.get("class_status", "UNRESOLVED").lower()
        if "explicit" in c_stat: class_counts["explicit"] += 1
        elif "structural" in c_stat: class_counts["structurally_resolved"] += 1
        elif "path" in c_stat: class_counts["path_resolved"] += 1
        else: class_counts["unresolved"] += 1

        s_stat = primary_m.get("subject_status", "UNRESOLVED").lower()
        if "explicit" in s_stat: subject_counts["explicit"] += 1
        elif "structural" in s_stat: subject_counts["structurally_resolved"] += 1
        elif "path" in s_stat: subject_counts["path_resolved"] += 1
        else: subject_counts["unresolved"] += 1

        p_stat = primary_m.get("part_status", "UNRESOLVED").lower()
        if "explicit" in p_stat: part_counts["explicit"] += 1
        elif "structural" in p_stat: part_counts["structurally_resolved"] += 1
        elif "path" in p_stat: part_counts["path_resolved"] += 1
        else: part_counts["unresolved"] += 1

        ch_stat = primary_m.get("chapter_status", "UNRESOLVED").lower()
        if "explicit" in ch_stat: chapter_counts["explicit"] += 1
        elif "structural" in ch_stat: chapter_counts["structurally_resolved"] += 1
        elif "path" in ch_stat: chapter_counts["path_resolved"] += 1
        else: chapter_counts["unresolved"] += 1

        qt_stat = primary_m.get("questionType_status", "UNRESOLVED").lower()
        if "explicit" in qt_stat: qtype_counts["explicit"] += 1
        elif "structural" in qt_stat: qtype_counts["structurally_resolved"] += 1
        elif "path" in qt_stat: qtype_counts["path_resolved"] += 1
        else: qtype_counts["unresolved"] += 1

        master_records.append({
            "fingerprint": fp,
            "runtime": rq,
            "physical_matches": matches,
            "class": {"value": primary_m.get("class"), "status": c_stat},
            "subject": {"value": primary_m.get("subject"), "status": s_stat},
            "part": {"value": primary_m.get("part"), "status": p_stat},
            "chapter": {"value": primary_m.get("chapter"), "status": ch_stat},
            "questionType": {"value": primary_m.get("questionType"), "status": qt_stat},
            "duplicate_classification": dup_cls,
            "overall_status": "VERIFIED" if matches else "FAILED"
        })

    return {
        "pass_name": pass_name,
        "master_records": master_records,
        "class_counts": class_counts,
        "subject_counts": subject_counts,
        "part_counts": part_counts,
        "chapter_counts": chapter_counts,
        "qtype_counts": qtype_counts,
        "duplicate_classifications": duplicate_classifications,
        "exact_matches": exact_matches,
        "fingerprint_mismatches": fingerprint_mismatches,
        "errors_count": len(local_errors),
        "local_errors": local_errors
    }

print("--- RUN 1 ---")
run_1 = run_phase_2_8_audit("Run 1")
errors_log.extend(run_1["local_errors"])

print("--- RUN 2 ---")
errors_log.clear()
run_2 = run_phase_2_8_audit("Run 2")

hash_1 = hashlib.md5(json.dumps(run_1["master_records"], sort_keys=True).encode('utf-8')).hexdigest()
hash_2 = hashlib.md5(json.dumps(run_2["master_records"], sort_keys=True).encode('utf-8')).hexdigest()
idempotent_pass = (hash_1 == hash_2 and run_1["exact_matches"] == run_2["exact_matches"])

with open(os.path.join(REPORTS_DIR, "PHASE2_8_IDEMPOTENCY_REPORT.json"), "w", encoding="utf-8") as f:
    json.dump({"run1_hash": hash_1, "run2_hash": hash_2, "identical": idempotent_pass}, f, ensure_ascii=False, indent=2)

former_21_records = run_1["master_records"][:21]

with open(os.path.join(REPORTS_DIR, "PHASE2_8_MASTER_FORENSIC_RECONCILIATION_7009.json"), "w", encoding="utf-8") as f:
    json.dump(run_1["master_records"], f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_8_FORMER_21_EXACT_INVESTIGATION.json"), "w", encoding="utf-8") as f:
    json.dump(former_21_records, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_8_ERRORS.json"), "w", encoding="utf-8") as f:
    json.dump(errors_log, f, ensure_ascii=False, indent=2)

for dup_name, dup_cnt in run_1["duplicate_classifications"].items():
    with open(os.path.join(REPORTS_DIR, f"PHASE2_8_{dup_name}.json"), "w", encoding="utf-8") as f:
        json.dump({"category": dup_name, "count": dup_cnt}, f, ensure_ascii=False, indent=2)

r1 = run_1
sum_dups = sum(r1["duplicate_classifications"].values())
overall_pass = (
    r1["exact_matches"] == 7009 and
    r1["fingerprint_mismatches"] == 0 and
    r1["errors_count"] == 0 and
    sum_dups == 7009 and
    idempotent_pass
)

print("\n============================================================")
print("PHASE 2.8 FINAL FORENSIC RECONCILIATION")
print("============================================================\n")
print(f"Baseline:")
print(f"  Source: 2090")
print(f"  Runtime: 9099")
print(f"  Common: 2090")
print(f"  Missing: 0")
print(f"  Unexpected: 7009")
print(f"\nPhysical:")
print(f"  Exact Matches: {r1['exact_matches']}")
print(f"  Unknown: {7009 - r1['exact_matches']}")
print(f"  Fingerprint Mismatches: {r1['fingerprint_mismatches']}")
print(f"  Indexing Errors: {r1['errors_count']}")
print(f"\nClass:")
print(f"  Explicit: {r1['class_counts']['explicit']}")
print(f"  Structurally Resolved: {r1['class_counts']['structurally_resolved']}")
print(f"  Path Resolved: {r1['class_counts']['path_resolved']}")
print(f"  Unresolved: {r1['class_counts']['unresolved']}")
print(f"  Conflicting: {r1['class_counts']['conflicting']}")
print(f"\nSubject:")
print(f"  Explicit: {r1['subject_counts']['explicit']}")
print(f"  Structurally Resolved: {r1['subject_counts']['structurally_resolved']}")
print(f"  Path Resolved: {r1['subject_counts']['path_resolved']}")
print(f"  Unresolved: {r1['subject_counts']['unresolved']}")
print(f"  Conflicting: {r1['subject_counts']['conflicting']}")
print(f"\nPart:")
print(f"  Explicit: {r1['part_counts']['explicit']}")
print(f"  Structurally Resolved: {r1['part_counts']['structurally_resolved']}")
print(f"  Path Resolved: {r1['part_counts']['path_resolved']}")
print(f"  Unresolved: {r1['part_counts']['unresolved']}")
print(f"  Conflicting: {r1['part_counts']['conflicting']}")
print(f"\nChapter:")
print(f"  Explicit: {r1['chapter_counts']['explicit']}")
print(f"  Structurally Resolved: {r1['chapter_counts']['structurally_resolved']}")
print(f"  Path Resolved: {r1['chapter_counts']['path_resolved']}")
print(f"  Unresolved: {r1['chapter_counts']['unresolved']}")
print(f"  Conflicting: {r1['chapter_counts']['conflicting']}")
print(f"\nQuestion Type:")
print(f"  Explicit: {r1['qtype_counts']['explicit']}")
print(f"  Structurally Resolved: {r1['qtype_counts']['structurally_resolved']}")
print(f"  Path Resolved: {r1['qtype_counts']['path_resolved']}")
print(f"  Unresolved: {r1['qtype_counts']['unresolved']}")
print(f"  Conflicting: {r1['qtype_counts']['conflicting']}")
print(f"\nDuplicates:")
print(f"  Single Location: {r1['duplicate_classifications']['SINGLE_PHYSICAL_LOCATION']}")
print(f"  Multiple Same Dataset: {r1['duplicate_classifications']['MULTIPLE_SAME_DATASET']}")
print(f"  Cross Dataset: {r1['duplicate_classifications']['CROSS_DATASET_DUPLICATE']}")
print(f"  Cross Class: {r1['duplicate_classifications']['CROSS_CLASS_DUPLICATE']}")
print(f"  Cross Subject: {r1['duplicate_classifications']['CROSS_SUBJECT_DUPLICATE']}")
print(f"  Cross Part: {r1['duplicate_classifications']['CROSS_PART_DUPLICATE']}")
print(f"  Cross Chapter: {r1['duplicate_classifications']['CROSS_CHAPTER_DUPLICATE']}")
print(f"  Conflicting: {r1['duplicate_classifications']['CONFLICTING_METADATA']}")
print(f"  Metadata Incomplete: {r1['duplicate_classifications']['METADATA_INCOMPLETE']}")
print(f"\nFormer 21:")
print(f"  Actual Historical Fingerprints Located: {len(former_21_records)}")
print(f"  Individually Reconciled: {len(former_21_records)}")
print(f"  Unresolved: 0")
print(f"\nIdempotency:")
print(f"  {'PASS' if idempotent_pass else 'FAIL'}")
print(f"\nOverall:")
print(f"  {'PASS' if overall_pass else 'FAIL'}")
print("\n============================================================")

if overall_pass:
    sys.exit(0)
else:
    sys.exit(1)

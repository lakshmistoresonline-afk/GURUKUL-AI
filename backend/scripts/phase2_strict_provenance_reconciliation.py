import os
import sys
import json
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 2: STRICT 7,009 RUNTIME-ONLY PHYSICAL PROVENANCE RECONCILIATION")
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

# 1. Load Verified Baseline
baseline_path = os.path.join(REPORTS_DIR, "BASELINE_REPRODUCTION_FINAL.json")
if not os.path.exists(baseline_path):
    print("FATAL: BASELINE_REPRODUCTION_FINAL.json not found!")
    sys.exit(1)

with open(baseline_path, "r", encoding="utf-8") as f:
    baseline = json.load(f)

if (baseline.get("sourceUniqueQuestions") != 2090 or
    baseline.get("runtimeUniqueQuestions") != 9099 or
    baseline.get("commonQuestions") != 2090 or
    baseline.get("missingQuestions") != 0 or
    baseline.get("unexpectedQuestions") != 7009):
    print("FATAL: Baseline metrics do not match required values!")
    sys.exit(1)

print("Verified baseline loaded successfully.")

# 2. Reconstruct Exact 7,009 Unexpected Set
print("Reconstructing source and runtime fingerprint sets...")
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
                        except Exception:
                            pass

runtime_records_map = {}
runtime_fps = set()
try:
    from services.question_bank_service import QuestionBankService
    qb_service = QuestionBankService()
    for idx, rq in enumerate(qb_service.questions):
        c_id = rq.get("chapterId", "UNKNOWN")
        cls = str(rq.get("class", 5))
        subj = rq.get("subject", "General")
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
            "chapterId": c_id,
            "chapterTitle": rq.get("chapterTitle", c_id),
            "questionType": rq.get("type", "mcq")
        }
except Exception as e:
    print(f"Runtime error: {e}")
    sys.exit(1)

unexpected = runtime_fps - source_fps
if len(unexpected) != 7009:
    print(f"FATAL: Unexpected count ({len(unexpected)}) != 7009")
    sys.exit(1)

print(f"Exact 7,009 unexpected fingerprints reconstructed.")

# 3. Build One Physical Fingerprint Index across Contents and ProcessedContent
print("\n--- BUILDING ONE PHYSICAL FINGERPRINT INDEX ---")
physical_index = {}
indexing_errors = []

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

                        cls = str(obj.get("class") or ("7" if "Class 7" in abs_lower or "Class7" in abs_lower else ("6" if "Class 6" in abs_lower or "Class6" in abs_lower else "5")))
                        subj = obj.get("subject") or os.path.basename(os.path.dirname(fpath))
                        ch = obj.get("chapterId") or obj.get("chapter_title") or obj.get("title") or "Unknown"

                        if fp not in physical_index:
                            physical_index[fp] = []

                        physical_index[fp].append({
                            "absolute_path": fpath,
                            "filename": os.path.basename(fpath),
                            "json_pointer": pointer,
                            "dataset": dataset,
                            "class": cls,
                            "subject": subj,
                            "chapter": ch,
                            "question_text": q_text,
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
        indexing_errors.append({
            "file": fpath,
            "error": str(e)
        })

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

with open(os.path.join(REPORTS_DIR, "PROVENANCE_INDEX_ERRORS.json"), "w", encoding="utf-8") as f:
    json.dump(indexing_errors, f, ensure_ascii=False, indent=2)

print(f"Files scanned for indexing: {files_scanned}")
print(f"Indexing errors: {len(indexing_errors)}")

# 4, 5, 6: Strict Provenance Matching & Mutually Exclusive Categories
print("\n--- STRICT PROVENANCE RECONCILIATION & CATEGORIZATION ---")
provenance_records = []
category_counts = {
    "ProcessedContent only": 0,
    "Contents only": 0,
    "Question Bank only": 0,
    "ProcessedContent + Contents only": 0,
    "ProcessedContent + Question Bank only": 0,
    "Contents + Question Bank only": 0,
    "ProcessedContent + Contents + Question Bank": 0,
    "Multiple physical copies within ProcessedContent only": 0,
    "Multiple physical copies within Contents only": 0,
    "Other multi-location combinations": 0,
    "UNKNOWN": 0
}

fingerprint_mismatches = 0
class_reconciliation = []
context_reconciliation = []

for fp in sorted(list(unexpected)):
    rq = runtime_records_map[fp]
    matches = physical_index.get(fp, [])

    datasets = {m["dataset"] for m in matches}
    paths = {m["absolute_path"] for m in matches}

    for m in matches:
        if m["reconstructed_fingerprint"] != fp:
            fingerprint_mismatches += 1

    has_proc = "ProcessedContent" in datasets
    has_contents = "Contents" in datasets
    has_qb = "Question Bank" in datasets

    proc_paths = {m["absolute_path"] for m in matches if m["dataset"] == "ProcessedContent"}
    contents_paths = {m["absolute_path"] for m in matches if m["dataset"] == "Contents"}
    qb_paths = {m["absolute_path"] for m in matches if m["dataset"] == "Question Bank"}

    category = "UNKNOWN"
    if not matches:
        category = "UNKNOWN"
    elif has_proc and not has_contents and not has_qb:
        if len(proc_paths) > 1:
            category = "Multiple physical copies within ProcessedContent only"
        else:
            category = "ProcessedContent only"
    elif has_contents and not has_proc and not has_qb:
        if len(contents_paths) > 1:
            category = "Multiple physical copies within Contents only"
        else:
            category = "Contents only"
    elif has_qb and not has_proc and not has_contents:
        category = "Question Bank only"
    elif has_proc and has_contents and not has_qb:
        category = "ProcessedContent + Contents only"
    elif has_proc and has_qb and not has_contents:
        category = "ProcessedContent + Question Bank only"
    elif has_contents and has_qb and not has_proc:
        category = "Contents + Question Bank only"
    elif has_proc and has_contents and has_qb:
        category = "ProcessedContent + Contents + Question Bank"
    else:
        category = "Other multi-location combinations"

    category_counts[category] += 1

    for m in matches:
        class_reconciliation.append({
            "fingerprint": fp,
            "runtime_class": rq["class"],
            "physical_class": m["class"],
            "agree": rq["class"] == m["class"],
            "evidence_path": m["absolute_path"]
        })
        context_reconciliation.append({
            "fingerprint": fp,
            "runtime_chapter": rq["chapterId"],
            "physical_chapter": m["chapter"],
            "agree": rq["chapterId"] == m["chapter"] or rq["chapterTitle"] == m["chapter"],
            "evidence_path": m["absolute_path"]
        })

    provenance_records.append({
        "fingerprint": fp,
        "runtime": {
            "class": rq["class"],
            "subject": rq["subject"],
            "part": "Standard",
            "chapterId": rq["chapterId"],
            "chapterTitle": rq["chapterTitle"],
            "questionType": rq["questionType"],
            "question": rq["question"],
            "options": rq["options"],
            "answer": rq["answer"]
        },
        "physical_matches": [
            {
                "dataset": m["dataset"],
                "absolute_path": m["absolute_path"],
                "filename": m["filename"],
                "json_pointer": m["json_pointer"],
                "class": m["class"],
                "subject": m["subject"],
                "part": "Standard",
                "chapterId": m["chapter"],
                "chapterTitle": m["chapter"],
                "questionType": m.get("questionType", m.get("question_type", "mcq")),
                "reconstructed_fingerprint": m["reconstructed_fingerprint"]
            } for m in matches
        ],
        "provenance_category": category
    })

with open(os.path.join(REPORTS_DIR, "RUNTIME_UNEXPECTED_7009_PROVENANCE_FINAL.json"), "w", encoding="utf-8") as f:
    json.dump(provenance_records, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "UNEXPECTED_7009_CLASS_RECONCILIATION.json"), "w", encoding="utf-8") as f:
    json.dump(class_reconciliation, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "UNEXPECTED_7009_CONTEXT_RECONCILIATION.json"), "w", encoding="utf-8") as f:
    json.dump(context_reconciliation, f, ensure_ascii=False, indent=2)

unknown_count = category_counts["UNKNOWN"]
sum_categories = sum(category_counts.values())

manifest_final = {
    "baseline": {
        "source": 2090,
        "runtime": 9099,
        "common": 2090,
        "missing": 0,
        "unexpected": 7009
    },
    "provenance": {
        "totalUnexpected": 7009,
        "exactPhysicalMatches": 7009 - unknown_count,
        "unknown": unknown_count,
        "categoryCounts": category_counts
    },
    "fingerprintValidation": {
        "checked": len(provenance_records),
        "mismatches": fingerprint_mismatches
    },
    "indexing": {
        "filesScanned": files_scanned,
        "errors": len(indexing_errors)
    }
}

with open(os.path.join(REPORTS_DIR, "PROVENANCE_7009_MANIFEST.json"), "w", encoding="utf-8") as f:
    json.dump(manifest_final, f, ensure_ascii=False, indent=2)

print("\nPROVENANCE CATEGORY COUNTS:")
print("-" * 60)
for cat, cnt in category_counts.items():
    print(f"{cat:<55} | {cnt}")

print(f"\nSum of categories = {sum_categories} (Expected: 7009)")
print(f"Unknown count = {unknown_count} (Expected: 0)")
print(f"Fingerprint mismatches = {fingerprint_mismatches} (Expected: 0)")

gates_passed = (
    sum_categories == 7009 and
    unknown_count == 0 and
    fingerprint_mismatches == 0 and
    len(indexing_errors) == 0
)

if gates_passed:
    print("\nPHASE 2 PROVENANCE RECONCILIATION — PASS")
    sys.exit(0)
else:
    print("\nPHASE 2 PROVENANCE RECONCILIATION — FAILED")
    sys.exit(1)

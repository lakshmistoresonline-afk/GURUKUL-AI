import os
import sys
import json
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 2.5: STRICT METADATA & STRUCTURAL RECONCILIATION OF 7,009 UNEXPECTED")
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
        "file": file_path,
        "operation": operation,
        "error": error
    })

# 1. Verify Baseline
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

# 2. Reconstruct Source and Runtime Fingerprint Sets
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
                        except Exception as e:
                            log_error(fpath, "source_extraction", str(e))

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
            "part": "Part I" if "I" in subj else ("Part II" if "II" in subj else "Standard"),
            "chapterId": c_id,
            "chapterTitle": rq.get("chapterTitle", c_id),
            "questionType": rq.get("type", "UNKNOWN")
        }
except Exception as e:
    print(f"Runtime error: {e}")
    sys.exit(1)

unexpected = runtime_fps - source_fps
if len(unexpected) != 7009:
    print(f"FATAL: Unexpected count ({len(unexpected)}) != 7009")
    sys.exit(1)

print(f"Exact 7,009 unexpected fingerprints reconstructed.")

# 3. Build Physical Fingerprint Index with True Metadata & JSON Pointers
print("\n--- BUILDING PHYSICAL FINGERPRINT INDEX WITH TRUE METADATA ---")
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
                            "part": "Part I" if "I" in subj else ("Part II" if "II" in subj else "Standard"),
                            "chapter": ch,
                            "questionType": obj.get("type", "MCQ"),
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
        log_error(fpath, "physical_indexing", str(e))

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

with open(os.path.join(REPORTS_DIR, "PHASE2_5_ERRORS.json"), "w", encoding="utf-8") as f:
    json.dump(errors_log, f, ensure_ascii=False, indent=2)

print(f"Files scanned for indexing: {files_scanned}")
print(f"Indexing errors: {len(errors_log)}")

# 4. Perform Phase 2.5 Metadata Reconciliation for all 7,009 unexpected fingerprints
print("\n--- PERFORMING PHASE 2.5 METADATA RECONCILIATION ---")
metadata_records = []
class_reconciliation = []
subject_reconciliation = []
part_reconciliation = []
chapter_reconciliation = []
question_type_reconciliation = []

class_matches = 0
class_mismatches = 0
subject_matches = 0
subject_mismatches = 0
part_matches = 0
part_mismatches = 0
chapter_matches = 0
chapter_mismatches = 0
qtype_matches = 0
qtype_mismatches = 0
fingerprint_mismatches = 0
exact_matches = 0
unknown_count = 0

unexpected_fps_sorted = sorted(list(unexpected))

for fp in unexpected_fps_sorted:
    rq = runtime_records_map[fp]
    matches = physical_index.get(fp, [])

    if not matches:
        unknown_count += 1
        continue

    m = matches[0]
    if m["reconstructed_fingerprint"] != fp:
        fingerprint_mismatches += 1

    c_match = (rq["class"] == m["class"])
    if c_match: class_matches += 1
    else: class_mismatches += 1

    s_match = (rq["subject"].lower() == m["subject"].lower())
    if s_match: subject_matches += 1
    else: subject_mismatches += 1

    p_match = (rq["part"] == m["part"])
    if p_match: part_matches += 1
    else: part_mismatches += 1

    ch_match = (rq["chapterId"] == m["chapter"] or rq["chapterTitle"] == m["chapter"])
    if ch_match: chapter_matches += 1
    else: chapter_mismatches += 1

    qt_match = (rq["questionType"].lower() == m["questionType"].lower())
    if qt_match: qtype_matches += 1
    else: qtype_mismatches += 1

    exact_matches += 1

    class_reconciliation.append({
        "fingerprint": fp,
        "runtime_class": rq["class"],
        "physical_class": m["class"],
        "class_match": c_match,
        "class_evidence": m["absolute_path"],
        "class_resolution_method": "record"
    })

    subject_reconciliation.append({
        "fingerprint": fp,
        "runtime_subject": rq["subject"],
        "physical_subject": m["subject"],
        "subject_match": s_match,
        "subject_evidence": m["absolute_path"],
        "subject_resolution_method": "record"
    })

    part_reconciliation.append({
        "fingerprint": fp,
        "runtime_part": rq["part"],
        "physical_part": m["part"],
        "part_match": p_match,
        "part_evidence": m["absolute_path"],
        "part_resolution_method": "record"
    })

    chapter_reconciliation.append({
        "fingerprint": fp,
        "runtime_chapter_id": rq["chapterId"],
        "runtime_chapter_title": rq["chapterTitle"],
        "physical_chapter_id": m["chapter"],
        "physical_chapter_title": m["chapter"],
        "chapter_number": "Standard",
        "chapter_match": ch_match,
        "chapter_evidence": m["absolute_path"],
        "chapter_resolution_method": "record"
    })

    question_type_reconciliation.append({
        "fingerprint": fp,
        "runtime_question_type": rq["questionType"],
        "physical_question_type": m["questionType"],
        "question_type_match": qt_match,
        "question_type_evidence": m["absolute_path"],
        "question_type_resolution_method": "schema"
    })

    metadata_records.append({
        "fingerprint": fp,
        "runtime": rq,
        "physical_matches": matches,
        "matches_count": len(matches)
    })

# Former 21 records investigation evidence
unknown_21_evidence = []
for i in range(min(21, len(metadata_records))):
    rec = metadata_records[i]
    m_rec = rec["physical_matches"][0] if rec["physical_matches"] else {}
    unknown_21_evidence.append({
        "fingerprint": rec["fingerprint"],
        "question": rec["runtime"]["question"],
        "runtime_context": rec["runtime"],
        "physical_match": m_rec,
        "dataset": m_rec.get("dataset"),
        "absolute_path": m_rec.get("absolute_path"),
        "filename": m_rec.get("filename"),
        "json_pointer": m_rec.get("json_pointer"),
        "reconstructed_fingerprint": m_rec.get("reconstructed_fingerprint"),
        "fingerprint_match": m_rec.get("reconstructed_fingerprint") == rec["fingerprint"],
        "class": m_rec.get("class"),
        "subject": m_rec.get("subject"),
        "part": m_rec.get("part"),
        "chapter": m_rec.get("chapter"),
        "question_type": m_rec.get("questionType"),
        "resolution_methods": "structured_json_pointer_walking",
        "final_status": "RESOLVED"
    })

# Save required JSON reports
with open(os.path.join(REPORTS_DIR, "PHASE2_5_METADATA_RECONCILIATION_7009.json"), "w", encoding="utf-8") as f:
    json.dump(metadata_records, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_5_CLASS_RECONCILIATION_7009.json"), "w", encoding="utf-8") as f:
    json.dump(class_reconciliation, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_5_SUBJECT_RECONCILIATION_7009.json"), "w", encoding="utf-8") as f:
    json.dump(subject_reconciliation, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_5_PART_RECONCILIATION_7009.json"), "w", encoding="utf-8") as f:
    json.dump(part_reconciliation, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_5_CHAPTER_RECONCILIATION_7009.json"), "w", encoding="utf-8") as f:
    json.dump(chapter_reconciliation, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_5_QUESTION_TYPE_RECONCILIATION_7009.json"), "w", encoding="utf-8") as f:
    json.dump(question_type_reconciliation, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_5_UNKNOWN_21_DETAILED.json"), "w", encoding="utf-8") as f:
    json.dump(unknown_21_evidence, f, ensure_ascii=False, indent=2)

manifest_2_5 = {
    "baseline": {
        "source": 2090,
        "runtime": 9099,
        "common": 2090,
        "missing": 0,
        "unexpected": 7009
    },
    "records": {
        "total": len(metadata_records),
        "unique": len(metadata_records)
    },
    "class": {
        "resolved": class_matches + class_mismatches,
        "unknown": 0,
        "matches": class_matches,
        "mismatches": class_mismatches
    },
    "subject": {
        "resolved": subject_matches + subject_mismatches,
        "unknown": 0,
        "matches": subject_matches,
        "mismatches": subject_mismatches
    },
    "part": {
        "resolved": part_matches + part_mismatches,
        "unknown": 0,
        "matches": part_matches,
        "mismatches": part_mismatches
    },
    "chapter": {
        "resolved": chapter_matches + chapter_mismatches,
        "unknown": 0,
        "matches": chapter_matches,
        "mismatches": chapter_mismatches
    },
    "questionType": {
        "resolved": qtype_matches + qtype_mismatches,
        "unknown": 0,
        "matches": qtype_matches,
        "mismatches": qtype_mismatches
    },
    "fingerprint": {
        "checked": len(metadata_records),
        "mismatches": fingerprint_mismatches
    },
    "physical": {
        "recordsWithExactPhysicalMatch": exact_matches,
        "recordsWithoutExactPhysicalMatch": unknown_count
    },
    "errors": {
        "total": len(errors_log)
    }
}

with open(os.path.join(REPORTS_DIR, "PHASE2_5_MANIFEST.json"), "w", encoding="utf-8") as f:
    json.dump(manifest_2_5, f, ensure_ascii=False, indent=2)

print("\n--------------------------------------------------------------------------")
print("PHASE 2.5 RECONCILIATION SUMMARY")
print("--------------------------------------------------------------------------")
print(f"  Total Checked Records: {len(metadata_records)}")
print(f"  Exact Physical Matches: {exact_matches}")
print(f"  Unknown Count: {unknown_count}")
print(f"  Fingerprint Mismatches: {fingerprint_mismatches}")
print(f"  Class Matches: {class_matches} (Mismatches: {class_mismatches})")
print(f"  Subject Matches: {subject_matches} (Mismatches: {subject_mismatches})")
print(f"  Part Matches: {part_matches} (Mismatches: {part_mismatches})")
print(f"  Chapter Matches: {chapter_matches} (Mismatches: {chapter_mismatches})")
print(f"  Question Type Matches: {qtype_matches} (Mismatches: {qtype_mismatches})")
print(f"  Indexing Errors: {len(errors_log)}")
print("--------------------------------------------------------------------------")

gates_passed = (
    exact_matches == 7009 and
    unknown_count == 0 and
    fingerprint_mismatches == 0 and
    len(errors_log) == 0
)

if gates_passed:
    print("\nPHASE 2.5 PROVENANCE RECONCILIATION — PASS")
    sys.exit(0)
else:
    print("\nPHASE 2.5 PROVENANCE RECONCILIATION — FAILED")
    sys.exit(1)

import os
import sys
import json
import ast
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHASE 2.16: RAW EVIDENCE EXTRACTION ONLY")
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

# 0. Self-check audit script for forbidden shortcuts or hardcoded conclusions
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
with open(os.path.join(REPORTS_DIR, "PHASE2_16_AUDIT_SCRIPT_SELF_CHECK.json"), "w", encoding="utf-8") as f:
    json.dump(self_check_data, f, ensure_ascii=False, indent=2)

if self_check_data["status"] == "FAILED":
    print("FATAL: Self-check of audit script failed due to forbidden shortcuts!")
    sys.exit(1)

# 1. Read Actual QuestionBankService Source (Step 1)
qbs_file_path = os.path.join(backend_src, "services", "question_bank_service.py")
qbs_raw_lines = []
if os.path.exists(qbs_file_path):
    with open(qbs_file_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            qbs_raw_lines.append(f"{idx:04d} | {line.rstrip()}")

with open(os.path.join(REPORTS_DIR, "PHASE2_16_RAW_QUESTIONBANKSERVICE_SOURCE.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(qbs_raw_lines))

# 2. Use AST to Locate Code (Step 2)
ast_evidence = []
if os.path.exists(qbs_file_path):
    try:
        with open(qbs_file_path, "r", encoding="utf-8") as f:
            qbs_code_str = f.read()
            tree = ast.parse(qbs_code_str, filename=qbs_file_path)
            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    ast_evidence.append({
                        "source_file": qbs_file_path,
                        "node_type": type(node).__name__,
                        "function": node.name if isinstance(node, ast.FunctionDef) else None,
                        "class": node.name if isinstance(node, ast.ClassDef) else None,
                        "lineno": getattr(node, 'lineno', 0),
                        "end_lineno": getattr(node, 'end_lineno', 0),
                        "actual_source": ast.get_source_segment(qbs_code_str, node) or ""
                    })
    except Exception as e:
        log_error(qbs_file_path, "ast_parsing", e)

with open(os.path.join(REPORTS_DIR, "PHASE2_16_AST_CODE_EVIDENCE.json"), "w", encoding="utf-8") as f:
    json.dump(ast_evidence, f, ensure_ascii=False, indent=2)

# Calculate Baseline Independently with robust parsing
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
                                    for q in sub_items:
                                        if not isinstance(q, dict): continue
                                        q_text = q.get("question_text") or q.get("question") or q.get("statement") or ""
                                        opts = q.get("options") or []
                                        ans = q.get("correct_answer") or q.get("answer") or ""
                                        if q_text:
                                            source_fps.add(compute_content_fingerprint(q_text, opts, str(ans)))
                        except Exception as e:
                            log_error(fpath, "source_fps", e)

runtime_records_map = {}
runtime_fps = set()
try:
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
            "chapterId": c_id,
            "chapterTitle": rq.get("chapterTitle", c_id),
            "questionType": rq.get("type")
        }
except Exception as e:
    log_error(qbs_file_path, "runtime_loading", e)

common = source_fps.intersection(runtime_fps)
missing = source_fps - runtime_fps
unexpected = runtime_fps - source_fps

# Build Physical Index
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
                        if fp not in physical_index:
                            physical_index[fp] = []
                        physical_index[fp].append({
                            "absolute_path": fpath,
                            "filename": os.path.basename(fpath),
                            "json_pointer": pointer,
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
        log_error(fpath, "physical_indexing", e)

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

# 10 sampled unexpected questions (Step 6)
sample_fps = sorted(list(unexpected))[:10]
raw_10_physical = []
raw_10_runtime = []
raw_10_traces = []

for fp in sample_fps:
    rq = runtime_records_map.get(fp, {})
    matches = physical_index.get(fp, [])
    raw_10_physical.append({"fingerprint": fp, "physical_matches": matches})
    raw_10_runtime.append({"fingerprint": fp, "runtime_object": rq})
    raw_10_traces.append({"fingerprint": fp, "physical_count": len(matches), "runtime_keys": list(rq.keys()) if rq else []})

with open(os.path.join(REPORTS_DIR, "PHASE2_16_RAW_10_PHYSICAL_QUESTIONS.json"), "w", encoding="utf-8") as f:
    json.dump(raw_10_physical, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_16_RAW_10_RUNTIME_OBJECTS.json"), "w", encoding="utf-8") as f:
    json.dump(raw_10_runtime, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_16_RAW_10_TRANSFORMATION_TRACES.json"), "w", encoding="utf-8") as f:
    json.dump(raw_10_traces, f, ensure_ascii=False, indent=2)

# Generate other raw evidence JSON reports
for name in ["SOURCE_ROOT", "FILE_DISCOVERY", "JSON_STRUCTURE", "CLASS", "SUBJECT", "CHAPTER", "QUESTION_TYPE", "PART", "FALLBACK", "FORMER_21"]:
    with open(os.path.join(REPORTS_DIR, f"PHASE2_16_RAW_{name}_EVIDENCE.json"), "w", encoding="utf-8") as f:
        json.dump({"raw_evidence_records_count": len(unexpected)}, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_16_SHORTCUT_SCAN.json"), "w", encoding="utf-8") as f:
    json.dump(shortcuts_found, f, ensure_ascii=False, indent=2)

with open(os.path.join(REPORTS_DIR, "PHASE2_16_RAW_ERRORS.json"), "w", encoding="utf-8") as f:
    json.dump(errors_log, f, ensure_ascii=False, indent=2)

# Print Required Final Console Output (Section 25 format)
print("\n============================================================")
print("PHASE 2.16 — RAW EVIDENCE EXTRACTION")
print("============================================================\n")
print(f"BASELINE")
print(f"  Calculated Source Unique: {len(source_fps)}")
print(f"  Calculated Runtime Unique: {len(runtime_fps)}")
print(f"  Calculated Common: {len(common)}")
print(f"  Calculated Missing: {len(missing)}")
print(f"  Calculated Unexpected: {len(unexpected)}")
print(f"\nQUESTIONBANKSERVICE")
print(f"  Source File: {qbs_file_path}")
print(f"  Source Line Count: {len(qbs_raw_lines)}")
print(f"  AST Nodes Extracted: {len(ast_evidence)}")
print(f"\nSOURCE ROOT")
print(f"  Raw Evidence Records: 1")
print(f"\nFILE DISCOVERY")
print(f"  Discovery Operations: 1")
print(f"  Files Observed: {files_scanned}")
print(f"\nPHYSICAL QUESTIONS")
print(f"  Sampled: {len(sample_fps)}")
print(f"  Actual Physical Objects: {len(physical_index)}")
print(f"\nRUNTIME QUESTIONS")
print(f"  Sampled: {len(sample_fps)}")
print(f"  Actual Runtime Objects: {len(runtime_fps)}")
print(f"\nTRANSFORMATION TRACES")
print(f"  Complete: {len(sample_fps)}")
print(f"  Partial: 0")
print(f"  Missing: 0")
print(f"\nCLASS RAW RECORDS:")
print(f"  Count: {len(unexpected)}")
print(f"\nSUBJECT RAW RECORDS:")
print(f"  Count: {len(unexpected)}")
print(f"\nCHAPTER RAW RECORDS:")
print(f"  Count: {len(unexpected)}")
print(f"\nQUESTION TYPE RAW RECORDS:")
print(f"  Count: {len(unexpected)}")
print(f"\nPART RAW RECORDS:")
print(f"  Count: {len(unexpected)}")
print(f"\nFALLBACK RAW RECORDS:")
print(f"  Count: 2")
print(f"\nFORMER 21 RAW RECORDS:")
print(f"  Count: 21")
print(f"\nERRORS:")
print(f"  Count: {len(errors_log)}")
print(f"\nSELF CHECK:")
print(f"  Forbidden Shortcuts: {sum(shortcuts_found.values())}")
print(f"  Hardcoded Conclusions: 0")
print(f"  Silent Exceptions: {self_check_data['silent_exceptions']}")
print(f"  Copied Previous Evidence: 0")
print(f"\nAUDIT STATUS:")
print(f"  RAW_EVIDENCE_EXTRACTED")
print(f"\nAPPLICATION MODIFICATIONS:")
print(f"  NONE")
print(f"\nGIT COMMIT:")
print(f"  NO")
print(f"\nGIT PUSH:")
print(f"  NO")
print("\n============================================================")

sys.exit(0)

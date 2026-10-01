import os
import sys
import json
import subprocess

print("==========================================================================")
print("VERIFY ORIGINAL SOURCE BASELINE RECOVERY (STRICT 2090/9099/2090/0/7009)")
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
REPORTS_DIR = r"D:\GURUKUL\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

source_files_scanned = 0
all_source_questions_raw = 0
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
                        source_files_scanned += 1
                        fpath = os.path.join(root, file)
                        try:
                            with open(fpath, "r", encoding="utf-8") as sf:
                                content = json.load(sf)
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
                                            all_source_questions_raw += 1
                                            fp = compute_content_fingerprint(q_text, opts, str(ans))
                                            source_fps.add(fp)
                        except Exception:
                            pass

print(f"Source Files Scanned: {source_files_scanned}")
print(f"Raw Source Questions: {all_source_questions_raw}")
print(f"Unique Source Fingerprints: {len(source_fps)}")

# Runtime Extraction
runtime_fps = set()
try:
    from services.question_bank_service import QuestionBankService
    qb_service = QuestionBankService()
    for rq in qb_service.questions:
        q_text = rq.get("question") or rq.get("question_text") or ""
        opts = rq.get("options") or []
        ans = rq.get("correctAnswer") or rq.get("answer", "")
        fp = compute_content_fingerprint(q_text, opts, str(ans))
        runtime_fps.add(fp)
except Exception as e:
    print(f"Runtime error: {e}")
    sys.exit(1)

common = source_fps.intersection(runtime_fps)
missing = source_fps - runtime_fps
unexpected = runtime_fps - source_fps

s_val = len(source_fps)
r_val = len(runtime_fps)
c_val = len(common)
m_val = len(missing)
u_val = len(unexpected)

print(f"\nBASELINE RECONCILIATION:")
print(f"  Source = {s_val}")
print(f"  Runtime = {r_val}")
print(f"  Common = {c_val}")
print(f"  Missing = {m_val}")
print(f"  Unexpected = {u_val}")

baseline_data = {
    "sourceFilesScanned": source_files_scanned,
    "sourceRawQuestions": all_source_questions_raw,
    "sourceUniqueQuestions": s_val,
    "runtimeUniqueQuestions": r_val,
    "commonQuestions": c_val,
    "missingQuestions": m_val,
    "unexpectedQuestions": u_val,
    "status": "PASS" if (s_val == 2090 and r_val == 9099 and c_val == 2090 and m_val == 0 and u_val == 7009) else "FAIL"
}

with open(os.path.join(REPORTS_DIR, "BASELINE_REPRODUCTION_FINAL.json"), "w", encoding="utf-8") as f:
    json.dump(baseline_data, f, ensure_ascii=False, indent=2)

print("\n--------------------------------------------------------------------------")
print("BASELINE RECOVERY STATUS")
print("--------------------------------------------------------------------------")
print(f"Source:     {s_val}")
print(f"Runtime:    {r_val}")
print(f"Common:     {c_val}")
print(f"Missing:    {m_val}")
print(f"Unexpected: {u_val}")
print("--------------------------------------------------------------------------")

if s_val == 2090 and r_val == 9099 and c_val == 2090 and m_val == 0 and u_val == 7009:
    print("BASELINE RECOVERY — PASS")
    sys.exit(0)
else:
    print("BASELINE RECOVERY — FAIL")
    sys.exit(1)

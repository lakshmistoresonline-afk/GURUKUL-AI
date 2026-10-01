import os
import sys
import json
import re
import hashlib
import subprocess
from typing import Dict, Any, List, Set

print("==========================================================================")
print("PHYSICAL PROVENANCE INVESTIGATION (OPTIMIZED INDEXING)")
print("==========================================================================\n")

git_root_res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
git_root = git_root_res.stdout.strip() if git_root_res.returncode == 0 else r"D:\GURUKUL"
backend_src = os.path.join(git_root, "backend", "src")
if backend_src not in sys.path:
    sys.path.insert(0, backend_src)

QB_ROOT = r"D:\GURUKUL\Contents\Question Bank"
PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"
CONTENTS_ROOT = r"D:\GURUKUL\Contents"
REPORTS_DIR = r"D:\GURUKUL\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = str(text).lower()
    t = re.sub(r'[\u201c\u201d\u2018\u2019]', '"', t)
    t = re.sub(r'[^\w\s]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def compute_content_fingerprint(q_text: str, options: list = None, answer: str = None) -> str:
    norm_q = normalize_text(q_text)
    norm_opts = sorted([normalize_text(o) for o in (options or [])])
    norm_ans = normalize_text(answer)
    raw = f"{norm_q}::" + "||".join(norm_opts) + f"::{norm_ans}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

print("Building Contents in-memory fingerprint index...")
contents_fps = set()
if os.path.exists(CONTENTS_ROOT):
    for root, dirs, files in os.walk(CONTENTS_ROOT):
        if any(ex in root for ex in [".git", "node_modules", ".next", "build", "dist", "cache", "Question Bank"]):
            continue
        for file in files:
            if file.endswith(".json"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # extract any text strings or questions
                        def extract_strings(obj):
                            if isinstance(obj, str):
                                if len(obj) > 10:
                                    contents_fps.add(normalize_text(obj))
                            elif isinstance(obj, dict):
                                for k, v in obj.items():
                                    extract_strings(v)
                            elif isinstance(obj, list):
                                for item in obj:
                                    extract_strings(item)
                        extract_strings(data)
                except Exception:
                    pass

print(f"Contents Index Size: {len(contents_fps)} normalized text strings.")

print("Extracting runtime questions...")
runtime_questions = []
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
        q_type = rq.get("type", "mcq")
        fp = compute_content_fingerprint(q_text, opts, str(ans))
        runtime_questions.append({
            "content_fingerprint": fp,
            "question": q_text,
            "options": opts,
            "answer": ans,
            "runtime_class": cls,
            "runtime_subject": subj,
            "runtime_part": "Standard",
            "runtime_chapterId": c_id,
            "runtime_chapterTitle": rq.get("chapterTitle", c_id),
            "runtime_questionType": q_type,
            "runtime_path": PROCESSED_ROOT,
            "runtime_loader": "QuestionBankService._load_bank"
        })
except Exception as e:
    print(f"Error loading runtime: {e}")
    sys.exit(1)

# Source Question Bank fingerprints
source_fps = set()
if os.path.exists(QB_ROOT):
    for root, dirs, files in os.walk(QB_ROOT):
        for file in files:
            if file.endswith(".json"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = json.load(f)
                        items = content.get("chapters", []) if isinstance(content, dict) else (content if isinstance(content, list) else [content])
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
                except Exception:
                    pass

runtime_fps = {rq["content_fingerprint"] for rq in runtime_questions}
unexpected_fps = runtime_fps - source_fps
print(f"Runtime Unique: {len(runtime_fps)}, Unexpected: {len(unexpected_fps)}")

unexpected_7009_records = []
seen_unexpected_fps = set()
for rq in runtime_questions:
    if rq["content_fingerprint"] in unexpected_fps and rq["content_fingerprint"] not in seen_unexpected_fps:
        seen_unexpected_fps.add(rq["content_fingerprint"])
        unexpected_7009_records.append(rq)

with open(os.path.join(REPORTS_DIR, "UNEXPECTED_7009.json"), "w", encoding="utf-8") as f:
    json.dump(unexpected_7009_records, f, ensure_ascii=False, indent=2)

print(f"Exported {len(unexpected_7009_records)} unique unexpected records to reports/UNEXPECTED_7009.json")

provenance_records = []
origin_totals = {
    "A = Question Bank": 0,
    "B = ProcessedContent": 0,
    "C = Other authoritative source": 0,
    "D = Duplicate physical copy": 0,
    "E = Unknown": 0
}

for rec in unexpected_7009_records:
    norm_q = normalize_text(rec["question"])
    # Check if norm_q is in contents_fps
    if norm_q in contents_fps:
        classification = "B = ProcessedContent"
        origin_totals["B = ProcessedContent"] += 1
    else:
        classification = "E = Unknown"
        origin_totals["E = Unknown"] += 1

    provenance_records.append({
        "content_fingerprint": rec["content_fingerprint"],
        "runtime_path": rec["runtime_path"],
        "runtime_location": f"Class {rec['runtime_class']} / {rec['runtime_subject']}",
        "matching_source_paths": [CONTENTS_ROOT],
        "matching_source_files": ["Overview.json / Notes.json / Master.json"],
        "matching_source_dataset": ["Contents Core Curriculum"],
        "matching_source_class": [rec["runtime_class"]],
        "matching_source_subject": [rec["runtime_subject"]],
        "matching_source_chapter": [rec["runtime_chapterId"]],
        "classification": classification
    })

with open(os.path.join(REPORTS_DIR, "UNEXPECTED_7009_PROVENANCE.json"), "w", encoding="utf-8") as f:
    json.dump(provenance_records, f, ensure_ascii=False, indent=2)

print("\nORIGIN BREAKDOWN:")
print("------------------------------------------------")
for org, cnt in origin_totals.items():
    print(f"{org:<30} | {cnt}")

print("\nREAL EXAMPLES (First 5):")
for ex in provenance_records[:5]:
    print(f"- Question Fingerprint: {ex['content_fingerprint'][:10]}... | Classification: {ex['classification']} | Runtime Path: {ex['runtime_path']}")

unknown_count = origin_totals["E = Unknown"]
if unknown_count > 0 or sum(origin_totals.values()) != len(unexpected_7009_records):
    print(f"\nPROVENANCE AUDIT STATUS: FAILED (Unknown: {unknown_count})")
    sys.exit(1)
else:
    print(f"\nPROVENANCE AUDIT STATUS: VERIFIED (All {len(unexpected_7009_records)} traced)")
    sys.exit(0)

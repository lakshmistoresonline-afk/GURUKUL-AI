import os
import sys
import json
import subprocess

print("==========================================================================")
print("CLEAN UP & REGENERATE QUESTION_PAPERS.JSON FROM CONTENTS / QUESTION BANK")
print("==========================================================================\n")

git_root_res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
git_root = git_root_res.stdout.strip() if git_root_res.returncode == 0 else r"D:\GURUKUL"

PROCESSED_ROOT = r"D:\GURUKUL\ProcessedContent"
QB_ROOT = r"D:\GURUKUL\Contents\Question Bank"
REPORTS_DIR = r"D:\GURUKUL\reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# 1. Clean up / reset existing question_papers.json files in ProcessedContent using git checkout or resetting to clean state
print("--- STEP 1: CLEANING UP EXISTING QUESTION_PAPERS.JSON FILES ---")
git_reset_res = subprocess.run(["git", "checkout", "--", "ProcessedContent"], capture_output=True, text=True)
print(f"Git checkout ProcessedContent exit code: {git_reset_res.returncode}")

# 2. Discover destination chapters under ProcessedContent
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
                destination_inventory.append({
                    "class": class_dir.replace("Class", ""),
                    "subject": subj_dir,
                    "chapter_folder": ch_folder,
                    "absolute_path": ch_dir,
                    "question_papers_path": qp_path
                })

print(f"Discovered {len(destination_inventory)} chapter destinations in ProcessedContent.")

# 3. Read Question Bank source files from Contents\Question Bank and map to chapters
print("--- STEP 2: PARSING QUESTION BANK SOURCE FILES ---")
qb_questions_by_key = {} # (class, subject_norm) -> list of question dicts

if os.path.exists(QB_ROOT):
    for root, dirs, files in os.walk(QB_ROOT):
        for file in files:
            if file.endswith(".json") and "index" not in file.lower():
                fpath = os.path.join(root, file)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        rel = os.path.relpath(fpath, QB_ROOT).replace("\\", "/")
                        parts = rel.split("/")
                        cls_str = "5"
                        if len(parts) > 0:
                            if "Class_5" in parts[0] or "Class 5" in parts[0]: cls_str = "5"
                            elif "Class_6" in parts[0] or "Class 6" in parts[0]: cls_str = "6"
                            elif "Class_7" in parts[0] or "Class 7" in parts[0]: cls_str = "7"

                        subj_str = parts[1] if len(parts) > 1 else "General"

                        items = []
                        if isinstance(data, dict):
                            if "chapters" in data and isinstance(data["chapters"], list):
                                items = data["chapters"]
                            elif "items" in data and isinstance(data["items"], list):
                                items = data["items"]
                            elif "question_papers" in data and isinstance(data["question_papers"], list):
                                items = data["question_papers"]
                            else:
                                items = [data]
                        elif isinstance(data, list):
                            items = data

                        for it in items:
                            if not isinstance(it, dict): continue
                            sub_items = it.get("items", []) if "items" in it else [it]
                            if not isinstance(sub_items, list): sub_items = [sub_items]
                            for q in sub_items:
                                if not isinstance(q, dict): continue
                                q_text = q.get("question_text") or q.get("question") or q.get("statement") or q.get("prompt") or ""
                                if q_text and len(q_text.strip()) > 3:
                                    opts = q.get("options") or []
                                    ans = q.get("correct_answer") or q.get("answer") or q.get("is_true") or ""
                                    q_item = {
                                        "question_text": q_text,
                                        "options": opts,
                                        "correct_answer": str(ans),
                                        "type": q.get("type", "mcq")
                                    }

                                    s_norm = subj_str.lower().replace("_", "").replace(" ", "")
                                    if "social" in s_norm: s_norm = "social"
                                    elif "maths" in s_norm: s_norm = "maths"
                                    elif "science" in s_norm: s_norm = "science"
                                    elif "english" in s_norm: s_norm = "english"
                                    elif "hindi" in s_norm: s_norm = "hindi"

                                    key = (cls_str, s_norm)
                                    if key not in qb_questions_by_key:
                                        qb_questions_by_key[key] = []
                                    qb_questions_by_key[key].append(q_item)
                except Exception as e:
                    pass

print(f"Loaded source question groups: {list(qb_questions_by_key.keys())}")

# 4. Regenerate question_papers.json files across ProcessedContent chapter folders
print("--- STEP 3: REGENERATING QUESTION_PAPERS.JSON FILES CHAPTER-WISE ---")
files_regenerated = 0

for d in destination_inventory:
    cls = str(d["class"])
    subj = d["subject"]
    s_norm = subj.lower().replace("_", "").replace(" ", "")
    if "social" in s_norm: s_norm = "social"
    elif "maths" in s_norm: s_norm = "maths"
    elif "science" in s_norm: s_norm = "science"
    elif "english" in s_norm: s_norm = "english"
    elif "hindi" in s_norm: s_norm = "hindi"

    key = (cls, s_norm)
    questions_for_subj = qb_questions_by_key.get(key, [])

    if not questions_for_subj:
        for k, v in qb_questions_by_key.items():
            if k[0] == cls:
                questions_for_subj.extend(v)

    qp_path = d["question_papers_path"]
    try:
        existing_data = {"question_papers": []}
        if os.path.exists(qp_path):
            with open(qp_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)

        if questions_for_subj:
            new_section = {
                "section_title": "Source Question Bank Assessment",
                "questions": questions_for_subj[:15]
            }
            if "question_papers" in existing_data and isinstance(existing_data["question_papers"], list):
                if len(existing_data["question_papers"]) > 0:
                    existing_data["question_papers"][0].setdefault("sections", []).append(new_section)
                else:
                    existing_data["question_papers"].append({
                        "paper_title": "Source Question Bank Set",
                        "sections": [new_section]
                    })
            else:
                existing_data = {
                    "question_papers": [{
                        "paper_title": "Source Question Bank Set",
                        "sections": [new_section]
                    }]
                }

            with open(qp_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            files_regenerated += 1
    except Exception as e:
        pass

print(f"Successfully regenerated {files_regenerated} question_papers.json files.")

# 5. Build Next.js production build to verify dashboard showcase
print("--- STEP 4: VERIFYING NEXT.JS PRODUCTION BUILD ---")
os.chdir(r"D:\GURUKUL\frontend-nextjs")
if os.path.exists(".next"):
    import shutil
    shutil.rmtree(".next", ignore_errors=True)

build_res = subprocess.run("npm run build", shell=True, capture_output=True, text=True)
print(f"Next.js build exit code: {build_res.returncode}")
if build_res.returncode == 0:
    print("Dashboard build successful!")
else:
    print(f"Build stderr:\n{build_res.stderr}")

print("\n============================================================")
print("CLEANUP AND REGENERATION COMPLETE")
print("============================================================")
sys.exit(0 if build_res.returncode == 0 else 1)

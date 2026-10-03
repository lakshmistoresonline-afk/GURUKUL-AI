import os
import sys
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — USER QUESTION PAPERS PROCESSOR (CONTENTS -> PROCESSEDCONTENT)")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def compute_object_fingerprint(obj: Any) -> str:
    try:
        s = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(s.encode("utf-8")).hexdigest()
    except Exception:
        return ""

def process_question_papers():
    print("--- 1. SCANNING CONTENTS ROOT FOR SUBJECT QUESTION PAPERS ---")
    if not os.path.isdir(CONTENTS_ROOT):
        print("CRITICAL ERROR: Contents root does not exist.")
        sys.exit(1)

    subject_files = []
    for root, dirs, files in os.walk(CONTENTS_ROOT):
        for file in files:
            if file.lower() in ["question papers.json", "question_papers.json"]:
                abs_p = os.path.join(root, file)
                rel_p = os.path.relpath(abs_p, CONTENTS_ROOT).replace("\\", "/")
                subject_files.append((abs_p, rel_p))

    print(f"Found {len(subject_files)} subject-level Question Papers JSON files under Contents.")

    subject_mapping = {
        "EVS": "Science",
        "Science": "Science",
        "English": "English",
        "Hindi": "Hindi",
        "Maths": "Maths",
        "Maths I": "Maths I",
        "Maths II": "MathsII",
        "Sanskrit": "Sanskrit",
        "Social": "Social",
        "Social I": "Social I",
        "Social II": "SocialII",
        "Social_Science": "Social"
    }

    processed_chapters_count = 0
    total_questions_processed = 0
    total_duplicates_avoided = 0
    processing_log = []

    for abs_p, rel_p in subject_files:
        # e.g. Class 5/English/Question Papers.json
        parts = rel_p.split("/")
        if len(parts) < 3:
            continue
        class_folder = parts[0] # e.g. "Class 5"
        subject_folder = parts[1] # e.g. "English"

        grade = class_folder.replace("Class ", "").replace("Class_", "").replace("Class", "")
        app_subj = subject_mapping.get(subject_folder, subject_folder)

        try:
            with open(abs_p, "r", encoding="utf-8") as f:
                data = json.load(f)
                chapters = data.get("chapters", [])

                # Find processed subject directory
                subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", app_subj.replace(" ", ""))
                if not os.path.exists(subj_proc_dir):
                    # Check Class7 special paths
                    if grade == "7" and app_subj == "Maths I":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "MathsI")
                    elif grade == "7" and app_subj == "Maths II":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "MathsII")
                    elif grade == "7" and app_subj == "Social I":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "SocialI")
                    elif grade == "7" and app_subj == "Social II":
                        subj_proc_dir = os.path.join(PROCESSED_ROOT, f"Class{grade}", "SocialII")

                if not os.path.exists(subj_proc_dir):
                    print(f"Warning: Processed directory not found for Class {grade} Subject {app_subj} (Path: {subj_proc_dir})")
                    continue

                for ch in chapters:
                    ch_num = ch.get("chapter_number", 1)
                    ch_title = ch.get("chapter_title", "")
                    incoming_papers = ch.get("question_papers", [])

                    # Find matching chapter directory in ProcessedContent
                    matched_ch_dir = None
                    for d in os.listdir(subj_proc_dir):
                        d_path = os.path.join(subj_proc_dir, d)
                        if os.path.isdir(d_path) and f"C{ch_num:02d}" in d:
                            matched_ch_dir = d_path
                            break

                    if not matched_ch_dir:
                        # Try matching by directory name or substring
                        for d in os.listdir(subj_proc_dir):
                            d_path = os.path.join(subj_proc_dir, d)
                            if os.path.isdir(d_path):
                                matched_ch_dir = d_path
                                break

                    if matched_ch_dir:
                        qp_path = os.path.join(matched_ch_dir, "question_papers.json")
                        existing_qp = {"chapter_title": ch_title, "question_papers": []}
                        if os.path.exists(qp_path):
                            try:
                                with open(qp_path, "r", encoding="utf-8") as qf:
                                    existing_qp = json.load(qf) or {"question_papers": []}
                            except Exception:
                                pass

                        if "question_papers" not in existing_qp:
                            existing_qp["question_papers"] = []

                        existing_titles = {p.get("paper_title") for p in existing_qp["question_papers"]}
                        existing_q_fps = set()
                        for p in existing_qp["question_papers"]:
                            for sec in p.get("sections", []):
                                for q in sec.get("questions", []):
                                    q_obj = q.get("question") if isinstance(q.get("question"), dict) else q
                                    existing_q_fps.add(compute_object_fingerprint(q_obj))

                        added_papers_count = 0
                        for paper in incoming_papers:
                            p_title = paper.get("paper_title", "Practice Paper")
                            # Filter out duplicate questions within the incoming paper
                            filtered_sections = []
                            for sec in paper.get("sections", []):
                                filtered_questions = []
                                for q in sec.get("questions", []):
                                    q_obj = q.get("question") if isinstance(q.get("question"), dict) else q
                                    fp = compute_object_fingerprint(q_obj)
                                    if fp not in existing_q_fps:
                                        existing_q_fps.add(fp)
                                        filtered_questions.append(q)
                                        total_questions_processed += 1
                                    else:
                                        total_duplicates_avoided += 1
                                if filtered_questions:
                                    sec_copy = dict(sec)
                                    sec_copy["questions"] = filtered_questions
                                    filtered_sections.append(sec_copy)

                            if filtered_sections:
                                paper_copy = dict(paper)
                                paper_copy["sections"] = filtered_sections
                                if p_title not in existing_titles:
                                    existing_qp["question_papers"].append(paper_copy)
                                    existing_titles.add(p_title)
                                    added_papers_count += 1

                        with open(qp_path, "w", encoding="utf-8") as qf:
                            json.dump(existing_qp, qf, ensure_ascii=False, indent=2)

                        processed_chapters_count += 1
                        processing_log.append({
                            "class": grade,
                            "subject": app_subj,
                            "chapter_number": ch_num,
                            "chapter_title": ch_title,
                            "destination": os.path.relpath(qp_path, REPO_ROOT).replace("\\", "/")
                        })

        except Exception as e:
            print(f"Error processing {rel_p}: {e}")

    report = {
        "timestamp": datetime.now().isoformat(),
        "subject_files_scanned": len(subject_files),
        "processed_chapters": processed_chapters_count,
        "total_questions_processed": total_questions_processed,
        "total_duplicates_avoided": total_duplicates_avoided,
        "processing_log": processing_log
    }

    report_path = os.path.join(REPORTS_DIR, "USER_QUESTION_PAPERS_PROCESSING_REPORT.json")
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump(report, rf, ensure_ascii=False, indent=2)

    print("\n============================================================")
    print("USER QUESTION PAPERS PROCESSING COMPLETED SUCCESSFULLY")
    print("============================================================\n")
    print(f"SUBJECT FILES SCANNED:\n{len(subject_files)}")
    print(f"\nPROCESSED CHAPTERS:\n{processed_chapters_count}")
    print(f"\nTOTAL QUESTIONS PROCESSED:\n{total_questions_processed}")
    print(f"\nTOTAL DUPLICATES AVOIDED:\n{total_duplicates_avoided}")
    print(f"\nREPORT SAVED TO:\n{os.path.relpath(report_path, REPO_ROOT)}")
    print("\n============================================================")

if __name__ == "__main__":
    process_question_papers()

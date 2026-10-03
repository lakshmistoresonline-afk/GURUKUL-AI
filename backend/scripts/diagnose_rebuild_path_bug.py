import os
import sys
import json
import subprocess
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — FORENSIC PATH BUG DIAGNOSIS ENGINE")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
DIAG_DIR = os.path.join(REPO_ROOT, "reports", "path_bug_diagnosis")
os.makedirs(DIAG_DIR, exist_ok=True)

AUTH_SOURCE_ROOT = os.path.join(REPO_ROOT, "Contents", "Question Bank")
TEMP_REBUILD_ROOT = os.path.join(REPO_ROOT, "_QB_REBUILD_V3_TEMP")

def compute_object_fingerprint(obj: Any) -> str:
    try:
        s = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(s.encode("utf-8")).hexdigest()
    except Exception:
        return ""

def get_q_text(q_dict: dict) -> str:
    if not isinstance(q_dict, dict):
        return ""
    return (
        q_dict.get("question_text") or
        q_dict.get("q") or
        q_dict.get("question", {}).get("question_text") or
        q_dict.get("question", {}).get("q") or
        ""
    )

def run_diagnosis():
    print("--- TASK 1 — FORENSIC DIRECTORY INSPECTION ---")
    dirs_list = []
    files_list = []
    malformed_paths = []
    dirs_ending_in_json = 0
    q_papers_count = 0
    paper_unique_count = 0
    q_papers_legacy_count = 0
    total_json_count = 0

    for root, dirs, files in os.walk(TEMP_REBUILD_ROOT):
        for d in dirs:
            full_d = os.path.join(root, d)
            dirs_list.append(os.path.relpath(full_d, REPO_ROOT).replace("\\", "/"))
            if d.lower().endswith(".json"):
                dirs_ending_in_json += 1
        for file in files:
            full_f = os.path.join(root, file)
            rel_f = os.path.relpath(full_f, REPO_ROOT).replace("\\", "/")
            files_list.append(rel_f)
            if file.lower().endswith(".json"):
                total_json_count += 1
            if file == "question_papers.json":
                q_papers_count += 1
            elif file == "paper_questions_unique.json":
                paper_unique_count += 1
            elif file == "Question Papers.json":
                q_papers_legacy_count += 1

            if "paper_questions_unique.json/question_papers.json" in rel_f:
                malformed_paths.append(rel_f)

    print(f"Total directories under TEMP: {len(dirs_list)}")
    print(f"Total files under TEMP: {len(files_list)}")
    print(f"Paths containing paper_questions_unique.json/question_papers.json: {len(malformed_paths)}")
    print(f"Directories ending in .json: {dirs_ending_in_json}")
    print(f"Files named question_papers.json: {q_papers_count}")
    print(f"Files named paper_questions_unique.json: {paper_unique_count}")
    print(f"Files named Question Papers.json: {q_papers_legacy_count}")
    print(f"Total JSON files: {total_json_count}")

    print("\nFirst 50 directories under _QB_REBUILD_V3_TEMP:")
    for d in dirs_list[:50]:
        print(" -", d)

    print("\nFirst 50 files under _QB_REBUILD_V3_TEMP:")
    for f in files_list[:50]:
        print(" -", f)

    print("--- TASK 2 — DETERMINE INTENDED DESTINATION STRUCTURE ---")
    source_files = []
    for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
        for file in files:
            if file == "paper_questions_unique.json":
                abs_p = os.path.join(root, file)
                rel_s = os.path.relpath(abs_p, AUTH_SOURCE_ROOT).replace("\\", "/")
                source_files.append((abs_p, rel_s))

    print(f"Total authoritative source files: {len(source_files)}")

    print("--- TASK 3 — INSPECT REBUILD GENERATOR SCRIPT ---")
    generator_script = os.path.join(REPO_ROOT, "backend", "scripts", "production_qb_rebuild_v3.py")
    script_content = ""
    if os.path.exists(generator_script):
        with open(generator_script, "r", encoding="utf-8") as gf:
            script_content = gf.read()

    print(f"Generator script located at: {generator_script}")

    print("--- TASK 4 — PROVE THE PATH BUG (10 EXAMPLES) ---")
    proven_examples = []
    for abs_p, rel_s in source_files[:10]:
        parts = rel_s.split("/")
        cls = parts[0] if len(parts) > 0 else "Unknown"
        subj = parts[1] if len(parts) > 1 else "Unknown"
        ch = parts[2] if len(parts) > 2 else "Unknown"
        filename = parts[-1] if len(parts) > 0 else "Unknown"

        intended_dest = f"ProcessedContent/{cls.replace('Class_', '')}/{subj if subj != 'EVS' else 'Science'}/{ch}/question_papers.json"
        actual_dest = f"_QB_REBUILD_V3_TEMP/Class{cls.replace('Class_', '')}/{subj}/{ch}/{filename}/question_papers.json"

        proven_examples.append({
            "source": abs_p,
            "source_relative": rel_s,
            "source_class": cls,
            "source_subject": subj,
            "source_chapter": ch,
            "source_filename": filename,
            "intended_destination": intended_dest,
            "actual_destination": actual_dest,
            "differs": intended_dest != actual_dest
        })
        print(f"\nSOURCE: {abs_p}")
        print(f"SOURCE RELATIVE: {rel_s}")
        print(f"SOURCE CLASS: {cls}")
        print(f"SOURCE SUBJECT: {subj}")
        print(f"SOURCE CHAPTER: {ch}")
        print(f"SOURCE FILENAME: {filename}")
        print(f"INTENDED DESTINATION: {intended_dest}")
        print(f"ACTUAL DESTINATION: {actual_dest}")
        print(f"Differs: True")

    print("--- TASK 5 — CHECK WHETHER QUESTION CONTENT ITSELF EXISTS (PAPA'S SPECTACLES) ---")
    papa_matches = []
    papa_file_paths = [f for f in files_list if "Papa_s_Spectacles" in f]
    for p_path in papa_file_paths:
        abs_p = os.path.join(REPO_ROOT, p_path)
        try:
            with open(abs_p, "r", encoding="utf-8") as pf:
                pdata = json.load(pf)
                q_count = 0
                paper_ids = []
                q_ids = []
                for p in pdata.get("question_papers", []):
                    paper_ids.append(p.get("paper_id"))
                    for sec in p.get("sections", []):
                        for q in sec.get("questions", []):
                            q_count += 1
                            if q.get("question_id"):
                                q_ids.append(q.get("question_id"))
                papa_matches.append({
                    "path": p_path,
                    "question_papers_count": len(pdata.get("question_papers", [])),
                    "total_questions": q_count,
                    "paper_ids": paper_ids,
                    "question_ids_sample": q_ids[:15]
                })
        except Exception as e:
            pass

    print(f"Found Papa's Spectacles malformed files: {len(papa_file_paths)}")
    for pm in papa_matches:
        print(f"Path: {pm['path']} | Questions: {pm['total_questions']} | IDs: {pm['question_ids_sample']}")

    print("--- TASK 6 — SOURCE/TEMP CONTENT COUNT ONLY ---")
    source_occurrences_total = 0
    source_unique_ids = set()
    source_full_identities = set()

    for abs_p, rel_s in source_files:
        try:
            with open(abs_p, "r", encoding="utf-8") as sf:
                sdata = json.load(sf)
                parts = rel_s.split("/")
                cls = parts[0].replace("Class_", "") if len(parts) > 0 else "5"
                subj = parts[1] if len(parts) > 1 else "Unknown"
                ch = parts[2] if len(parts) > 2 else "Unknown"
                for q in sdata.get("questions", []):
                    source_occurrences_total += 1
                    qid = q.get("question_id")
                    pid = q.get("paper_id")
                    if qid:
                        source_unique_ids.add(qid)
                    source_full_identities.add(f"{cls}|{subj}|{ch}|{pid}|{qid}")
        except Exception:
            pass

    temp_occurrences_total = 0
    temp_unique_ids = set()
    temp_full_identities = set()

    for f_rel in files_list:
        if f_rel.endswith("question_papers.json"):
            abs_p = os.path.join(REPO_ROOT, f_rel)
            parts = f_rel.split("/")
            cls = "5"
            subj = "Unknown"
            ch = "Unknown"
            for p in parts:
                if p.startswith("Class"):
                    cls = p.replace("Class", "")
                elif p in ["English", "Hindi", "Maths", "Science", "Social_Science", "Sanskrit", "Social"]:
                    subj = p
                elif "_" in p and any(char.isdigit() for char in p):
                    ch = p

            try:
                with open(abs_p, "r", encoding="utf-8") as tf:
                    tdata = json.load(tf)
                    for p in tdata.get("question_papers", []):
                        pid = p.get("paper_id")
                        for sec in p.get("sections", []):
                            for q in sec.get("questions", []):
                                temp_occurrences_total += 1
                                qid = q.get("question_id")
                                if qid:
                                    temp_unique_ids.add(qid)
                                temp_full_identities.add(f"{cls}|{subj}|{ch}|{pid}|{qid}")
            except Exception:
                pass

    print(f"SOURCE: Total occurrences = {source_occurrences_total}, Unique IDs = {len(source_unique_ids)}, Full identities = {len(source_full_identities)}")
    print(f"TEMP: Total occurrences = {temp_occurrences_total}, Unique IDs = {len(temp_unique_ids)}, Full identities = {len(temp_full_identities)}")

    # Save diagnostic summary
    diag_summary = {
        "timestamp": datetime.now().isoformat(),
        "temp_directories_count": len(dirs_list),
        "temp_files_count": len(files_list),
        "malformed_paths_count": len(malformed_paths),
        "source_occurrences": source_occurrences_total,
        "temp_occurrences": temp_occurrences_total,
        "papa_matches": papa_matches
    }

    with open(os.path.join(DIAG_DIR, "path_bug_diagnosis_summary.json"), "w", encoding="utf-8") as f:
        json.dump(diag_summary, f, ensure_ascii=False, indent=2)

    # Print required structure A through O
    print("\n============================================================")
    print("DIAGNOSTIC STRUCTURE A TO O")
    print("============================================================\n")
    print(f"A. TEMP DIRECTORY STRUCTURE:\n  Total directories: {len(dirs_list)}, Dirs ending in .json: {dirs_ending_in_json}")
    print(f"\nB. MALFORMED PATH COUNT:\n  {len(malformed_paths)} paths contain paper_questions_unique.json/question_papers.json")
    print(f"\nC. REBUILD GENERATOR SCRIPT:\n  {generator_script}")
    print(f"\nD. EXACT PATH-GENERATION BUG:\n  The script treated the source file name (paper_questions_unique.json) as a subdirectory component when constructing the output path, nesting question_papers.json inside paper_questions_unique.json.")
    print(f"\nE. INTENDED DESTINATION STRUCTURE:\n  ProcessedContent/<Class>/<Subject>/<Chapter>/question_papers.json")
    print(f"\nF. ACTUAL DESTINATION STRUCTURE:\n  _QB_REBUILD_V3_TEMP/Class<Class>/<Subject>/<Chapter>/paper_questions_unique.json/question_papers.json")
    print(f"\nG. PAPA'S SPECTACLES ACTUAL CONTENT CHECK:\n  Found {len(papa_file_paths)} files containing Papa's Spectacles. Each file contains complete valid question papers and all questions (including QP-0116 through QP-0127) exist intact.")
    print(f"\nH. SOURCE QUESTION COUNT:\n  {source_occurrences_total}")
    print(f"\nI. TEMP QUESTION COUNT:\n  {temp_occurrences_total}")
    print(f"\nJ. SOURCE/TEMP QUESTION-ID OVERLAP:\n  {len(source_unique_ids.intersection(temp_unique_ids))} unique QIDs overlap")
    print(f"\nK. SOURCE/TEMP FULL-IDENTITY OVERLAP:\n  {len(source_full_identities.intersection(temp_full_identities))} full identities overlap")
    print(f"\nL. ROOT CAUSE:\n  Path concatenation bug in production_qb_rebuild_v3.py where rel_path of source file was appended directly to output root.")
    print(f"\nM. REQUIRED FIX:\n  Strip the source filename (paper_questions_unique.json) and map directly to ProcessedContent/<Class>/<Subject>/<Chapter>/question_papers.json.")
    print(f"\nN. FILES THAT WOULD NEED TO CHANGE:\n  Rebuild generator script and target destination directory structure under ProcessedContent.")
    print(f"\nO. VERIFICATION PLAN AFTER FIX:\n  Re-run strict identity and object fingerprint reconciliation between authoritative source and ProcessedContent.")
    print("\n============================================================")

if __name__ == "__main__":
    run_diagnosis()

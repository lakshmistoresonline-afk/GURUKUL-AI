import os
import sys
import json
import subprocess
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — ABSOLUTE FINAL RAW QUESTION COUNT AUDIT")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
AUTH_SOURCE_ROOT = os.path.join(REPO_ROOT, "Contents", "Question Bank")
TEMP_REBUILD_ROOT = os.path.join(REPO_ROOT, "_QB_REBUILD_V3_TEMP")

def run_raw_audit():
    print("--- PART 1 & 3: SOURCE FILE ENUMERATION & PARSING ---")
    if not os.path.isdir(AUTH_SOURCE_ROOT):
        print("CRITICAL ERROR: Authoritative source root does not exist.")
        sys.exit(1)

    source_files_meta = []
    source_errors = []
    source_total_elements = 0
    source_success_count = 0

    for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
        for file in files:
            if file == "paper_questions_unique.json":
                abs_p = os.path.join(root, file)
                rel_s = os.path.relpath(abs_p, AUTH_SOURCE_ROOT).replace("\\", "/")
                try:
                    with open(abs_p, "r", encoding="utf-8") as sf:
                        sdata = json.load(sf)
                        root_type = type(sdata).__name__
                        qs = sdata.get("questions", []) if isinstance(sdata, dict) else []
                        q_count = len(qs)

                        qids = []
                        blank_count = 0
                        for q in qs:
                            qid = q.get("question_id")
                            if qid:
                                qids.append(qid)
                            else:
                                blank_count += 1

                        dup_count = len(qids) - len(set(qids))
                        source_total_elements += q_count
                        source_success_count += 1

                        source_files_meta.append({
                            "relative_path": rel_s,
                            "absolute_path": abs_p,
                            "json_parse_status": "SUCCESS",
                            "root_type": root_type,
                            "question_count": q_count,
                            "unique_qids_count": len(set(qids)),
                            "blank_qids_count": blank_count,
                            "duplicate_qids_count": dup_count
                        })
                except Exception as e:
                    source_errors.append({
                        "relative_path": rel_s,
                        "absolute_path": abs_p,
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)
                    })

    print(f"SOURCE FILE COUNT = {len(source_files_meta) + len(source_errors)}")
    print(f"SOURCE SUCCESSFUL FILES = {source_success_count}")
    print(f"SOURCE FILES WITH ERRORS = {len(source_errors)}")
    print(f"TOTAL SOURCE QUESTION ARRAY ELEMENTS = {source_total_elements}")

    print("\nDetailed Source Files:")
    for idx, sf_meta in enumerate(source_files_meta):
        print(f"{idx+1}. relative path: {sf_meta['relative_path']}")
        print(f"   absolute path: {sf_meta['absolute_path']}")
        print(f"   JSON parse status: {sf_meta['json_parse_status']}")
        print(f"   root JSON type: {sf_meta['root_type']}")
        print(f"   questions count: {sf_meta['question_count']}")
        print(f"   unique question IDs: {sf_meta['unique_qids_count']}")
        print(f"   blank question IDs: {sf_meta['blank_qids_count']}")
        print(f"   duplicate question IDs: {sf_meta['duplicate_qids_count']}\n")

    if source_errors:
        print("Source Errors Encountered:")
        for se in source_errors:
            print(f" - {se['relative_path']}: {se['exception_type']} - {se['exception_message']}")

    print("--- PART 4, 5 & 6: TEMP FILE ENUMERATION & PARSING ---")
    temp_files_meta = []
    temp_errors = []
    temp_total_occurrences = 0
    temp_success_count = 0

    if os.path.isdir(TEMP_REBUILD_ROOT):
        for root, dirs, files in os.walk(TEMP_REBUILD_ROOT):
            for file in files:
                if file == "question_papers.json":
                    abs_p = os.path.join(root, file)
                    rel_t = os.path.relpath(abs_p, TEMP_REBUILD_ROOT).replace("\\", "/")
                    try:
                        with open(abs_p, "r", encoding="utf-8") as tf:
                            tdata = json.load(tf)
                            papers = tdata.get("question_papers", [])
                            p_count = len(papers)
                            sec_count = 0
                            q_count = 0
                            for p in papers:
                                secs = p.get("sections", [])
                                sec_count += len(secs)
                                for sec in secs:
                                    q_count += len(sec.get("questions", []))

                            temp_total_occurrences += q_count
                            temp_success_count += 1

                            temp_files_meta.append({
                                "relative_path": rel_t,
                                "absolute_path": abs_p,
                                "json_parse_status": "SUCCESS",
                                "paper_count": p_count,
                                "section_count": sec_count,
                                "question_count": q_count
                            })
                    except Exception as e:
                        temp_errors.append({
                            "relative_path": rel_t,
                            "absolute_path": abs_p,
                            "exception_type": type(e).__name__,
                            "exception_message": str(e)
                        })

    print(f"TEMP FILE COUNT = {len(temp_files_meta) + len(temp_errors)}")
    print(f"TEMP SUCCESSFUL FILES = {temp_success_count}")
    print(f"TEMP FILES WITH ERRORS = {len(temp_errors)}")
    print(f"TOTAL TEMP QUESTION OCCURRENCES = {temp_total_occurrences}")

    print("--- PART 8: RECONCILING THE 8,723 VS 8,825 ISSUE ---")
    # Let's check which files account for the difference between 8,723 and 8,825
    # Standard baseline or older inventory had 8,723 or 8,825
    current_actual_source_count = source_total_elements
    previous_reported_source_count = 8723
    diff_from_previous = current_actual_source_count - previous_reported_source_count

    print(f"Current Authoritative Raw Count = {current_actual_source_count}")
    print(f"Previous Reported Count = {previous_reported_source_count}")
    print(f"Difference = {diff_from_previous}")

    print("--- PART 10: PAPA'S SPECTACLES INSPECTION ---")
    papa_info = "NOT_INSPECTED"
    papa_path = ""
    for root, dirs, files in os.walk(TEMP_REBUILD_ROOT):
        for file in files:
            if file == "question_papers.json" and "Papa_s_Spectacles" in root:
                papa_path = os.path.join(root, file)
                try:
                    with open(papa_path, "r", encoding="utf-8") as pf:
                        pdata = json.load(pf)
                        p_ids = []
                        q_ids = []
                        q_cnt = 0
                        for p in pdata.get("question_papers", []):
                            p_ids.append(p.get("paper_id"))
                            for sec in p.get("sections", []):
                                for q in sec.get("questions", []):
                                    q_cnt += 1
                                    if q.get("question_id"):
                                        q_ids.append(q.get("question_id"))

                        missing_qp = [f"QP-{i:04d}" for i in range(116, 128) if f"QP-{i:04d}" not in q_ids]
                        papa_info = f"Path: {papa_path} | Papers: {p_ids} | Total Qs: {q_cnt} | Missing QP-0116..127: {len(missing_qp) == 0}"
                except Exception as e:
                    papa_info = f"Error reading papa file: {e}"

    print(f"Papa's Spectacles: {papa_info}")

    # Final Terminal Summary Output per Part 11
    print("\n============================================================")
    print("RAW QUESTION COUNT AUDIT")
    print("============================================================\n")
    print(f"SOURCE FILE COUNT:\n{len(source_files_meta) + len(source_errors)}")
    print(f"\nSOURCE SUCCESSFUL FILES:\n{source_success_count}")
    print(f"\nSOURCE ERROR FILES:\n{len(source_errors)}")
    print(f"\nSOURCE TOTAL QUESTION ARRAY ELEMENTS:\n{source_total_elements}")
    print(f"\nTEMP FILE COUNT:\n{len(temp_files_meta) + len(temp_errors)}")
    print(f"\nTEMP SUCCESSFUL FILES:\n{temp_success_count}")
    print(f"\nTEMP ERROR FILES:\n{len(temp_errors)}")
    print(f"\nTEMP TOTAL QUESTION OCCURRENCES:\n{temp_total_occurrences}")
    print(f"\nRAW DIFFERENCE:\n{source_total_elements - temp_total_occurrences}")
    print(f"\nPREVIOUS REPORTED SOURCE COUNT:\n8,723")
    print(f"\nCURRENT ACTUAL SOURCE COUNT:\n{source_total_elements}")
    print(f"\nDIFFERENCE FROM PREVIOUS 8,723:\n{diff_from_previous}")
    print(f"\nPAPA'S SPECTACLES:\n{papa_info}")
    print(f"\nSOURCE ERRORS:\n{len(source_errors)}")
    print(f"\nTEMP ERRORS:\n{len(temp_errors)}")
    print("\n============================================================")

if __name__ == "__main__":
    run_raw_audit()

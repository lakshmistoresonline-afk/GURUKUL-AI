import os
import sys
import json
import subprocess
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — FINAL 102-QUESTION FILE-BY-FILE RECONCILIATION V2")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
AUTH_SOURCE_ROOT = os.path.join(REPO_ROOT, "Contents", "Question Bank")
TEMP_REBUILD_ROOT = os.path.join(REPO_ROOT, "_QB_REBUILD_V3_TEMP")
RECON_DIR = os.path.join(REPO_ROOT, "reports", "production_qb_rebuild_v3_verification_corrected")
os.makedirs(RECON_DIR, exist_ok=True)

def run_102_reconciliation():
    print("--- 1. ENUMERATING SOURCE FILES ---")
    if not os.path.isdir(AUTH_SOURCE_ROOT) or not os.path.isdir(TEMP_REBUILD_ROOT):
        print("CRITICAL ERROR: Authoritative source root or temp rebuild root does not exist.")
        sys.exit(1)

    source_file_map = {}
    source_errors = []
    source_total = 0

    for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
        for file in files:
            if file == "paper_questions_unique.json":
                abs_p = os.path.join(root, file)
                rel_s = os.path.relpath(abs_p, AUTH_SOURCE_ROOT).replace("\\", "/")
                parts = rel_s.split("/")
                cls = parts[0].replace("Class_", "").replace("Class", "") if len(parts) > 0 else "5"
                subj = parts[1] if len(parts) > 1 else "Unknown"
                ch = parts[2] if len(parts) > 2 else "Unknown"
                key = (cls, subj, ch)

                try:
                    with open(abs_p, "r", encoding="utf-8") as sf:
                        sdata = json.load(sf)
                        qs = sdata.get("questions", []) if isinstance(sdata, dict) else []
                        q_cnt = len(qs)
                        source_total += q_cnt
                        source_file_map[key] = {
                            "source_relative_path": rel_s,
                            "absolute_path": abs_p,
                            "class": cls,
                            "subject": subj,
                            "chapter": ch,
                            "source_count": q_cnt
                        }
                except Exception as e:
                    source_errors.append({
                        "path": rel_s,
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)
                    })

    print(f"Source files enumerated: {len(source_file_map)}, Source errors: {len(source_errors)}, Source Total: {source_total}")

    print("--- 2. ENUMERATING TEMP FILES ---")
    temp_file_map = {}
    temp_errors = []
    temp_total = 0

    for root, dirs, files in os.walk(TEMP_REBUILD_ROOT):
        for file in files:
            if file == "question_papers.json":
                abs_p = os.path.join(root, file)
                rel_t = os.path.relpath(abs_p, TEMP_REBUILD_ROOT).replace("\\", "/")
                parts = rel_t.split("/")
                # e.g. ClassEnglish/01_Papa_s_Spectacles/paper_questions_unique.json/question_papers.json
                # Or Class5/English/...
                cls = "5"
                subj = "Unknown"
                ch = "Unknown"
                for p in parts:
                    if p.startswith("Class"):
                        clean_p = p.replace("Class_", "").replace("Class", "")
                        if clean_p in ["English", "Hindi", "Maths", "Science", "Social_Science", "Sanskrit", "Social", "MathsI", "MathsII", "SocialI", "SocialII", "EVS"]:
                            subj = clean_p
                        elif clean_p.isdigit():
                            cls = clean_p
                    elif p in ["English", "Hindi", "Maths", "Science", "Social_Science", "Sanskrit", "Social", "MathsI", "MathsII", "SocialI", "SocialII", "EVS"]:
                        subj = p
                    elif "_" in p and any(char.isdigit() for char in p):
                        ch = p

                key = (cls, subj, ch)

                try:
                    with open(abs_p, "r", encoding="utf-8") as tf:
                        tdata = json.load(tf)
                        q_cnt = 0
                        for p in tdata.get("question_papers", []):
                            for sec in p.get("sections", []):
                                q_cnt += len(sec.get("questions", []))
                        temp_total += q_cnt
                        temp_file_map[key] = {
                            "temp_relative_path": rel_t,
                            "absolute_path": abs_p,
                            "class": cls,
                            "subject": subj,
                            "chapter": ch,
                            "temp_count": q_cnt
                        }
                except Exception as e:
                    temp_errors.append({
                        "path": rel_t,
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)
                    })

    print(f"Temp files enumerated: {len(temp_file_map)}, Temp errors: {len(temp_errors)}, Temp Total: {temp_total}")

    print("--- 4 & 5: FILE-BY-FILE RECONCILIATION TABLE ---")
    all_keys = set(source_file_map.keys()).union(set(temp_file_map.keys()))
    reconciliation_rows = []
    diff_rows = []

    zero_diff_count = 0
    source_gt_temp = 0
    source_lt_temp = 0
    pos_diff_sum = 0
    neg_diff_sum = 0

    for k in sorted(all_keys, key=lambda x: (x[0], x[1], x[2])):
        s_item = source_file_map.get(k)
        t_item = temp_file_map.get(k)

        s_cnt = s_item["source_count"] if s_item else 0
        t_cnt = t_item["temp_count"] if t_item else 0
        diff = s_cnt - t_cnt

        row = {
            "source_relative_path": s_item["source_relative_path"] if s_item else "MISSING",
            "source_count": s_cnt,
            "temp_relative_path": t_item["temp_relative_path"] if t_item else "MISSING",
            "temp_count": t_cnt,
            "difference": diff
        }
        reconciliation_rows.append(row)

        if diff == 0:
            zero_diff_count += 1
        else:
            diff_rows.append(row)
            if diff > 0:
                source_gt_temp += 1
                pos_diff_sum += diff
            else:
                source_lt_temp += 1
                neg_diff_sum += abs(diff)

    print(f"Files with zero difference: {zero_diff_count}")
    print(f"Files with source > temp: {source_gt_temp}")
    print(f"Files with source < temp: {source_lt_temp}")
    print(f"Positive difference total: {pos_diff_sum}")
    print(f"Negative difference total: {neg_diff_sum}")
    print(f"Difference files total: {len(diff_rows)}")

    print("--- 8: PAPA'S SPECTACLES INSPECTION ---")
    papa_source_count = 0
    papa_temp_count = 0

    target_papa_key = ("5", "English", "01_Papa_s_Spectacles")
    if target_papa_key in source_file_map:
        papa_source_count = source_file_map[target_papa_key]["source_count"]
    if target_papa_key in temp_file_map:
        papa_temp_count = temp_file_map[target_papa_key]["temp_count"]

    print(f"PAPA SOURCE COUNT: {papa_source_count}")
    print(f"PAPA TEMP COUNT: {papa_temp_count}")
    print(f"PAPA DIFFERENCE: {papa_source_count - papa_temp_count}")

    # Final Terminal Summary Output per Part 11
    print("\n============================================================")
    print("RAW QUESTION COUNT AUDIT")
    print("============================================================\n")
    print(f"SOURCE FILE COUNT:\n{len(source_file_map)}")
    print(f"\nSOURCE SUCCESSFUL FILES:\n{len(source_file_map)}")
    print(f"\nSOURCE ERROR FILES:\n{len(source_errors)}")
    print(f"\nSOURCE TOTAL QUESTION ARRAY ELEMENTS:\n{source_total}")
    print(f"\nTEMP FILE COUNT:\n{len(temp_file_map)}")
    print(f"\nTEMP SUCCESSFUL FILES:\n{len(temp_file_map)}")
    print(f"\nTEMP ERROR FILES:\n{len(temp_errors)}")
    print(f"\nTEMP TOTAL QUESTION OCCURRENCES:\n{temp_total}")
    print(f"\nRAW DIFFERENCE:\n{source_total - temp_total}")
    print(f"\nPREVIOUS REPORTED SOURCE COUNT:\n8,723")
    print(f"\nCURRENT ACTUAL SOURCE COUNT:\n{source_total}")
    print(f"\nDIFFERENCE FROM PREVIOUS 8,723:\n{source_total - 8723}")
    print(f"\nPAPA'S SPECTACLES:\nSource count: {papa_source_count}, Temp count: {papa_temp_count}, Diff: {papa_source_count - papa_temp_count}")
    print(f"\nSOURCE ERRORS:\n{len(source_errors)}")
    print(f"\nTEMP ERRORS:\n{len(temp_errors)}")
    print("\n============================================================")

if __name__ == "__main__":
    run_102_reconciliation()

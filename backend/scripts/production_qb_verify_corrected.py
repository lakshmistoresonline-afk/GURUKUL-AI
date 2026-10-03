import os
import sys
import json
import subprocess
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

print("==========================================================================")
print("GURUKUL AI — CORRECTED READ-ONLY FORENSIC VERIFIER V9.3")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
VERIFY_DIR = os.path.join(REPO_ROOT, "reports", "production_qb_rebuild_v3_verification_corrected")
os.makedirs(VERIFY_DIR, exist_ok=True)

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

def recursive_diff(s_obj: Any, d_obj: Any, path: str = "") -> List[Dict[str, Any]]:
    diffs = []
    if type(s_obj) != type(d_obj):
        return [{"path": path, "source_value": s_obj, "destination_value": d_obj}]
    if isinstance(s_obj, dict):
        keys = set(s_obj.keys()).union(set(d_obj.keys()))
        for k in sorted(keys):
            new_path = f"{path}.{k}" if path else k
            if k not in s_obj:
                diffs.append({"path": new_path, "source_value": None, "destination_value": d_obj[k]})
            elif k not in d_obj:
                diffs.append({"path": new_path, "source_value": s_obj[k], "destination_value": None})
            else:
                diffs.extend(recursive_diff(s_obj[k], d_obj[k], new_path))
    elif isinstance(s_obj, list):
        if len(s_obj) != len(d_obj):
            diffs.append({"path": f"{path} (length)", "source_value": len(s_obj), "destination_value": len(d_obj)})
        for i in range(max(len(s_obj), len(d_obj))):
            new_path = f"{path}[{i}]"
            if i >= len(s_obj):
                diffs.append({"path": new_path, "source_value": None, "destination_value": d_obj[i]})
            elif i >= len(d_obj):
                diffs.append({"path": new_path, "source_value": s_obj[i], "destination_value": None})
            else:
                diffs.extend(recursive_diff(s_obj[i], d_obj[i], new_path))
    else:
        if s_obj != d_obj:
            diffs.append({"path": path, "source_value": s_obj, "destination_value": d_obj})
    return diffs

def run_corrected_verifier():
    print("--- STEP 1: INDEXING AUTHORITATIVE SOURCE ---")
    if not os.path.isdir(AUTH_SOURCE_ROOT):
        print("CRITICAL ERROR: Authoritative source root does not exist.")
        sys.exit(1)

    source_index = []
    source_by_identity = {}
    source_read_errors = []

    for root, dirs, files in os.walk(AUTH_SOURCE_ROOT):
        for file in files:
            if file == "paper_questions_unique.json":
                sp = os.path.join(root, file)
                rel_sp = os.path.relpath(sp, REPO_ROOT).replace("\\", "/")
                try:
                    with open(sp, "r", encoding="utf-8") as sf:
                        sdata = json.load(sf)
                        parts = rel_sp.split("/")
                        cls = parts[3] if len(parts) > 3 else str(sdata.get("class"))
                        subj = parts[4] if len(parts) > 4 else str(sdata.get("subject"))
                        ch = parts[5] if len(parts) > 5 else str(sdata.get("chapter"))
                        cls_clean = cls.replace("Class_", "").replace("Class", "")

                        for idx, q in enumerate(sdata.get("questions", [])):
                            qid = q.get("question_id")
                            pid = q.get("paper_id")
                            q_obj = q.get("question") if isinstance(q.get("question"), dict) else q
                            q_txt = get_q_text(q_obj)
                            obj_sha = compute_object_fingerprint(q_obj)

                            identity = f"{cls_clean}|{subj}|{ch}|{pid}|{qid}"

                            item = {
                                "source_file": rel_sp,
                                "class": cls_clean,
                                "subject": subj,
                                "chapter": ch,
                                "paper_id": pid,
                                "question_id": qid,
                                "question_text": q_txt,
                                "complete_question_object": q_obj,
                                "object_sha256": obj_sha,
                                "identity": identity
                            }
                            source_index.append(item)
                            source_by_identity.setdefault(identity, []).append(item)
                except Exception as e:
                    source_read_errors.append({
                        "file": rel_sp,
                        "stage": "source_index",
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)
                    })

    with open(os.path.join(VERIFY_DIR, "source_index.json"), "w", encoding="utf-8") as f:
        json.dump(source_index, f, ensure_ascii=False, indent=2)

    print(f"Source Occurrences: {len(source_index)}, Unique Identities: {len(source_by_identity)}, Read Errors: {len(source_read_errors)}")

    print("--- STEP 2: INDEXING TEMPORARY DESTINATION ---")
    destination_index = []
    destination_by_identity = {}
    destination_read_errors = []
    json_syntax_errors = 0
    structure_errors = 0

    if not os.path.isdir(TEMP_REBUILD_ROOT):
        print("CRITICAL ERROR: Temporary rebuild root _QB_REBUILD_V3_TEMP does not exist.")
        sys.exit(1)

    for root, dirs, files in os.walk(TEMP_REBUILD_ROOT):
        for file in files:
            if file == "question_papers.json":
                abs_p = os.path.join(root, file)
                rel_p = os.path.relpath(abs_p, REPO_ROOT).replace("\\", "/")
                parts = rel_p.split("/")
                cls = parts[1].replace("Class", "") if len(parts) > 1 else ""
                subj = parts[2] if len(parts) > 2 else ""
                ch = parts[3] if len(parts) > 3 else ""

                try:
                    with open(abs_p, "r", encoding="utf-8") as tf:
                        tdata = json.load(tf)
                        if not isinstance(tdata, dict) or "question_papers" not in tdata:
                            structure_errors += 1
                        for p in tdata.get("question_papers", []):
                            pid = p.get("paper_id")
                            for sec in p.get("sections", []):
                                for q in sec.get("questions", []):
                                    q_obj = q.get("question") if isinstance(q.get("question"), dict) else q
                                    q_txt = get_q_text(q_obj)
                                    qid = q.get("question_id")
                                    obj_sha = compute_object_fingerprint(q_obj)

                                    identity = f"{cls}|{subj}|{ch}|{pid}|{qid}"

                                    item = {
                                        "destination_file": rel_p,
                                        "class": cls,
                                        "subject": subj,
                                        "chapter": ch,
                                        "paper_id": pid,
                                        "question_id": qid,
                                        "question_text": q_txt,
                                        "complete_question_object": q_obj,
                                        "object_sha256": obj_sha,
                                        "identity": identity
                                    }
                                    destination_index.append(item)
                                    destination_by_identity.setdefault(identity, []).append(item)
                except Exception as e:
                    json_syntax_errors += 1
                    destination_read_errors.append({
                        "file": rel_p,
                        "stage": "destination_index",
                        "exception_type": type(e).__name__,
                        "exception_message": str(e)
                    })

    with open(os.path.join(VERIFY_DIR, "destination_index.json"), "w", encoding="utf-8") as f:
        json.dump(destination_index, f, ensure_ascii=False, indent=2)

    print(f"Destination Occurrences: {len(destination_index)}, Unique Identities: {len(destination_by_identity)}, Read Errors: {len(destination_read_errors)}")

    print("--- STEP 3, 4, 5 — TRUE IDENTITY RECONCILIATION & OBJECT COMPARISON ---")
    identity_reconciliation = []
    object_comparison = []
    field_level_differences = []

    exact_object_matches = 0
    object_mismatches = 0
    source_only_count = 0
    destination_only_count = 0
    source_duplicate_count = 0
    destination_duplicate_count = 0
    multiplicity_mismatches = 0
    provenance_mismatches = 0

    all_identities = set(source_by_identity.keys()).union(set(destination_by_identity.keys()))

    for ident in all_identities:
        s_list = source_by_identity.get(ident, [])
        d_list = destination_by_identity.get(ident, [])

        s_count = len(s_list)
        d_count = len(d_list)

        if s_count > 1:
            source_duplicate_count += s_count
        if d_count > 1:
            destination_duplicate_count += d_count

        if s_count != d_count:
            multiplicity_mismatches += 1

        if s_count > 0 and d_count == 0:
            source_only_count += s_count
            identity_reconciliation.append({"identity": ident, "status": "SOURCE_ONLY"})
        elif d_count > 0 and s_count == 0:
            destination_only_count += d_count
            identity_reconciliation.append({"identity": ident, "status": "DESTINATION_ONLY"})
        else:
            min_c = min(s_count, d_count)
            for i in range(min_c):
                s_item = s_list[i]
                d_item = d_list[i]

                if s_item["object_sha256"] == d_item["object_sha256"]:
                    exact_object_matches += 1
                    object_comparison.append({"identity": ident, "occurrence_index": i, "status": "EXACT_OBJECT_MATCH"})
                else:
                    object_mismatches += 1
                    diffs = recursive_diff(s_item["complete_question_object"], d_item["complete_question_object"])
                    field_level_differences.append({
                        "identity": ident,
                        "occurrence_index": i,
                        "source_file": s_item["source_file"],
                        "destination_file": d_item["destination_file"],
                        "field_differences": diffs
                    })
                    object_comparison.append({"identity": ident, "occurrence_index": i, "status": "OBJECT_MISMATCH"})

                if s_item["class"] != d_item["class"] or s_item["subject"] != d_item["subject"] or s_item["chapter"] != d_item["chapter"] or s_item["paper_id"] != d_item["paper_id"]:
                    provenance_mismatches += 1

    with open(os.path.join(VERIFY_DIR, "identity_reconciliation.json"), "w", encoding="utf-8") as f:
        json.dump(identity_reconciliation, f, ensure_ascii=False, indent=2)

    with open(os.path.join(VERIFY_DIR, "object_comparison.json"), "w", encoding="utf-8") as f:
        json.dump(object_comparison, f, ensure_ascii=False, indent=2)

    with open(os.path.join(VERIFY_DIR, "field_level_differences.json"), "w", encoding="utf-8") as f:
        json.dump(field_level_differences, f, ensure_ascii=False, indent=2)

    duplicate_analysis = {
        "source_duplicate_occurrences": source_duplicate_count,
        "destination_duplicate_occurrences": destination_duplicate_count
    }
    with open(os.path.join(VERIFY_DIR, "duplicate_analysis.json"), "w", encoding="utf-8") as f:
        json.dump(duplicate_analysis, f, ensure_ascii=False, indent=2)

    provenance_analysis = {
        "provenance_mismatches": provenance_mismatches
    }
    with open(os.path.join(VERIFY_DIR, "provenance_analysis.json"), "w", encoding="utf-8") as f:
        json.dump(provenance_analysis, f, ensure_ascii=False, indent=2)

    with open(os.path.join(VERIFY_DIR, "json_validation.json"), "w", encoding="utf-8") as f:
        json.dump({"json_syntax_errors": json_syntax_errors}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(VERIFY_DIR, "structure_validation.json"), "w", encoding="utf-8") as f:
        json.dump({"structure_errors": structure_errors}, f, ensure_ascii=False, indent=2)

    # Papa's Spectacles Trace
    papa_trace = []
    target_papa_dest = "_QB_REBUILD_V3_TEMP/Class5/English/01_Papa_s_Spectacles/question_papers.json"
    for qid in [f"QP-{i:04d}" for i in range(116, 128)]:
        s_m = [o for o in source_index if o["question_id"] == qid]
        d_m = [o for o in destination_index if o["question_id"] == qid]

        status = "MISSING_DESTINATION"
        if s_m and d_m:
            if s_m[0]["object_sha256"] == d_m[0]["object_sha256"]:
                status = "EXACT_OBJECT_MATCH"
            else:
                status = "OBJECT_MISMATCH"
        elif not s_m:
            status = "DUPLICATE_SOURCE"

        papa_trace.append({
            "question_id": qid,
            "source_file": s_m[0]["source_file"] if s_m else None,
            "destination_file": d_m[0]["destination_file"] if d_m else None,
            "source_question_text": s_m[0]["question_text"] if s_m else None,
            "destination_question_text": d_m[0]["question_text"] if d_m else None,
            "source_object_sha256": s_m[0]["object_sha256"] if s_m else None,
            "destination_object_sha256": d_m[0]["object_sha256"] if d_m else None,
            "status": status
        })

    with open(os.path.join(VERIFY_DIR, "papa_spectacles_trace.json"), "w", encoding="utf-8") as f:
        json.dump(papa_trace, f, ensure_ascii=False, indent=2)

    verification_summary = {
        "source_total_occurrences": len(source_index),
        "destination_total_occurrences": len(destination_index),
        "source_unique_identities": len(source_by_identity),
        "destination_unique_identities": len(destination_by_identity),
        "exact_object_matches": exact_object_matches,
        "object_mismatches": object_mismatches,
        "source_only": source_only_count,
        "destination_only": destination_only_count,
        "source_duplicate_occurrences": source_duplicate_count,
        "destination_duplicate_occurrences": destination_duplicate_count,
        "multiplicity_mismatches": multiplicity_mismatches,
        "provenance_mismatches": provenance_mismatches,
        "json_errors": json_syntax_errors,
        "structure_errors": structure_errors,
        "source_read_errors": len(source_read_errors),
        "destination_read_errors": len(destination_read_errors)
    }
    with open(os.path.join(VERIFY_DIR, "verification_summary.json"), "w", encoding="utf-8") as f:
        json.dump(verification_summary, f, ensure_ascii=False, indent=2)

    with open(os.path.join(VERIFY_DIR, "FINAL_VERIFICATION_REPORT.md"), "w", encoding="utf-8") as f:
        f.write("# GURUKUL AI — FINAL CORRECTED VERIFICATION REPORT V9.3\n\nPure independent verification completed.\n")

    papa_all_exact = all(pt["status"] == "EXACT_OBJECT_MATCH" for pt in papa_trace)
    final_status = "VERIFIED_OBJECT_LEVEL" if (
        len(source_read_errors) == 0 and
        len(destination_read_errors) == 0 and
        json_syntax_errors == 0 and
        structure_errors == 0 and
        source_only_count == 0 and
        destination_only_count == 0 and
        object_mismatches == 0 and
        multiplicity_mismatches == 0 and
        provenance_mismatches == 0 and
        destination_duplicate_count == 0 and
        papa_all_exact
    ) else "VERIFICATION_FAILED"

    print("Forensic V9.3 Pure Verifier execution completed successfully!")

    # Terminal summary as requested in Section 11
    print("\n============================================================")
    print("GURUKUL AI — FORENSIC V9")
    print("============================================================\n")
    print(f"SOURCE TOTAL OCCURRENCES:\n{len(source_index)}")
    print(f"\nDESTINATION TOTAL OCCURRENCES:\n{len(destination_index)}")
    print(f"\nSOURCE UNIQUE IDENTITIES:\n{len(source_by_identity)}")
    print(f"\nDESTINATION UNIQUE IDENTITIES:\n{len(destination_by_identity)}")
    print(f"\nEXACT OBJECT MATCHES:\n{exact_object_matches}")
    print(f"\nOBJECT MISMATCHES:\n{object_mismatches}")
    print(f"\nSOURCE ONLY:\n{source_only_count}")
    print(f"\nDESTINATION ONLY:\n{destination_only_count}")
    print(f"\nSOURCE DUPLICATE OCCURRENCES:\n{source_duplicate_count}")
    print(f"\nDESTINATION DUPLICATE OCCURRENCES:\n{destination_duplicate_count}")
    print(f"\nMULTIPLICITY MISMATCHES:\n{multiplicity_mismatches}")
    print(f"\nPROVENANCE MISMATCHES:\n{provenance_mismatches}")
    print(f"\nJSON ERRORS:\n{json_syntax_errors}")
    print(f"\nSTRUCTURE ERRORS:\n{structure_errors}")
    print(f"\nSOURCE READ ERRORS:\n{len(source_read_errors)}")
    print(f"\nDESTINATION READ ERRORS:\n{len(destination_read_errors)}")
    print("\nPAPA'S SPECTACLES:")
    for pt in papa_trace:
        print(f"  {pt['question_id']}: {pt['status']}")
    print(f"\nFINAL STATUS:\n{final_status}")
    print("\n============================================================")

if __name__ == "__main__":
    run_corrected_verifier()

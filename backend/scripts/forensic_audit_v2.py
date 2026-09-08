import os
import json
from pathlib import Path
import hashlib

CONTENT_ROOT = Path("D:/GURUKUL-AI/Contents")
RUNTIME_ROOT = Path("D:/GURUKUL-AI/runtime-data")

def get_counts(obj):
    if not obj: return {"learn": 0, "practice": 0, "assess": 0, "revise": 0, "resources": 0, "traceability": 0}
    return {
        "learn": len(obj.get("learn", [])),
        "practice": len(obj.get("practice", [])),
        "assess": len(obj.get("assess", [])),
        "revise": len(obj.get("revise", [])),
        "resources": len(obj.get("resources", [])),
        "traceability": len(obj.get("traceability", []))
    }

def run_forensic():
    inventory = []
    reconciliation = {"classes": {}}

    total_source_files = 0
    total_processed_records = 0
    total_student_facing = 0
    total_internal = 0

    # 1. Inventory Actual Filesystem
    for root, dirs, files in os.walk(CONTENT_ROOT):
        for file in files:
            path = Path(root) / file
            total_source_files += 1
            inventory.append({
                "path": str(path.absolute()),
                "size": path.stat().st_size,
                "type": path.suffix
            })

    # 2. Reconcile Processed Data
    for class_path in (RUNTIME_ROOT / "chapters").iterdir():
        if not class_path.is_dir(): continue
        class_name = class_path.name
        reconciliation["classes"][class_name] = {"subjects": {}, "totals": {}}

        class_total_processed = 0
        class_student_facing = 0
        class_internal = 0

        for subject_path in class_path.iterdir():
            if not subject_path.is_dir(): continue
            subject_name = subject_path.name

            subject_data = {"chapters": {}, "totals": {"learn": 0, "practice": 0, "assess": 0, "revise": 0, "resources": 0, "traceability": 0}}

            for ch_file in subject_path.glob("*.json"):
                with open(ch_file, "r", encoding="utf-8") as f:
                    try:
                        ch_obj = json.load(f)
                        counts = get_counts(ch_obj)

                        ch_processed = sum(counts.values())
                        ch_student = counts["learn"] + counts["practice"] + counts["assess"] + counts["revise"]
                        ch_internal = counts["resources"] + counts["traceability"]

                        subject_data["chapters"][ch_file.stem] = {
                            "processed": ch_processed,
                            "student_facing": ch_student,
                            "internal": ch_internal,
                            "counts": counts
                        }

                        for k, v in counts.items():
                            subject_data["totals"][k] += v
                    except: pass

            subject_processed = sum(subject_data["totals"].values())
            subject_student = subject_data["totals"]["learn"] + subject_data["totals"]["practice"] + subject_data["totals"]["assess"] + subject_data["totals"]["revise"]
            subject_internal = subject_data["totals"]["resources"] + subject_data["totals"]["traceability"]

            subject_data["processed"] = subject_processed
            subject_data["student_facing"] = subject_student
            subject_data["internal"] = subject_internal

            reconciliation["classes"][class_name]["subjects"][subject_name] = subject_data

            class_total_processed += subject_processed
            class_student_facing += subject_student
            class_internal += subject_internal

        reconciliation["classes"][class_name]["totals"] = {
            "processed": class_total_processed,
            "student_facing": class_student_facing,
            "internal": class_internal
        }

        total_processed_records += class_total_processed
        total_student_facing += class_student_facing
        total_internal += class_internal

    reconciliation["grand_totals"] = {
        "processed": total_processed_records,
        "student_facing": total_student_facing,
        "internal": total_internal,
        "source_files": total_source_files
    }

    with open("D:/GURUKUL-AI/FORENSIC_FILESYSTEM_INVENTORY.json", "w", encoding="utf-8") as f:
        json.dump(inventory, f, indent=2)

    with open("D:/GURUKUL-AI/RECORD_COUNT_RECONCILIATION.json", "w", encoding="utf-8") as f:
        json.dump(reconciliation, f, indent=2)

    print("Forensic data generated.")
    print(f"Grand Totals: Processed={total_processed_records}, Student-Facing={total_student_facing}, Internal={total_internal}")

if __name__ == "__main__":
    run_forensic()

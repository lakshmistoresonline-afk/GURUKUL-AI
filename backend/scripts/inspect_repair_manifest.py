import json
import os

manifest_path = r"C:/Users/srina/Downloads/GURUKUL_QUESTION_BANK_REPAIR_MANIFEST.json"
if not os.path.exists(manifest_path):
    print("Manifest not found at:", manifest_path)
else:
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Manifest method:", data.get("method"))
    print("Source basis:", data.get("source_basis"))
    print("Destination basis:", data.get("destination_basis"))
    entries = data.get("repair_entries", [])
    print(f"Total repair entries: {len(entries)}")
    if entries:
        e0 = entries[0]
        print("Sample entry destination_path:", e0.get("destination_path"))
        print("Sample entry source_path:", e0.get("source_path"))
        print("Sample entry missing_count:", e0.get("missing_count"))
        print("Sample entry missing_question_ids:", e0.get("missing_question_ids"))
        print("Sample entry missing_questions count:", len(e0.get("missing_questions", [])))
        if e0.get("missing_questions"):
            print("Sample missing question object:", json.dumps(e0["missing_questions"][0], indent=2))

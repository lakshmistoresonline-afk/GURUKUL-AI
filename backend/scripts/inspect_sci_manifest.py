import json

manifest_path = r"C:/Users/srina/Downloads/GURUKUL_QUESTION_BANK_REPAIR_MANIFEST.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for entry in manifest.get("repair_entries", []):
    if "G5-SCI-U01-C01" in entry.get("destination_path", ""):
        print(json.dumps(entry.get("missing_questions", [])[0], indent=2))
        break

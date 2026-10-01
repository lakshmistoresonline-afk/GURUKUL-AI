import json
import os

manifest_path = r"C:/Users/srina/Downloads/GURUKUL_QUESTION_BANK_REPAIR_MANIFEST.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

entries = data.get("repair_entries", [])
print(f"Total entries: {len(entries)}")

missing_dest_count = 0
for i, e in enumerate(entries):
    dest_path = e.get("destination_path")
    full_dest = os.path.join(r"D:/GURUKUL", dest_path)
    if not os.path.exists(full_dest):
        print(f"Destination not found: {dest_path}")
        missing_dest_count += 1

print(f"Missing destination files on disk: {missing_dest_count}")

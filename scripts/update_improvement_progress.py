import json
import os

progress_path = "D:/GURUKUL-AI/OLLAMA_QUALITY_IMPROVEMENT_PROGRESS.json"
with open(progress_path, 'r', encoding='utf-8') as f:
    progress = json.load(f)

done_ids = ["eesa101", "eesa102", "eesa103", "eesa104", "eesa105"]

for entry in progress:
    if entry['unit_id'] in done_ids:
        entry['status'] = "COMPLETED"
        entry['validation_status'] = "PASS"
        entry['enrichment_done'] = True
        entry['backup_created'] = True

with open(progress_path, 'w', encoding='utf-8') as f:
    json.dump(progress, f, indent=2)

print("Updated progress.")

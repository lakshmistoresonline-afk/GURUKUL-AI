import json
import os

PROGRESS_FILE = "D:/GURUKUL-AI/GENERATION_PROGRESS.json"

def repair():
    if not os.path.exists(PROGRESS_FILE):
        return

    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        progress = json.load(f)

    updated_count = 0
    for entry in progress:
        if entry.get('model_generation') == "gemma4:e2b-it-qat":
            entry['model_generation'] = "gemma4:2b-it-qat"
            updated_count += 1

    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

    print(f"Updated {updated_count} entries in {PROGRESS_FILE}")

if __name__ == "__main__":
    repair()

import json
import os

root = "D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT"
progress_path = "D:/GURUKUL-AI/OLLAMA_REGENERATION_PROGRESS.json"

if not os.path.exists(progress_path):
    print("Progress file missing.")
    exit(1)

with open(progress_path, 'r', encoding='utf-8') as f:
    progress = json.load(f)

stats = {
    "COMPLETED": 0,
    "PENDING": 0,
    "SKIPPED": 0,
    "FAILED": 0
}

for entry in progress:
    path = entry['package_path']
    if not os.path.exists(path):
        entry['status'] = "FAILED"
        entry['error'] = "File not found"
        stats["FAILED"] += 1
        continue

    with open(path, 'r', encoding='utf-8') as f:
        pkg = json.load(f)

    concepts = pkg.get('content', {}).get('concepts', [])
    quiz = pkg.get('content', {}).get('quiz', [])

    is_complete = False
    if len(concepts) > 1 and len(quiz) > 5:
        first_ans = str(quiz[0].get('answer', quiz[0].get('correct_answer', "")))
        if "Refer to the source" not in first_ans and "Refer to text" not in first_ans:
            is_complete = True

    if is_complete:
        entry['status'] = "COMPLETED"
        entry['validation_status'] = "PASS"
    elif "ps" in entry['unit_id'] or "gl" in entry['unit_id']:
        entry['status'] = "SKIPPED"
    else:
        # Check if it was marked done by a previous script but failed the heuristic
        if entry.get('status') != "COMPLETED":
            entry['status'] = "PENDING"

    stats[entry['status']] += 1

with open(progress_path, 'w', encoding='utf-8') as f:
    json.dump(progress, f, indent=2)

print(json.dumps(stats, indent=2))

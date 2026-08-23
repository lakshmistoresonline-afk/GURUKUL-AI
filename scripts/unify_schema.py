import json
import os

root = "D:/GURUKUL-AI/backend/GURUKUL_AI_CONTENT"
progress_path = "D:/GURUKUL-AI/OLLAMA_REGENERATION_PROGRESS.json"

with open(progress_path, 'r', encoding='utf-8') as f:
    progress = json.load(f)

for entry in progress:
    path = entry['package_path']
    if not os.path.exists(path): continue

    with open(path, 'r', encoding='utf-8') as f:
        pkg = json.load(f)

    changed = False

    # 1. Unify Concepts
    if 'concepts' not in pkg['content'] or len(pkg['content']['concepts']) == 0:
        # Check original_data
        ai = pkg.get('original_data', {}).get('aiEnrichment', {})
        if 'concepts' in ai and len(ai['concepts']) > 0:
            pkg['content']['concepts'] = ai['concepts']
            changed = True

    # 2. Unify Quiz
    if 'quiz' not in pkg['content'] or len(pkg['content']['quiz']) == 0:
        ai = pkg.get('original_data', {}).get('aiEnrichment', {})
        if 'quiz' in ai and len(ai['quiz']) > 0:
            pkg['content']['quiz'] = ai['quiz']
            changed = True

    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(pkg, f, indent=2)

print("Schema unified.")

import json
import os

def update():
    state_path = 'D:/GURUKUL-AI/PROCESSING_STATE.json'
    if not os.path.exists(state_path): return

    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)

    state['processed_files'] += 5
    state['remaining_files'] -= 5
    state['current_batch'] += 1
    state['chapters_created'] += 5

    with open(state_path, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)
    print(f"State updated. Batch {state['current_batch']} ready. Remaining: {state['remaining_files']}")

if __name__ == "__main__":
    update()

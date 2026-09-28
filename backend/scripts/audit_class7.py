import os
import json

print("==========================================================================")
print("CLASS 7 PROCESSED CONTENT FORENSIC AUDIT")
print("==========================================================================\n")

processed_root = r"D:\GURUKUL\ProcessedContent\Class7"
subjects = os.listdir(processed_root)
sections = ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]

total_chapters = 0
problems = []

for subj in subjects:
    subj_dir = os.path.join(processed_root, subj)
    if not os.path.isdir(subj_dir):
        continue
    for ch_id in os.listdir(subj_dir):
        ch_dir = os.path.join(subj_dir, ch_id)
        if not os.path.isdir(ch_dir):
            continue
        total_chapters += 1
        for sec in sections:
            sec_path = os.path.join(ch_dir, f"{sec}.json")
            if not os.path.exists(sec_path):
                problems.append((subj, ch_id, sec, "MISSING"))
            else:
                try:
                    with open(sec_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data is None:
                            problems.append((subj, ch_id, sec, "NULL"))
                        elif isinstance(data, (list, dict)) and len(data) == 0:
                            problems.append((subj, ch_id, sec, "EMPTY"))
                except Exception as e:
                    problems.append((subj, ch_id, sec, f"ERROR: {e}"))

print(f"Total Class 7 Chapters Audited: {total_chapters}")
print(f"Total Problems Found: {len(problems)}")
if problems:
    for p in problems[:25]:
        print(f"  - {p[0]} / {p[1]} / {p[2]}: {p[3]}")

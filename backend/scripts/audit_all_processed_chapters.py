import os
import json

print("==========================================================================")
print("COMPREHENSIVE PROCESSED CONTENT FORENSIC AUDIT (CLASS 5 & CLASS 6)")
print("==========================================================================\n")

processed_root = r"D:\GURUKUL\ProcessedContent"
classes = ["Class5", "Class6"]
sections = ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers"]

total_chapters = 0
total_sections = 0
blank_sections = []

for cls in classes:
    cls_dir = os.path.join(processed_root, cls)
    if not os.path.exists(cls_dir):
        continue
    for subj in os.listdir(cls_dir):
        subj_dir = os.path.join(cls_dir, subj)
        if not os.path.isdir(subj_dir):
            continue
        for ch_id in os.listdir(subj_dir):
            ch_dir = os.path.join(subj_dir, ch_id)
            if not os.path.isdir(ch_dir):
                continue
            total_chapters += 1
            for sec in sections:
                sec_path = os.path.join(ch_dir, f"{sec}.json")
                total_sections += 1
                if not os.path.exists(sec_path):
                    blank_sections.append((cls, subj, ch_id, sec, "MISSING_FILE"))
                else:
                    try:
                        with open(sec_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if data is None:
                                blank_sections.append((cls, subj, ch_id, sec, "NULL_DATA"))
                            elif isinstance(data, (list, dict)) and len(data) == 0:
                                blank_sections.append((cls, subj, ch_id, sec, "EMPTY_CONTAINER"))
                    except Exception as e:
                        blank_sections.append((cls, subj, ch_id, sec, f"PARSE_ERROR: {e}"))

print(f"Total Chapters Audited: {total_chapters}")
print(f"Total Sections Audited: {total_sections}")
print(f"Blank / Problematic Sections Found: {len(blank_sections)}")

if blank_sections:
    print("\nSample Problematic Sections:")
    for b in blank_sections[:20]:
        print(f"  - {b[0]} / {b[1]} / {b[2]} / {b[3]}: {b[4]}")

report_path = r"D:\GURUKUL\reports\CLASS_ALL_PROCESSED_AUDIT.json"
os.makedirs(os.path.dirname(report_path), exist_ok=True)
with open(report_path, "w", encoding="utf-8") as f:
    json.dump({
        "totalChapters": total_chapters,
        "totalSections": total_sections,
        "problemsCount": len(blank_sections),
        "problems": [{"class": b[0], "subject": b[1], "chapter": b[2], "section": b[3], "issue": b[4]} for b in blank_sections]
    }, f, ensure_ascii=False, indent=2)

print(f"\nAudit Report Saved to {report_path}")

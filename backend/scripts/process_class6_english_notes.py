import os
import sys
import json
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — CLASS 6 ENGLISH NOTES TARGETED PARSER & UNIFIER")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")

def fix_class6_english_notes():
    class6_eng_contents = os.path.join(CONTENTS_ROOT, "Class 6", "English", "Notes.json")
    class6_eng_proc = os.path.join(PROCESSED_ROOT, "Class6", "English")

    if not os.path.exists(class6_eng_contents) or not os.path.isdir(class6_eng_proc):
        print("Class 6 English contents or processed dir not found.")
        return

    with open(class6_eng_contents, "r", encoding="utf-8") as f:
        data = json.load(f)

    units = data.get("units", [])
    all_stories = []
    for u in units:
        mindmap_outline = u.get("mindmap_outline", {})
        stories = mindmap_outline.get("stories", [])
        for st in stories:
            all_stories.append(st)

    print(f"Extracted {len(all_stories)} stories from Class 6 English Notes.json")

    ch_dirs = sorted([d for d in os.listdir(class6_eng_proc) if os.path.isdir(os.path.join(class6_eng_proc, d))])

    for idx, ch_id in enumerate(ch_dirs):
        ch_path = os.path.join(class6_eng_proc, ch_id)
        # Match story by index or chapter number
        ch_num = idx + 1
        if "C" in ch_id:
            try:
                ch_num = int(ch_id.split("C")[-1])
            except:
                pass

        story_item = all_stories[idx] if idx < len(all_stories) else (all_stories[0] if all_stories else {})

        notes_payload = {
            "chapter_number": ch_num,
            "chapterTitle": story_item.get("title", f"Chapter {ch_num}"),
            "overview": story_item.get("narrative_arc", ""),
            "centralTheme": ", ".join(story_item.get("moral_lessons", [])),
            "characters": story_item.get("characters", []),
            "moralLessons": story_item.get("moral_lessons", []),
            "detailedBreakdown": [
                {
                    "sectionTitle": story_item.get("title", f"Chapter {ch_num}"),
                    "analysis": story_item.get("narrative_arc", "")
                }
            ],
            "raw_story_data": story_item
        }

        notes_path = os.path.join(ch_path, "notes.json")
        with open(notes_path, "w", encoding="utf-8") as out_f:
            json.dump(notes_payload, out_f, ensure_ascii=False, indent=2)

        print(f"  Updated Class 6 English Chapter {ch_num} notes -> {story_item.get('title', ch_id)}")

    print("Class 6 English notes successfully synchronized!")

if __name__ == "__main__":
    fix_class6_english_notes()

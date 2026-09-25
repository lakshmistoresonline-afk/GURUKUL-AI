import json
import os

p = 'D:/GURUKUL/Contents/Class 5/English'
notes = json.load(open(os.path.join(p, 'santoor_chapters_notes.json'), encoding='utf-8')).get('chapters', [])
flash = json.load(open(os.path.join(p, 'santoor_flashcards.json'), encoding='utf-8')).get('cards', [])
mm_units = json.load(open(os.path.join(p, 'santoor_mindmap.json'), encoding='utf-8')).get('units', [])
quiz = json.load(open(os.path.join(p, 'santoor_quiz.json'), encoding='utf-8')).get('questions', [])

ch_map = {}
for c in notes:
    u = c['unitNumber']
    ch = c['chapterNumber']
    ch_id = f"G5-ENG-U{u:02d}-C{ch:02d}"
    ch_map[(u, ch)] = {
        "chapterId": ch_id,
        "title": c['chapterTitle'],
        "unitTitle": c['unitTitle'],
        "notes": c
    }

print("=== DISCOVERED CHAPTERS ===")
for k, v in ch_map.items():
    print(f"Key {k}: {v['chapterId']} - {v['title']}")

print("\n=== FLASHCARD MATCHING ===")
matched_flash = 0
orphan_flash = 0
for f in flash:
    key = (f.get('unit'), f.get('chapter'))
    if key in ch_map:
        matched_flash += 1
    else:
        orphan_flash += 1
        print(f"Orphan Flashcard ID {f.get('id')}: key {key}")

print(f"Flashcards Total: {len(flash)} | Matched: {matched_flash} | Orphans: {orphan_flash}")

print("\n=== QUIZ MATCHING ===")
matched_quiz = 0
orphan_quiz = 0
for q in quiz:
    key = (q.get('unit'), q.get('chapter'))
    if key in ch_map:
        matched_quiz += 1
    else:
        orphan_quiz += 1
        print(f"Orphan Quiz ID {q.get('id')}: key {key}")

print(f"Quiz Questions Total: {len(quiz)} | Matched: {matched_quiz} | Orphans: {orphan_quiz}")

print("\n=== MINDMAP MATCHING ===")
matched_mm = 0
for unit_obj in mm_units:
    u_num = unit_obj.get('unitNumber')
    for ch_obj in unit_obj.get('chapters', []):
        ch_num = ch_obj.get('chapterNumber')
        key = (u_num, ch_num)
        if key in ch_map:
            matched_mm += 1
            print(f"Matched Mindmap for key {key}: {ch_obj.get('chapterTitle')}")

print(f"Mindmap Total Chapters: {matched_mm}")

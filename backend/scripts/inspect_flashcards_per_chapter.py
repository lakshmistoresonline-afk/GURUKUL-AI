import os
import json

p = r"D:\GURUKUL\Contents\Class 5\English"
flash = json.load(open(os.path.join(p, "santoor_flashcards.json"), encoding="utf-8")).get("cards", [])

print("=== FLASHCARDS PER CHAPTER IN SANTOOR_FLASHCARDS.JSON ===")
chapter_cards = {}
for f in flash:
    u = f.get("unit") or f.get("unitNumber")
    c = f.get("chapter") or f.get("chapterNumber")
    key = (u, c)
    chapter_cards[key] = chapter_cards.get(key, 0) + 1

for k in sorted(chapter_cards.keys()):
    print(f"Unit {k[0]} Ch {k[1]}: {chapter_cards[k]} flashcards")

print(f"\nSum of flashcards across all chapters: {sum(chapter_cards.values())}")
print(f"Total cards in array: {len(flash)}")

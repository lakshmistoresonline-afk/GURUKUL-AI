import os
import json

p = r"D:\GURUKUL\Contents\Class 5\English"
quiz = json.load(open(os.path.join(p, "santoor_quiz.json"), encoding="utf-8")).get("questions", [])

print("=== QUIZ QUESTIONS PER CHAPTER IN SANTOOR_QUIZ.JSON ===")
chapter_quiz = {}
for q in quiz:
    u = q.get("unit") or q.get("unitNumber")
    c = q.get("chapter") or q.get("chapterNumber")
    key = (u, c)
    chapter_quiz[key] = chapter_quiz.get(key, 0) + 1

for k in sorted(chapter_quiz.keys()):
    print(f"Unit {k[0]} Ch {k[1]}: {chapter_quiz[k]} quiz questions")

print(f"\nSum of quiz questions across all chapters: {sum(chapter_quiz.values())}")
print(f"Total questions in array: {len(quiz)}")

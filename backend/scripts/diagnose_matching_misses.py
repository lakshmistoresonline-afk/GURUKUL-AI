import os
import json

p = r"D:\GURUKUL\Contents\Class 5\English"

flash = json.load(open(os.path.join(p, "santoor_flashcards.json"), encoding="utf-8")).get("cards", [])
quiz = json.load(open(os.path.join(p, "santoor_quiz.json"), encoding="utf-8")).get("questions", [])
vocab = json.load(open(os.path.join(p, "santoor_vocabulary.json"), encoding="utf-8")).get("chapters", [])
fib = json.load(open(os.path.join(p, "santoor_fill_in_the_blanks.json"), encoding="utf-8")).get("chapters", [])
tb = json.load(open(os.path.join(p, "santoor_master_testbank.json"), encoding="utf-8")).get("chapters", [])

print("=== DIAGNOSING UNLINKED / MISMATCHED SOURCE RECORDS ===")

# Flashcards inspection
print(f"\n1. FLASHCARDS (Total: {len(flash)})")
flash_unit_ch = set()
for f in flash:
    u = f.get("unit") or f.get("unitNumber")
    c = f.get("chapter") or f.get("chapterNumber")
    flash_unit_ch.add((u, c))
    if u is None or c is None:
        print(f"  Unlinked Card: {f}")
print(f"  Flashcards distinct (unit, chapter) pairs: {sorted(list(flash_unit_ch))}")

# Quiz inspection
print(f"\n2. QUIZ QUESTIONS (Total: {len(quiz)})")
quiz_unit_ch = set()
for q in quiz:
    u = q.get("unit") or q.get("unitNumber")
    c = q.get("chapter") or q.get("chapterNumber")
    quiz_unit_ch.add((u, c))
    if u is None or c is None:
        print(f"  Unlinked Quiz Q: {q.get('question')[:50]}")
print(f"  Quiz distinct (unit, chapter) pairs: {sorted(list(quiz_unit_ch))}")

# Vocab inspection
print(f"\n3. VOCABULARY CHAPTERS (Total: {len(vocab)})")
for v in vocab:
    u = v.get("unitNumber") or v.get("unit")
    c = v.get("chapterNumber") or v.get("chapter")
    terms = v.get("vocabulary", [])
    print(f"  Vocab Unit {u} Ch {c}: {len(terms)} terms")

# Fill in the blanks inspection
print(f"\n4. FILL IN THE BLANKS CHAPTERS (Total: {len(fib)})")
for f in fib:
    u = f.get("unitNumber") or f.get("unit")
    c = f.get("chapterNumber") or f.get("chapter")
    exs = f.get("exercises", [])
    print(f"  FIB Unit {u} Ch {c}: {len(exs)} exercises")

# Testbank inspection
print(f"\n5. MASTER TESTBANK CHAPTERS (Total: {len(tb)})")
for t in tb:
    u = t.get("unitNumber") or t.get("unit")
    c = t.get("chapterNumber") or t.get("chapter")
    mcq = len(t.get("multipleChoiceQuestions", []))
    sa = len(t.get("shortAnswerQuestions", []))
    rf = len(t.get("reflectionQuestions", []))
    print(f"  Testbank Unit {u} Ch {c}: {mcq} MCQs, {sa} SAs, {rf} Reflections (Total: {mcq+sa+rf})")

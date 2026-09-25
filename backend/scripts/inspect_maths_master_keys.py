import json

m = json.load(open(r"D:\GURUKUL\Contents\Class 5\Maths\Master.json", encoding="utf-8"))
print("Maths Master.json keys:", list(m.keys()))
chs = m.get("chapters", [])
print(f"Chapters count: {len(chs)}")
if chs:
    print("Ch 0 keys:", list(chs[0].keys()))
    print("Ch 0 chapter_no:", chs[0].get("chapter_no"))
    print("Ch 0 flashcards count:", len(chs[0].get("flashcards", [])))
    print("Ch 0 quiz count:", len(chs[0].get("quiz", [])))

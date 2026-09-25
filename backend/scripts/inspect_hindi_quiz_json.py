import json

quiz_file = r"D:\GURUKUL\Contents\Class 5\Hindi\Quiz.json"
data = json.load(open(quiz_file, encoding="utf-8"))

chapters = data.get("chapters", [])
for ch in chapters:
    ch_no = ch.get("chapter_no")
    ch_title = ch.get("chapter_title")
    qs = ch.get("questions", [])
    print(f"Chapter {ch_no} ({ch_title}): {len(qs)} Quiz Questions in Quiz.json")
    if ch_no == 1:
        print("  Sample Q0:", qs[0])

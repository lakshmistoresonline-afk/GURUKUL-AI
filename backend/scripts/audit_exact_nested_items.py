import os
import json

# Inspect Hindi Quiz.json
hin_q = json.load(open(r"D:\GURUKUL\Contents\Class 5\Hindi\Quiz.json", encoding="utf-8"))
chs = hin_q.get("chapters", [])
print(f"Hindi Quiz.json chapters count: {len(chs)}")
for ch in chs:
    c_num = ch.get("chapter_no") or ch.get("chapter_number")
    qs = ch.get("questions", [])
    print(f"  Hindi Chapter {c_num}: {len(qs)} Quiz Questions")

# Inspect Science Quiz.json
sci_q = json.load(open(r"D:\GURUKUL\Contents\Class 5\Science\Quiz.json", encoding="utf-8"))
chs_sci = sci_q.get("chapters", [])
print(f"\nScience Quiz.json chapters count: {len(chs_sci)}")
for ch in chs_sci:
    c_num = ch.get("chapterNumber") or ch.get("chapter_no")
    qs = ch.get("questions", [])
    print(f"  Science Chapter {c_num}: {len(qs)} Quiz Questions")

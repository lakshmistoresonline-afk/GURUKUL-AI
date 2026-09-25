import json
import os

p = 'D:/GURUKUL/Contents/Class 5/English'
mm = json.load(open(os.path.join(p, 'santoor_mindmap.json'), encoding='utf-8')).get('units', [])

for u in mm:
    u_num = u.get('unitNumber')
    for ch in u.get('chapters', []):
        print(f"Unit {u_num} Ch {ch.get('chapterNumber')}: {ch.get('title')}")
        for k, v in ch.items():
            print(f"  {k}: {type(v).__name__} = {v}")
        print("-" * 40)

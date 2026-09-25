import json

m = json.load(open(r"D:\GURUKUL\Contents\Class 5\Maths\Master.json", encoding="utf-8"))
chs = m.get("chapters", [])
print(f"Maths Master.json chapters count: {len(chs)}")
ch1 = chs[0]
qb = ch1.get("question_bank", {})
print("Ch 1 question_bank keys:", list(qb.keys()) if isinstance(qb, dict) else type(qb))
if isinstance(qb, dict):
    for k, v in qb.items():
        if isinstance(v, list):
            print(f"  Key '{k}': {len(v)} items")
            if len(v) > 0 and isinstance(v[0], dict):
                print(f"    Sample Item 0 keys: {list(v[0].keys())}")

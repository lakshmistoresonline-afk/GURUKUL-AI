import json

data = json.load(open('D:/GURUKUL/Contents/Class 5/Science/Science Master.json', encoding='utf-8'))
ch1 = data['chapters'][0]

print("=== SCIENCE CHAPTER 1 KEYS & PAYLOADS ===")
for k, v in ch1.items():
    if isinstance(v, list):
        print(f"Key '{k}': List[{len(v)} items]")
        if v:
            print(f"   Sample item: {v[0]}")
    elif isinstance(v, dict):
        print(f"Key '{k}': Dict with keys {list(v.keys())}")
    else:
        print(f"Key '{k}': {type(v).__name__} = {str(v)[:50]}")

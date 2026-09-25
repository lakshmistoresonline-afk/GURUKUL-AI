import os
import json

root = r"D:\GURUKUL\Contents\Class 5\Hindi"

for f in sorted(os.listdir(root)):
    if f.endswith(".json"):
        fpath = os.path.join(root, f)
        data = json.load(open(fpath, encoding="utf-8"))
        print(f"================ File: {f} ================")
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, list):
                    print(f"  Key '{k}': List of {len(v)} items")
                    if len(v) > 0 and isinstance(v[0], dict):
                        print(f"    Sample Item 0 keys: {list(v[0].keys())}")
                elif isinstance(v, dict):
                    print(f"  Key '{k}': Dict with keys {list(v.keys())}")
                else:
                    print(f"  Key '{k}': {v}")

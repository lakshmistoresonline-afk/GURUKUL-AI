import os
import json

root = r"D:\GURUKUL\Contents\Class 5"

flash_keys = set()
mind_keys = set()
sq_keys = set()

for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith(".json"):
            fpath = os.path.join(dp, f)
            data = json.load(open(fpath, encoding="utf-8"))

            def search_dict(d):
                if isinstance(d, dict):
                    for k, v in d.items():
                        if k == "flashcards" or k == "cards":
                            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                                flash_keys.update(v[0].keys())
                        elif "mindmap" in k.lower():
                            if isinstance(v, dict):
                                mind_keys.update(v.keys())
                                if "sub_nodes" in v and isinstance(v["sub_nodes"], list) and len(v["sub_nodes"]) > 0:
                                    mind_keys.update(v["sub_nodes"][0].keys())
                        elif "question" in k.lower() or "quiz" in k.lower():
                            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
                                sq_keys.update(v[0].keys())
                        search_dict(v)
                elif isinstance(d, list):
                    for item in d:
                        search_dict(item)

            search_dict(data)

print("Flashcard keys found across all datasets:", sorted(list(flash_keys)))
print("\nMindmap keys found across all datasets:", sorted(list(mind_keys)))
print("\nQuestion keys found across all datasets:", sorted(list(sq_keys)))

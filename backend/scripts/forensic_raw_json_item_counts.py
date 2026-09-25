import os
import json

root_dir = r"D:\GURUKUL\Contents\Class 5"

print("==========================================================================")
print("FORENSIC RAW SOURCE JSON ITEM-BY-ITEM AUDIT ACROSS ALL 20 DATASETS")
print("==========================================================================\n")

for sub in ["English", "Hindi", "Maths", "Science"]:
    sub_dir = os.path.join(root_dir, sub)
    print(f"================ SUBJECT: Class 5 {sub} ================")

    if not os.path.exists(sub_dir):
        print("  Directory not found!")
        continue

    for fname in sorted(os.listdir(sub_dir)):
        if fname.endswith(".json"):
            fpath = os.path.join(sub_dir, fname)
            size = os.path.getsize(fpath)
            data = json.load(open(fpath, encoding="utf-8"))

            print(f"\n--- FILE: {sub}/{fname} ({size:,} bytes) ---")

            if isinstance(data, dict):
                for k, v in data.items():
                    if isinstance(v, list):
                        print(f"  Top-level Array '{k}': Total {len(v)} items")
                        # Inspect items per chapter if items have chapter info
                        ch_counts = {}
                        for item in v:
                            if isinstance(item, dict):
                                c_num = item.get("chapterNumber") or item.get("chapter_number") or item.get("chapter_no") or item.get("chapter") or item.get("unit")
                                if c_num is not None:
                                    ch_counts[c_num] = ch_counts.get(c_num, 0) + 1
                                # Check nested lists inside chapter items (e.g. questions, flashcards)
                                for sub_k, sub_v in item.items():
                                    if isinstance(sub_v, list):
                                        c_id = item.get("chapterNumber") or item.get("chapter_number") or item.get("chapter_no") or item.get("chapter_title") or "item"
                                        # print(f"      Nested list '{sub_k}' in chapter {c_id}: {len(sub_v)} items")
                        if ch_counts:
                            print(f"    Per-chapter item distribution: {dict(sorted(ch_counts.items()))}")
                    elif isinstance(v, dict):
                        print(f"  Top-level Dict '{k}': {len(v)} keys ({list(v.keys())[:5]})")
                    else:
                        print(f"  Top-level Key '{k}': {v}")
            elif isinstance(data, list):
                print(f"  Root Array: Total {len(data)} items")

    print("\n" + "-" * 74)

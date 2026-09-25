import os
import json

def inspect_datasets():
    p = r"D:\GURUKUL\Contents\Class 5\English"
    files = sorted(os.listdir(p))

    print("=== DEEP DATASET CONTENT & RECORD COUNT INSPECTION ===")

    for f in files:
        fpath = os.path.join(p, f)
        data = json.load(open(fpath, encoding="utf-8"))
        print(f"\nFILE: {f}")
        print(f"  Top Keys: {list(data.keys())}")

        # Check primary array key
        for main_key in ["chapters", "cards", "questions", "units"]:
            if main_key in data:
                arr = data[main_key]
                print(f"  Primary Array '{main_key}': length = {len(arr)}")
                if arr and isinstance(arr[0], dict):
                    print(f"  Sample Item Keys in '{main_key}': {list(arr[0].keys())}")

        # Check for specific keys in chapters
        if "chapters" in data and isinstance(data["chapters"], list):
            sample_ch = data["chapters"][0]
            print(f"  Sample Chapter Title: {sample_ch.get('chapterTitle') or sample_ch.get('title')}")

if __name__ == "__main__":
    inspect_datasets()

import os
import json
import hashlib

def run_inventory_table():
    p = r"D:\GURUKUL\Contents\Class 5\English"
    files = sorted(os.listdir(p))

    print("=== COMPLETE AUTHORITATIVE SOURCE FILE INVENTORY ===")
    print(f"{'Filename':<35} | {'Size(B)':<8} | {'SHA-256 Hash':<64} | {'Root':<5} | {'Primary Record Count'}")
    print("-" * 140)

    for fname in files:
        fpath = os.path.join(p, fname)
        size = os.path.getsize(fpath)
        sha = hashlib.sha256(open(fpath, "rb").read()).hexdigest()
        data = json.load(open(fpath, encoding="utf-8"))
        root = type(data).__name__

        counts_str = ""
        if "chapters" in data and isinstance(data["chapters"], list):
            counts_str = f"10 Chapters"
        elif "cards" in data and isinstance(data["cards"], list):
            counts_str = f"{len(data['cards'])} Cards"
        elif "questions" in data and isinstance(data["questions"], list):
            counts_str = f"{len(data['questions'])} Questions"
        elif "units" in data and isinstance(data["units"], list):
            counts_str = f"{len(data['units'])} Units, 4 Goals"

        print(f"{fname:<35} | {size:<8} | {sha:<64} | {root:<5} | {counts_str}")

if __name__ == "__main__":
    run_inventory_table()

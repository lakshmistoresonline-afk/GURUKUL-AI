import os
import json
import hashlib

print("==========================================================================")
print("CLASS 6 CONTENTS FORENSIC AUDIT")
print("==========================================================================\n")

class6_root = r"D:\GURUKUL\Contents\Class 6"
if not os.path.exists(class6_root):
    print(f"Class 6 directory not found at {class6_root}")
    exit(1)

inventory = []

for subject in sorted(os.listdir(class6_root)):
    subj_dir = os.path.join(class6_root, subject)
    if os.path.isdir(subj_dir):
        print(f"Subject: {subject}")
        for fname in sorted(os.listdir(subj_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(subj_dir, fname)
                bdata = open(fpath, "rb").read()
                sha = hashlib.sha256(bdata).hexdigest()
                try:
                    data = json.loads(bdata.decode("utf-8"))
                    keys = list(data.keys()) if isinstance(data, dict) else []
                    ch_count = len(data.get("chapters", [])) if isinstance(data, dict) else 0
                except Exception:
                    keys = []
                    ch_count = 0

                inventory.append({
                    "subject": subject,
                    "file": fname,
                    "sizeBytes": len(bdata),
                    "sha256": sha,
                    "rootKeys": keys,
                    "chapterCount": ch_count
                })
                print(f"  - {fname}: {len(bdata):,} bytes | keys={keys} | chapters={ch_count}")

reports_dir = r"D:\GURUKUL\reports"
os.makedirs(reports_dir, exist_ok=True)
with open(os.path.join(reports_dir, "CLASS6_SOURCE_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump(inventory, f, ensure_ascii=False, indent=2)

print(f"\nTotal Class 6 Source Files Discovered: {len(inventory)}")
print("CLASS 6 SOURCE INVENTORY GENERATED SUCCESSFULLY!")

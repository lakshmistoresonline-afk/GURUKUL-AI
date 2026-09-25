import os
import json
import hashlib

print("==========================================================================")
print("CLASS 5 MANDATORY SOURCE FORENSIC AUDIT")
print("==========================================================================\n")

contents_root = r"D:\GURUKUL\Contents\Class 5"
source_inventory = []

for subject in ["English", "Hindi", "Maths", "Science"]:
    subj_dir = os.path.join(contents_root, subject)
    if not os.path.exists(subj_dir):
        continue
    for fname in sorted(os.listdir(subj_dir)):
        if fname.endswith(".json"):
            fpath = os.path.join(subj_dir, fname)
            bdata = open(fpath, "rb").read()
            sha = hashlib.sha256(bdata).hexdigest()
            try:
                data = json.loads(bdata.decode("utf-8"))
                root_keys = list(data.keys()) if isinstance(data, dict) else []
                ch_count = len(data.get("chapters", [])) if isinstance(data, dict) else 0
            except Exception:
                root_keys = []
                ch_count = 0

            source_inventory.append({
                "subject": subject,
                "file": fname,
                "sha256": sha,
                "sizeBytes": len(bdata),
                "rootKeys": root_keys,
                "chapterCount": ch_count
            })

print(f"Total Source Files Audited: {len(source_inventory)}")
for item in source_inventory:
    print(f"  - [{item['subject']}] {item['file']}: size={item['sizeBytes']:,} bytes | keys={item['rootKeys']} | chapters={item['chapterCount']}")

reports_dir = r"D:\GURUKUL\reports"
os.makedirs(reports_dir, exist_ok=True)
with open(os.path.join(reports_dir, "CLASS5_SOURCE_FORENSIC_INVENTORY.json"), "w", encoding="utf-8") as f:
    json.dump(source_inventory, f, ensure_ascii=False, indent=2)

print("\nSOURCE FORENSIC INVENTORY GENERATED SUCCESSFULLY!")

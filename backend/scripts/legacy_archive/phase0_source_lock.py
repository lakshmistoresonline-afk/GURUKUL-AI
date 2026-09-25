import os
import json
import hashlib

root_dir = r"D:\GURUKUL\Contents\Class 5"
manifest_path = r"D:\GURUKUL\reports\CLASS5_SOURCE_LOCK_MANIFEST.json"

print("==========================================================================")
print("PHASE 0: DISCOVER, FINGERPRINT & LOCK ALL SOURCE DATASETS")
print("==========================================================================\n")

source_lock = {
    "expectedDatasetCount": 20,
    "actualDatasetCount": 0,
    "datasets": []
}

for dp, dn, fn in os.walk(root_dir):
    for f in sorted(fn):
        if f.endswith(".json"):
            fpath = os.path.join(dp, f)
            rel_path = os.path.relpath(fpath, root_dir)
            file_size = os.path.getsize(fpath)

            content_bytes = open(fpath, "rb").read()
            sha256 = hashlib.sha256(content_bytes).hexdigest()

            parsed = json.loads(content_bytes.decode("utf-8"))
            root_type = type(parsed).__name__
            top_keys = list(parsed.keys()) if isinstance(parsed, dict) else [f"array_len_{len(parsed)}"]

            sub = rel_path.split(os.sep)[0]

            ds_entry = {
                "sourceDatasetId": f"G5-{sub[:3].upper()}-SRC-{len(source_lock['datasets'])+1:03d}",
                "grade": "5",
                "subject": sub,
                "filename": f,
                "relPath": rel_path,
                "absolutePath": fpath,
                "sizeBytes": file_size,
                "sourceHash": sha256,
                "rootType": root_type,
                "topKeys": top_keys,
                "schemaFingerprint": f"G5_{sub.upper()}_{f.replace('.', '_')}_V3"
            }
            source_lock["datasets"].append(ds_entry)

source_lock["actualDatasetCount"] = len(source_lock["datasets"])

os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(source_lock, f, indent=2, ensure_ascii=False)

print(f"Phase 0 Lock Completed!")
print(f"  Expected Datasets: 20 | Actual Datasets Discovered: {source_lock['actualDatasetCount']}")
print(f"  Lock Manifest Saved: {manifest_path}\n")

for ds in source_lock["datasets"]:
    print(f"  - [{ds['sourceDatasetId']}] {ds['subject']} / {ds['filename']} ({ds['sizeBytes']:,} bytes) | Hash: {ds['sourceHash'][:16]}...")

print("\n" + "=" * 74)

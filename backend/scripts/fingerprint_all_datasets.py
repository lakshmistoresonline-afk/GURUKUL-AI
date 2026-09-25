import os
import json
import hashlib

root_dir = r"D:\GURUKUL\Contents\Class 5"

print("==========================================================================")
print("DEEP SCHEMA FINGERPRINTING & RECORD AUDIT FOR ALL 24 JSON DATASETS")
print("==========================================================================\n")

datasets_info = []

for dp, dn, fn in os.walk(root_dir):
    for f in sorted(fn):
        if f.endswith(".json"):
            fpath = os.path.join(dp, f)
            rel_path = os.path.relpath(fpath, root_dir)
            file_size = os.path.getsize(fpath)

            content_bytes = open(fpath, "rb").read()
            sha256 = hashlib.sha256(content_bytes).hexdigest()

            try:
                data = json.loads(content_bytes.decode("utf-8"))
                root_type = type(data).__name__
                top_keys = list(data.keys()) if isinstance(data, dict) else [f"array_len_{len(data)}"]

                datasets_info.append({
                    "rel_path": rel_path,
                    "fpath": fpath,
                    "file_size": file_size,
                    "sha256": sha256,
                    "root_type": root_type,
                    "top_keys": top_keys,
                    "data": data
                })
            except Exception as e:
                print(f"ERROR reading {rel_path}: {e}")

print(f"Total Datasets Discovered: {len(datasets_info)}\n")

for ds in datasets_info:
    print(f"Dataset: {ds['rel_path']}")
    print(f"  Size: {ds['file_size']} bytes | SHA256: {ds['sha256'][:16]}...")
    print(f"  Root Type: {ds['root_type']} | Top Keys: {ds['top_keys'][:8]}")

    # Detailed record inspection
    data = ds['data']
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list):
                print(f"    - Key '{k}': List of {len(v)} items")
            elif isinstance(v, dict):
                print(f"    - Key '{k}': Dict with {len(v)} sub-keys ({list(v.keys())[:5]})")
            else:
                print(f"    - Key '{k}': Primitive ({type(v).__name__}) = {str(v)[:40]}")
    elif isinstance(data, list):
        print(f"    - Array of {len(data)} root items")
    print("-" * 74)

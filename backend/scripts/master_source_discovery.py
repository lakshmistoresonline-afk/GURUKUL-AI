import os
import json
import hashlib

def run_master_discovery():
    contents_root = r"D:\GURUKUL\Contents"
    print("==========================================================================")
    print("AUTHORITATIVE RECURSIVE SOURCE DISCOVERY ACROSS ALL CLASSES & SUBJECTS")
    print("==========================================================================\n")

    inventory = []

    for root, dirs, files in os.walk(contents_root):
        for fname in sorted(files):
            if fname.endswith(".json"):
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, contents_root)
                size = os.path.getsize(fpath)
                raw_bytes = open(fpath, "rb").read()
                sha = hashlib.sha256(raw_bytes).hexdigest()

                try:
                    data = json.loads(raw_bytes.decode("utf-8"))
                    root_type = type(data).__name__
                    top_keys = list(data.keys()) if isinstance(data, dict) else []
                except Exception as e:
                    root_type = "INVALID_JSON"
                    top_keys = [str(e)]
                    data = None

                path_parts = rel_path.split(os.sep)
                cls_name = path_parts[0] if len(path_parts) > 0 else "Unknown"
                sub_name = path_parts[1] if len(path_parts) > 1 else "Unknown"

                inventory.append({
                    "rel_path": rel_path,
                    "abs_path": fpath,
                    "filename": fname,
                    "class": cls_name,
                    "subject": sub_name,
                    "size": size,
                    "sha256": sha,
                    "root_type": root_type,
                    "top_keys": top_keys,
                    "data": data
                })

                print(f"File: {rel_path}")
                print(f"  Class: {cls_name} | Subject: {sub_name}")
                print(f"  Size: {size} bytes | SHA256: {sha}")
                print(f"  Root Type: {root_type} | Top Keys: {top_keys}")
                print("-" * 74)

    print(f"\nTotal JSON Datasets Discovered: {len(inventory)}")
    return inventory

if __name__ == "__main__":
    run_master_discovery()

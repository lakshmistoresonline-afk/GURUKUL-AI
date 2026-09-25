import os
import json
import hashlib

def run_source_audit():
    source_dir = r"D:\GURUKUL\Contents\Class 5\English"
    files = sorted(os.listdir(source_dir))

    print(f"=== AUTHORITATIVE SOURCE DIRECTORY AUDIT ===")
    print(f"Directory: {source_dir}\n")
    print(f"Total files found: {len(files)}\n")

    file_details = []

    for fname in files:
        fpath = os.path.join(source_dir, fname)
        if not os.path.isfile(fpath):
            continue

        size = os.path.getsize(fpath)
        content_bytes = open(fpath, "rb").read()
        sha256_hash = hashlib.sha256(content_bytes).hexdigest()

        try:
            json_obj = json.loads(content_bytes.decode("utf-8"))
            root_type = type(json_obj).__name__

            if isinstance(json_obj, dict):
                top_keys = sorted(list(json_obj.keys()))
            elif isinstance(json_obj, list):
                top_keys = [f"Array[{len(json_obj)} items]"]
            else:
                top_keys = [str(json_obj)]
        except Exception as e:
            root_type = "INVALID_JSON"
            top_keys = [str(e)]
            json_obj = None

        file_details.append({
            "filename": fname,
            "path": fpath,
            "size": size,
            "sha256": sha256_hash,
            "root_type": root_type,
            "top_keys": top_keys,
            "data": json_obj
        })

    return file_details

if __name__ == "__main__":
    details = run_source_audit()
    for item in details:
        print(f"File: {item['filename']}")
        print(f"  Path: {item['path']}")
        print(f"  Size: {item['size']} bytes")
        print(f"  SHA-256: {item['sha256']}")
        print(f"  Root Type: {item['root_type']}")
        print(f"  Top Keys: {item['top_keys']}")
        print("-" * 60)

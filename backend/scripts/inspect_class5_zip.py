import os
import zipfile
import hashlib

zip_path = r"D:\GURUKUL\Contents\Class 5.zip"
print(f"Checking {zip_path}: exists={os.path.exists(zip_path)}")

if os.path.exists(zip_path):
    size = os.path.getsize(zip_path)
    bdata = open(zip_path, "rb").read()
    sha = hashlib.sha256(bdata).hexdigest()
    print(f"  Size: {size:,} bytes | SHA256: {sha}")

    with zipfile.ZipFile(zip_path, "r") as z:
        namelist = z.namelist()
        print(f"  Total items inside zip: {len(namelist)}")
        json_items = [n for n in namelist if n.endswith(".json")]
        print(f"  JSON files inside zip: {len(json_items)}")
        for j in sorted(json_items):
            print(f"    - {j}")

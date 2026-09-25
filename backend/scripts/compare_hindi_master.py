import os
import hashlib

dl_path = r"C:\Users\srina\Downloads\Class 5\Hindi\Master.json"
ct_path = r"D:\GURUKUL\Contents\Class 5\Hindi\Master.json"

dl_bytes = open(dl_path, "rb").read()
ct_bytes = open(ct_path, "rb").read()

dl_sha = hashlib.sha256(dl_bytes).hexdigest()
ct_sha = hashlib.sha256(ct_bytes).hexdigest()

print(f"Downloads Master.json: {len(dl_bytes):,} bytes | SHA256: {dl_sha}")
print(f"Contents Master.json:  {len(ct_bytes):,} bytes | SHA256: {ct_sha}")
print(f"Hash Match: {dl_sha == ct_sha}")

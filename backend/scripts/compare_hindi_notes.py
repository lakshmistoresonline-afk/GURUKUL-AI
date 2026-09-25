import os
import hashlib

dl_path = r"C:\Users\srina\Downloads\Class 5\Hindi\Notes.json"
ct_path = r"D:\GURUKUL\Contents\Class 5\Hindi\Notes.json"

dl_bytes = open(dl_path, "rb").read()
ct_bytes = open(ct_path, "rb").read()

dl_sha = hashlib.sha256(dl_bytes).hexdigest()
ct_sha = hashlib.sha256(ct_bytes).hexdigest()

print(f"Downloads Notes.json: {len(dl_bytes):,} bytes | SHA256: {dl_sha}")
print(f"Contents Notes.json:  {len(ct_bytes):,} bytes | SHA256: {ct_sha}")
print(f"Hash Match: {dl_sha == ct_sha}")

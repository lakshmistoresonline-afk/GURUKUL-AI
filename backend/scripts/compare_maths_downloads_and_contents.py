import os
import json
import hashlib

dl_dir = r"C:\Users\srina\Downloads\Class 5\Maths"
ct_dir = r"D:\GURUKUL\Contents\Class 5\Maths"

print("==========================================================================")
print("DEEP FORENSIC COMPARISON OF MATHS JSON FILES")
print("==========================================================================\n")

for fname in ["Notes.json", "Master.json", "Flashcards.json", "Mindmaps.json", "Quiz.json"]:
    dl_path = os.path.join(dl_dir, fname)
    ct_path = os.path.join(ct_dir, fname)

    dl_exists = os.path.exists(dl_path)
    ct_exists = os.path.exists(ct_path)

    print(f"--- File: {fname} ---")
    print(f"  Downloads Path Exists: {dl_exists}")
    print(f"  Contents Path Exists:  {ct_exists}")

    if dl_exists:
        dl_bytes = open(dl_path, "rb").read()
        dl_sha = hashlib.sha256(dl_bytes).hexdigest()
        dl_size = len(dl_bytes)
        dl_json = json.loads(dl_bytes.decode("utf-8"))
        print(f"  Downloads Size: {dl_size:,} bytes | SHA256: {dl_sha[:16]}...")
        print(f"  Downloads Top Keys: {list(dl_json.keys()) if isinstance(dl_json, dict) else 'Array'}")

    if ct_exists:
        ct_bytes = open(ct_path, "rb").read()
        ct_sha = hashlib.sha256(ct_bytes).hexdigest()
        ct_size = len(ct_bytes)
        ct_json = json.loads(ct_bytes.decode("utf-8"))
        print(f"  Contents Size:  {ct_size:,} bytes | SHA256: {ct_sha[:16]}...")
        print(f"  Contents Top Keys:  {list(ct_json.keys()) if isinstance(ct_json, dict) else 'Array'}")

    if dl_exists and ct_exists:
        match = (dl_sha == ct_sha)
        print(f"  >>> HASH MATCH: {match}")

    print()

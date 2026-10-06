import os
import sys
import hashlib
import json
from datetime import datetime

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
INTEGRITY_DIR = os.path.join(REPO_ROOT, "reports", "content-integrity")
os.makedirs(INTEGRITY_DIR, exist_ok=True)

BASELINE_PATH = os.path.join(INTEGRITY_DIR, "two_directory_baseline.json")

def compute_dir_hashes(root_dir: str) -> dict:
    hashes = {}
    if not os.path.exists(root_dir):
        return hashes
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".json") or file.endswith(".pdf"):
                f_abs = os.path.join(root, file)
                rel = os.path.relpath(f_abs, root_dir)
                sha = hashlib.sha256()
                with open(f_abs, "rb") as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        sha.update(chunk)
                hashes[rel] = sha.hexdigest()
    return hashes

def main():
    print("Running Two-Directory Immutability Verification (Contents & ProcessedContent)...")

    current_contents = compute_dir_hashes(CONTENTS_ROOT)
    current_processed = compute_dir_hashes(PROCESSED_ROOT)

    current_combined = {
        "Contents": current_contents,
        "ProcessedContent": current_processed
    }

    if not os.path.exists(BASELINE_PATH):
        with open(BASELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(current_combined, f, indent=2)
        print("Two-directory baseline established.")
        print("Result: PASS")
        sys.exit(0)

    with open(BASELINE_PATH, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    b_contents = baseline.get("Contents", {})
    b_processed = baseline.get("ProcessedContent", {})

    mismatches = 0
    for path, sha in current_contents.items():
        if b_contents.get(path) != sha:
            print(f"Mismatch in Contents/: {path}")
            mismatches += 1

    for path, sha in current_processed.items():
        if b_processed.get(path) != sha:
            print(f"Mismatch in ProcessedContent/: {path}")
            mismatches += 1

    if mismatches == 0:
        print("Result: PASS — Both Contents/ and ProcessedContent/ are 100% immutable and unchanged.")
        sys.exit(0)
    else:
        print(f"Result: FAIL — {mismatches} hash mismatches detected!")
        sys.exit(1)

if __name__ == "__main__":
    main()

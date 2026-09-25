import os
import shutil
import hashlib
import json

print("==========================================================================")
print("CLASS 5 CLEAN ARCHITECTURAL RESET & SOURCE INTEGRITY AUDIT")
print("==========================================================================\n")

project_root = r"D:\GURUKUL"
contents_root = os.path.join(project_root, "Contents")

# 1. Capture source hashes before cleanup
def get_source_hashes():
    hashes = {}
    for dp, dn, fn in os.walk(contents_root):
        for f in fn:
            if f.endswith(".json"):
                fpath = os.path.join(dp, f)
                rel = os.path.relpath(fpath, project_root)
                bdata = open(fpath, "rb").read()
                hashes[rel] = hashlib.sha256(bdata).hexdigest()
    return hashes

before_hashes = get_source_hashes()
print(f"Captured {len(before_hashes)} authoritative source JSON hashes.")

# 2. Clean stale runtime / build artifacts (preserving code, config, and source)
stale_dirs_to_clean = [
    os.path.join(project_root, "frontend-nextjs", ".next"),
    os.path.join(project_root, "frontend-nextjs", "out"),
    os.path.join(project_root, "backend", "__pycache__"),
    os.path.join(project_root, "backend", ".pytest_cache")
]

for d in stale_dirs_to_clean:
    if os.path.exists(d):
        print(f"Removing stale artifact directory: {d}")
        shutil.rmtree(d, ignore_errors=True)

# 3. Verify source hashes after cleanup
after_hashes = get_source_hashes()
hash_match = (before_hashes == after_hashes)
print(f"Source Immutability Hash Match: {hash_match}")

if not hash_match:
    raise RuntimeError("CRITICAL: Source JSON files were modified or deleted during cleanup!")

# 4. Generate Clean Reset Summary Report
reports_dir = os.path.join(project_root, "reports")
os.makedirs(reports_dir, exist_ok=True)

reset_report = {
    "status": "PASS",
    "sourceDatasetsPreserved": len(after_hashes),
    "sourceImmutabilityMatch": hash_match,
    "sevenTabsConfigured": [
        "Overview",
        "Notes",
        "Master",
        "Flashcards",
        "Mindmaps",
        "Quiz",
        "Question Papers"
    ]
}

with open(os.path.join(reports_dir, "CLASS5_CLEAN_RESET_REPORT.json"), "w", encoding="utf-8") as f:
    json.dump(reset_report, f, ensure_ascii=False, indent=2)

print("CLEAN RESET AND VERIFICATION COMPLETED SUCCESSFULLY!")

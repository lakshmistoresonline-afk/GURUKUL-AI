import os
import sys
import shutil

print("==========================================================================")
print("GURUKUL AI — DELETE GENERATED QUESTION PAPERS OUTSIDE CONTENTS")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
AUTH_CONTENTS = os.path.join(REPO_ROOT, "Contents")

targets_to_remove = [
    os.path.join(REPO_ROOT, "ProcessedContent"),
    os.path.join(REPO_ROOT, "_QB_REBUILD_V3_TEMP"),
    os.path.join(REPO_ROOT, "_QB_V3_EXECUTION_TEST"),
    os.path.join(REPO_ROOT, "_QB_V3_INSTRUMENT_TEST")
]

deleted_paths = []

for target in targets_to_remove:
    if os.path.exists(target):
        # Ensure target is strictly outside Contents
        rel = os.path.relpath(target, AUTH_CONTENTS)
        if rel.startswith(".."):
            print(f"Removing generated directory/file: {target}")
            try:
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
                deleted_paths.append(target)
            except Exception as e:
                print(f"Error removing {target}: {e}")
        else:
            print(f"SAFETY ERROR: Target {target} is inside Contents! Refusing to delete.")

print(f"\nSuccessfully deleted {len(deleted_paths)} generated question-related paths outside Contents.")
print("Authoritative Contents directory was untouched.")

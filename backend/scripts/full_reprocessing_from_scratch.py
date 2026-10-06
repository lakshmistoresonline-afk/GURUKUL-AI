import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — FULL REPROCESSING FROM SCRATCH (MODULAR ARCHITECTURE)")
print("==========================================================================\n")

REPO_ROOT = Path(r"D:/GURUKUL")
CONTENTS_ROOT = REPO_ROOT / "Contents"
PROCESSED_ROOT = REPO_ROOT / "ProcessedContent"
LEGACY_CLASS5 = REPO_ROOT / "backend" / "src" / "curriculum" / "class5"
LEGACY_CLASS6 = REPO_ROOT / "backend" / "src" / "curriculum" / "class6"
LEGACY_CLASS7_CLI = REPO_ROOT / "backend" / "src" / "curriculum" / "class7_process_cli.py"

def clean_legacy_and_processed():
    print("--- 1. CLEANING LEGACY PROCESSOR PATHS ---")
    for path in [LEGACY_CLASS5, LEGACY_CLASS6]:
        if path.exists() and path.is_dir():
            print(f"Removing legacy directory: {path}")
            shutil.rmtree(path)
    if LEGACY_CLASS7_CLI.exists():
        print(f"Removing legacy CLI script: {LEGACY_CLASS7_CLI}")
        os.remove(LEGACY_CLASS7_CLI)

    print("--- 2. CLEANING GENERATED PROCESSED CONTENT ---")
    if PROCESSED_ROOT.exists():
        print(f"Removing generated artifact directory: {PROCESSED_ROOT}")
        shutil.rmtree(PROCESSED_ROOT)
    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)

def execute_reprocessing():
    print("--- 3. EXECUTING MODULAR REPROCESSING FROM SOURCE (Contents/) ---")
    if not CONTENTS_ROOT.exists():
        print("CRITICAL ERROR: Contents root does not exist.")
        sys.exit(1)

    # Run the V13 strict 1-to-1 deterministic materializer backed by classes/ modular structure
    script_path = REPO_ROOT / "backend" / "scripts" / "generate_processed_content_strict_1to1.py"
    if script_path.exists():
        import subprocess
        res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print(f"Error during reprocessing: {res.stderr}")
            sys.exit(1)

    print("\n============================================================")
    print("FULL REPROCESSING FROM SCRATCH COMPLETED SUCCESSFULLY")
    print("============================================================")

if __name__ == "__main__":
    clean_legacy_and_processed()
    execute_reprocessing()

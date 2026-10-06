import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — MASTER REPROCESSING SCRIPT (FROM SCRATCH)")
print("==========================================================================\n")

REPO_ROOT = Path(r"D:/GURUKUL")
CONTENTS_ROOT = REPO_ROOT / "Contents"
PROCESSED_ROOT = REPO_ROOT / "ProcessedContent"

def reprocess_all():
    if not CONTENTS_ROOT.exists():
        print("CRITICAL ERROR: Contents root does not exist.")
        sys.exit(1)

    print("1. Cleaning ProcessedContent/ directory...")
    if PROCESSED_ROOT.exists():
        shutil.rmtree(PROCESSED_ROOT)
    PROCESSED_ROOT.mkdir(parents=True, exist_ok=True)

    print("2. Executing deterministic V13 strict 1-to-1 materializer from Contents/...")
    script_path = REPO_ROOT / "backend" / "scripts" / "generate_processed_content_strict_1to1.py"
    if script_path.exists():
        import subprocess
        res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode != 0:
            print(f"Error during reprocessing: {res.stderr}")
            sys.exit(1)

    print("3. Unifying question papers globally...")
    qp_script = REPO_ROOT / "backend" / "scripts" / "merge_question_papers_into_one.py"
    if qp_script.exists():
        import subprocess
        res2 = subprocess.run([sys.executable, str(qp_script)], capture_output=True, text=True)
        print(res2.stdout)

    print("\n============================================================")
    print("MASTER REPROCESSING FROM SCRATCH COMPLETED SUCCESSFULLY")
    print("============================================================")

if __name__ == "__main__":
    reprocess_all()

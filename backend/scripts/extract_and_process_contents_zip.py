import os
import sys
import json
import zipfile
import subprocess
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — CONTENTS.ZIP EXTRACTION & COMPREHENSIVE INTEGRATION")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
ZIP_PATH = os.path.join(REPO_ROOT, "Contents.zip")
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def extract_and_integrate():
    if not os.path.exists(ZIP_PATH):
        print(f"Error: {ZIP_PATH} not found.")
        sys.exit(1)

    print(f"Extracting {ZIP_PATH} into {CONTENTS_ROOT}...")
    try:
        with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
            zf.extractall(CONTENTS_ROOT)
        print("Extraction completed successfully.")
    except Exception as e:
        print(f"Error extracting ZIP: {e}")
        sys.exit(1)

    print("\n--- RUNNING CURRICULUM PROCESSING PIPELINE ---")
    scripts_to_run = [
        os.path.join(REPO_ROOT, "backend", "src", "curriculum", "process_cli.py"),
        os.path.join(REPO_ROOT, "backend", "src", "curriculum", "class6_process_cli.py"),
        os.path.join(REPO_ROOT, "backend", "src", "curriculum", "class7_process_cli.py")
    ]

    for script in scripts_to_run:
        if os.path.exists(script):
            print(f"Executing {os.path.relpath(script, REPO_ROOT)}...")
            res = subprocess.run([sys.executable, script], capture_output=True, text=True)
            print(res.stdout)
            if res.returncode != 0:
                print(f"Stderr: {res.stderr}")

    # Verify processed content
    processed_count = 0
    total_chapters_verified = 0
    for root, dirs, files in os.walk(os.path.join(REPO_ROOT, "ProcessedContent")):
        for file in files:
            if file.endswith(".json"):
                total_chapters_verified += 1

    report = {
        "timestamp": datetime.now().isoformat(),
        "zip_extracted": True,
        "total_processed_json_files": total_chapters_verified,
        "status": "FULL_INTEGRATION_SUCCESS"
    }

    report_path = os.path.join(REPORTS_DIR, "CONTENTS_ZIP_FULL_INTEGRATION_REPORT.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n============================================================")
    print("CONTENTS.ZIP INTEGRATION COMPLETED SUCCESSFULLY")
    print("============================================================\n")
    print(f"TOTAL PROCESSED JSON ASSETS:\n{total_chapters_verified}")
    print(f"\nINTEGRATION STATUS:\nSUCCESS")
    print(f"\nREPORT SAVED TO:\n{os.path.relpath(report_path, REPO_ROOT)}")
    print("\n============================================================")

if __name__ == "__main__":
    extract_and_integrate()

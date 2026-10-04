import os
import sys
import json
import subprocess
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — MASTER ORCHESTRATION: CLASS & SUBJECT SEPARATE PROCESSORS")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_all_processors():
    print("--- 1. EXECUTING CLASS 5 PROCESSORS ---")
    p5 = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "backend", "src", "curriculum", "process_cli.py")], capture_output=True, text=True)
    print(p5.stdout)
    if p5.stderr:
        print(p5.stderr)

    print("--- 2. EXECUTING CLASS 6 PROCESSORS ---")
    p6 = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "backend", "src", "curriculum", "class6_process_cli.py")], capture_output=True, text=True)
    print(p6.stdout)
    if p6.stderr:
        print(p6.stderr)

    print("--- 3. EXECUTING CLASS 7 PROCESSORS ---")
    p7 = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "backend", "src", "curriculum", "class7_process_cli.py")], capture_output=True, text=True)
    print(p7.stdout)
    if p7.stderr:
        print(p7.stderr)

    print("--- 4. EXECUTING FOUNDATIONAL JSON PROCESSOR ---")
    pf = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "backend", "scripts", "process_foundational_json.py")], capture_output=True, text=True)
    print(pf.stdout)
    if pf.stderr:
        print(pf.stderr)

    print("--- 5. EXECUTING QUESTION PAPER UNIFIER ---")
    pq = subprocess.run([sys.executable, os.path.join(REPO_ROOT, "backend", "scripts", "merge_question_papers_into_one.py")], capture_output=True, text=True)
    print(pq.stdout)
    if pq.stderr:
        print(pq.stderr)

    print("\n============================================================")
    print("MASTER ORCHESTRATION PIPELINE COMPLETED SUCCESSFULLY")
    print("============================================================")

if __name__ == "__main__":
    run_all_processors()

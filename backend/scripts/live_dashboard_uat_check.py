import os
import sys
import json
from datetime import datetime

print("==========================================================================")
print("GURUKUL AI — UAT PROCESSED CONTENT DIRECT INTEGRITY VERIFICATION")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_direct_uat():
    print("--- 1. VERIFYING DIRECT PROCESSED CONTENT ASSETS ---")
    if not os.path.isdir(PROCESSED_ROOT):
        print("CRITICAL ERROR: ProcessedContent root does not exist.")
        sys.exit(1)

    total_chapters = 0
    missing_files = []
    verified_files = 0

    required_sections = ["overview.json", "notes.json", "master.json", "mindmaps.json", "flashcards.json", "quiz.json", "question_papers.json", "foundational.json", "manifest.json"]

    for class_dir in os.listdir(PROCESSED_ROOT):
        class_path = os.path.join(PROCESSED_ROOT, class_dir)
        if not os.path.isdir(class_path):
            continue
        for subj_dir in os.listdir(class_path):
            subj_path = os.path.join(class_path, subj_dir)
            if not os.path.isdir(subj_path):
                continue
            for ch_dir in os.listdir(subj_path):
                ch_path = os.path.join(subj_path, ch_dir)
                if not os.path.isdir(ch_path):
                    continue
                total_chapters += 1
                for sec in required_sections:
                    sec_path = os.path.join(ch_path, sec)
                    if os.path.exists(sec_path):
                        verified_files += 1
                    else:
                        missing_files.append(os.path.relpath(sec_path, REPO_ROOT))

    uat_result = {
        "timestamp": datetime.now().isoformat(),
        "total_chapters_audited": total_chapters,
        "required_sections_per_chapter": len(required_sections),
        "total_files_verified": verified_files,
        "missing_files_count": len(missing_files),
        "missing_files": missing_files,
        "uat_verdict": "DIRECT_UAT_PASSED" if len(missing_files) == 0 else "DIRECT_UAT_WARNINGS"
    }

    report_path = os.path.join(REPORTS_DIR, "LIVE_DASHBOARD_UAT_REPORT.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(uat_result, f, ensure_ascii=False, indent=2)

    print("\n============================================================")
    print("UAT PROCESSED CONTENT DIRECT INTEGRITY VERIFICATION COMPLETED")
    print("============================================================\n")
    print(f"TOTAL CHAPTERS AUDITED:\n{total_chapters}")
    print(f"\nTOTAL FILES VERIFIED:\n{verified_files:,}")
    print(f"\nMISSING FILES:\n{len(missing_files)}")
    print(f"\nVERDICT:\n{'DIRECT_UAT_PASSED' if len(missing_files) == 0 else 'DIRECT_UAT_WARNINGS'}")
    print(f"\nREPORT SAVED TO:\n{os.path.relpath(report_path, REPO_ROOT)}")
    print("\n============================================================")

if __name__ == "__main__":
    run_direct_uat()

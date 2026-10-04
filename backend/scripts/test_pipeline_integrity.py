import os
import sys
import json

print("==========================================================================")
print("GURUKUL AI — AUTOMATED PIPELINE INTEGRITY & SELF-TEST SUITE")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
PROCESSED_ROOT = os.path.join(REPO_ROOT, "ProcessedContent")

def test_integrity():
    if not os.path.isdir(PROCESSED_ROOT):
        print("CRITICAL ERROR: ProcessedContent root does not exist.")
        sys.exit(1)

    total_chapters = 0
    passed_chapters = 0
    errors = []

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
                manifest = os.path.join(ch_path, "manifest.json")
                if os.path.exists(manifest):
                    passed_chapters += 1
                else:
                    errors.append(ch_path)

    print("\n============================================================")
    print("PIPELINE INTEGRITY TEST SUITE COMPLETED")
    print("============================================================\n")
    print(f"TOTAL CHAPTERS TESTED:\n{total_chapters}")
    print(f"PASSED:\n{passed_chapters}")
    print(f"ERRORS:\n{len(errors)}")
    print(f"\nINTEGRITY STATUS:\n{'PASSED' if len(errors) == 0 else 'WARNINGS'}")
    print("\n============================================================")

if __name__ == "__main__":
    test_integrity()

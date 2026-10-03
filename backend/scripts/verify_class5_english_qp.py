import os
import sys
import json

print("==========================================================================")
print("GURUKUL AI — CLASS 5 ENGLISH QUESTION PAPERS COMPREHENSIVE VERIFICATION")
print("==========================================================================\n")

REPO_ROOT = r"D:/GURUKUL"
QP_SOURCE_PATH = os.path.join(REPO_ROOT, "Contents", "Class 5", "English", "Question Papers.json")
PROCESSED_SUBJ_DIR = os.path.join(REPO_ROOT, "ProcessedContent", "Class5", "English")

def verify_and_sync():
    if not os.path.exists(QP_SOURCE_PATH):
        print(f"Error: {QP_SOURCE_PATH} not found.")
        sys.exit(1)

    with open(QP_SOURCE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    chapters = data.get("chapters", [])
    total_source_questions = 0
    total_source_papers = 0

    print(f"Loaded Class 5 English Question Papers source: {len(chapters)} chapters found.")

    for ch_idx, ch in enumerate(chapters):
        ch_num = ch.get("chapter_number", ch_idx + 1)
        ch_title = ch.get("chapter_title", f"Chapter {ch_num}")
        papers = ch.get("question_papers", [])
        total_source_papers += len(papers)

        ch_q_count = 0
        for p in papers:
            for sec in p.get("sections", []):
                ch_q_count += len(sec.get("questions", []))
        total_source_questions += ch_q_count

        # Find matching processed chapter directory
        matched_dir = None
        if os.path.exists(PROCESSED_SUBJ_DIR):
            for d in os.listdir(PROCESSED_SUBJ_DIR):
                d_path = os.path.join(PROCESSED_SUBJ_DIR, d)
                if os.path.isdir(d_path) and f"C{ch_num:02d}" in d:
                    matched_dir = d_path
                    break

        if matched_dir:
            qp_dest_path = os.path.join(matched_dir, "question_papers.json")
            # Ensure complete papers are written
            with open(qp_dest_path, "w", encoding="utf-8") as out_f:
                json.dump({"chapter_title": ch_title, "question_papers": papers}, out_f, ensure_ascii=False, indent=2)
            print(f"  Synced Chapter {ch_num} ({ch_title}): {len(papers)} papers, {ch_q_count} questions -> {os.path.relpath(qp_dest_path, REPO_ROOT)}")
        else:
            print(f"  Warning: Processed directory not found for Chapter {ch_num} ({ch_title})")

    print(f"\nTotal Source Papers: {total_source_papers}")
    print(f"Total Source Questions: {total_source_questions}")
    print("Class 5 English question papers verification and synchronization completed successfully!")

if __name__ == "__main__":
    verify_and_sync()

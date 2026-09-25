import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def audit_exact_item_counts():
    subjects = ["English", "Hindi", "Maths", "Science"]
    print("==========================================================================")
    print("EXACT SOURCE DATASET ITEM COUNTS ACROSS ALL SUBJECTS & CHAPTERS")
    print("==========================================================================\n")

    for sub in subjects:
        files = ContentLoaderService.load_raw_subject_files("5", sub)
        print(f"SUBJECT: Class 5 {sub} (Discovered Files: {list(files.keys())})")

        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])

        for u in units:
            for ch in u.get("chapters", []):
                ch_num = ch.get("chapterNumber")
                ch_id = ch.get("id")

                # Load raw source
                ch_source = ContentLoaderService.load_chapter_source("5", sub, ch_id)

                # Inspect items in ch_source
                flash_count = len(ch_source.get("flashcards", [])) if isinstance(ch_source.get("flashcards"), list) else 0
                quiz_count = len(ch_source.get("quiz", [])) if isinstance(ch_source.get("quiz"), list) else len(ch_source.get("interactive_quiz", [])) if isinstance(ch_source.get("interactive_quiz"), list) else len(ch_source.get("quizzes_mcq", [])) if isinstance(ch_source.get("quizzes_mcq"), list) else 0

                qb = ch_source.get("question_bank") or ch_source.get("studyQuestions") or ch_source.get("practiceQuestions") or {}
                if isinstance(qb, dict):
                    mcq_c = len(qb.get("mcqs", [])) or len(qb.get("multipleChoiceQuestions", []))
                    sa_c = len(qb.get("short_answers", [])) or len(qb.get("shortAnswerQuestions", []))
                else:
                    mcq_c = 0
                    sa_c = 0

                print(f"  Ch {ch_num:02d} ({ch_id}): {flash_count:2d} Flashcards | {quiz_count:2d} Quiz Questions | Practice MCQs: {mcq_c} | Practice SAs: {sa_c}")

        print("-" * 74)

if __name__ == "__main__":
    audit_exact_item_counts()

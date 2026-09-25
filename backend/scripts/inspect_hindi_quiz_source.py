import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def inspect_hindi_quiz():
    files = ContentLoaderService.load_raw_subject_files("5", "Hindi")
    print("Files in Class 5 Hindi:", list(files.keys()))

    hin_master = files.get("Hindi Master.json", {})
    master_data = hin_master.get("chapters_master_data", [])
    print(f"\nHindi Master chapters_master_data count: {len(master_data)}")

    ch1 = next((c for c in master_data if c.get("chapter_number") == 1), {})
    print("Ch 1 keys in Hindi Master.json:", list(ch1.keys()))
    print("Ch 1 'interactive_quiz':", ch1.get("interactive_quiz"))

    # Also check Hindi Quiz.json
    hin_quiz_file = files.get("Quiz.json", {})
    print("\nQuiz.json keys:", list(hin_quiz_file.keys()))
    quiz_chs = hin_quiz_file.get("chapters", [])
    print(f"Quiz.json chapters count: {len(quiz_chs)}")
    q_ch1 = next((c for c in quiz_chs if c.get("chapter_number") == 1 or c.get("chapterNumber") == 1), {})
    print("Quiz.json Ch 1 keys:", list(q_ch1.keys()))
    if q_ch1:
        print("Quiz.json Ch 1 questions count:", len(q_ch1.get("questions", [])))

    # Also check class_5_hindi_master_quiz_bank.json if present
    master_qb_file = files.get("Master.json", {})
    print("\nMaster.json keys:", list(master_qb_file.keys()))

if __name__ == "__main__":
    inspect_hindi_quiz()

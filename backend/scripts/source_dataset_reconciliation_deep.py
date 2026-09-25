import os
import json
import hashlib

def run_deep_comparison():
    p = r"D:\GURUKUL\Contents\Class 5\English"

    print("=== DEEP COMPARISON OF VARIANT & COMPLEMENTARY DATASETS ===")

    # 1. santoor_flashcards vs santoor_flashcards (1)
    f1_path = os.path.join(p, "santoor_flashcards.json")
    f2_path = os.path.join(p, "santoor_flashcards (1).json")
    h1 = hashlib.sha256(open(f1_path, "rb").read()).hexdigest()
    h2 = hashlib.sha256(open(f2_path, "rb").read()).hexdigest()
    print(f"\nFlashcards Comparison:")
    print(f"  santoor_flashcards.json SHA256:     {h1}")
    print(f"  santoor_flashcards (1).json SHA256: {h2}")
    print(f"  Identical Bytes? {h1 == h2}")

    # 2. santoor_quiz vs santoor_quiz (1)
    q1_path = os.path.join(p, "santoor_quiz.json")
    q2_path = os.path.join(p, "santoor_quiz (1).json")
    hq1 = hashlib.sha256(open(q1_path, "rb").read()).hexdigest()
    hq2 = hashlib.sha256(open(q2_path, "rb").read()).hexdigest()
    print(f"\nQuiz Comparison:")
    print(f"  santoor_quiz.json SHA256:     {hq1}")
    print(f"  santoor_quiz (1).json SHA256: {hq2}")
    print(f"  Identical Bytes? {hq1 == hq2}")

    q1_data = json.load(open(q1_path, encoding="utf-8")).get("questions", [])
    q2_data = json.load(open(q2_path, encoding="utf-8")).get("questions", [])
    print(f"  q1 count: {len(q1_data)} | q2 count: {len(q2_data)}")
    if len(q1_data) == len(q2_data):
        diffs = 0
        for i in range(len(q1_data)):
            if q1_data[i] != q2_data[i]:
                diffs += 1
                print(f"    Diff at Q{i+1}: Q1='{q1_data[i].get('question')}' vs Q2='{q2_data[i].get('question')}'")
        print(f"  Total differences between quiz files: {diffs}")

    # 3. Assessment / Testbank Datasets
    print("\nAssessment / Question Bank Datasets Overview:")
    notes_data = json.load(open(os.path.join(p, "santoor_chapters_notes.json"), encoding="utf-8")).get("chapters", [])
    tb_data = json.load(open(os.path.join(p, "santoor_master_testbank.json"), encoding="utf-8")).get("chapters", [])
    mqb_data = json.load(open(os.path.join(p, "santoor_model_question_bank.json"), encoding="utf-8")).get("chapters", [])

    print(f"  notes.studyQuestions chapters count: {len(notes_data)}")
    print(f"  master_testbank chapters count: {len(tb_data)}")
    print(f"  model_question_bank chapters count: {len(mqb_data)}")

if __name__ == "__main__":
    run_deep_comparison()

import os
import json

def inspect_subject_masters():
    p = r"D:\GURUKUL\Contents\Class 5"

    print("==========================================================================")
    print("MASTER DATASETS DEEP STRUCTURAL INSPECTION (ALL 4 SUBJECTS)")
    print("==========================================================================\n")

    # 1. English Master
    eng_file = os.path.join(p, "English", "English Master.json")
    if os.path.exists(eng_file):
        eng = json.load(open(eng_file, encoding="utf-8"))
        eng_chs = eng.get("chapters", [])
        print(f"1. ENGLISH MASTER: {len(eng_chs)} Chapters")
        if eng_chs:
            print(f"   Chapter 1 Title: {eng_chs[0].get('chapterTitle')}")
            print(f"   Chapter 1 Keys: {list(eng_chs[0].keys())}")

    # 2. Hindi Master
    hin_file = os.path.join(p, "Hindi", "Hindi Master.json")
    if os.path.exists(hin_file):
        hin = json.load(open(hin_file, encoding="utf-8"))
        hin_chs = hin.get("chapters_master_data", [])
        print(f"\n2. HINDI MASTER: {len(hin_chs)} Chapters")
        if hin_chs:
            ch1_info = hin_chs[0].get("chapter_info", {})
            print(f"   Chapter 1 Title: {ch1_info.get('title')} ({ch1_info.get('title_hindi')})")
            print(f"   Chapter 1 Keys: {list(hin_chs[0].keys())}")

    # 3. Science Master
    sci_file = os.path.join(p, "Science", "Science Master.json")
    if os.path.exists(sci_file):
        sci = json.load(open(sci_file, encoding="utf-8"))
        sci_chs = sci.get("chapters", [])
        print(f"\n3. SCIENCE MASTER: {len(sci_chs)} Chapters")
        if sci_chs:
            print(f"   Chapter 1 Title: {sci_chs[0].get('chapterTitle')}")
            print(f"   Chapter 1 Keys: {list(sci_chs[0].keys())}")

    # 4. Maths Master
    math_file = os.path.join(p, "Maths", "Maths Master.json")
    if os.path.exists(math_file):
        m = json.load(open(math_file, encoding="utf-8"))
        print(f"\n4. MATHS MASTER: Top Level Keys = {list(m.keys())}")
        for key in ["chapter_notes", "flashcards", "quizzes_mcq", "vsa_questions", "sa_questions", "la_questions", "case_study_questions", "sample_question_papers"]:
            arr = m.get(key, [])
            print(f"   '{key}': {len(arr)} records")
            if arr and isinstance(arr[0], dict):
                print(f"     Sample item keys in '{key}': {list(arr[0].keys())}")

if __name__ == "__main__":
    inspect_subject_masters()

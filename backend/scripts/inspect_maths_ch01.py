import json

data = json.load(open('D:/GURUKUL/Contents/Class 5/Maths/Maths Master.json', encoding='utf-8'))

print("=== MATHS MASTER KEYS & PAYLOADS ===")
for k in ["chapter_notes", "flashcards", "quizzes_mcq", "vsa_questions", "sa_questions", "la_questions", "case_study_questions", "sample_question_papers"]:
    arr = data.get(k, [])
    print(f"Key '{k}': List[{len(arr)} items]")
    if arr:
        print(f"   Sample item for Ch 1: {next((x for x in arr if x.get('chapter_number') == 1 or 1 in x.get('associated_chapters', [])), None)}")

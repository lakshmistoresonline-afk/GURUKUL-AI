import json

fpath = r"D:\GURUKUL\Contents\Class 5\English\English Master.json"
data = json.load(open(fpath, encoding="utf-8"))

print("==========================================================================")
print("ENGLISH MASTER.JSON FIELD-BY-FIELD AUDIT & PIPELINE TRACE")
print("==========================================================================\n")

print("TOP-LEVEL METADATA:")
print(f"  title: {data.get('title')}")
print(f"  textbook: {data.get('textbook')}")
print(f"  publisher: {data.get('publisher')}")
print(f"  grade: {data.get('grade')}")
print(f"  curriculumFramework: {data.get('curriculumFramework')}")
print(f"  totalChapters: {data.get('totalChapters')}")
print(f"  summaryStatistics: {data.get('summaryStatistics')}\n")

chapters = data.get("chapters", [])
print(f"CHAPTERS COUNT: {len(chapters)}\n")

for i, ch in enumerate(chapters, 1):
    c_num = ch.get("chapterNumber")
    c_title = ch.get("chapterTitle")
    u_num = ch.get("unitNumber")
    u_title = ch.get("unitTitle")
    c_type = ch.get("chapterType")

    notes = ch.get("notes", {})
    vocab = ch.get("vocabulary", [])
    grammar = ch.get("grammar", {})
    flashcards = ch.get("flashcards", [])
    quiz = ch.get("quiz", [])
    fib = ch.get("fillInTheBlanks", {})
    sub_q = ch.get("subjectiveQuestionBank", {})
    model_p = ch.get("sampleModelPaper", {})
    writing = ch.get("creativeWritingTasks", [])

    print(f"Chapter {c_num}: {c_title} (Unit {u_num}: {u_title} | Type: {c_type})")
    print(f"  - notes: overview({bool(notes.get('overview'))}), centralTheme({bool(notes.get('centralTheme'))}), detailedBreakdown({len(notes.get('detailedBreakdown', []))}), poeticDevices({bool(notes.get('poeticDevices'))}), characterAnalysis({len(notes.get('characterAnalysis', []))}), takeaways({len(notes.get('importantTakeaways', []))})")
    print(f"  - vocabulary: {len(vocab)} terms")
    print(f"  - grammar: conceptTitle({grammar.get('conceptTitle')}), rules({len(grammar.get('rules', []))}), practiceExercises({len(grammar.get('practiceExercises', []))})")
    print(f"  - flashcards: {len(flashcards)} cards")
    print(f"  - quiz: {len(quiz)} questions")
    print(f"  - fillInTheBlanks: wordBank({len(fib.get('wordBank', []))}), exercises({len(fib.get('exercises', []))})")
    print(f"  - subjectiveQuestionBank: partA({len(sub_q.get('partA', {}).get('questions', []))}), partB({len(sub_q.get('partB', {}).get('questions', []))}), partC({len(sub_q.get('partC', {}).get('questions', []))}), partD({bool(sub_q.get('partD'))})")
    print(f"  - sampleModelPaper: maxMarks({model_p.get('maxMarks')}), sectionA({len(model_p.get('sectionA', {}).get('questions', []))}), sectionB({len(model_p.get('sectionB', {}).get('questions', []))}), sectionC({len(model_p.get('sectionC', {}).get('questions', []))}), sectionD({bool(model_p.get('sectionD'))})")
    print(f"  - creativeWritingTasks: {len(writing)} tasks")
    print("-" * 74)

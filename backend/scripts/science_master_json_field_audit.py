import json

fpath = r"D:\GURUKUL\Contents\Class 5\Science\Science Master.json"
data = json.load(open(fpath, encoding="utf-8"))

print("==========================================================================")
print("SCIENCE MASTER.JSON FIELD-BY-FIELD AUDIT & PIPELINE TRACE")
print("==========================================================================\n")

print("TOP-LEVEL METADATA:")
print(f"  title: {data.get('title')}")
print(f"  grade: {data.get('grade')}")
print(f"  subject: {data.get('subject')}")
print(f"  curriculumFramework: {data.get('curriculumFramework')}")
print(f"  sourceTextbook: {data.get('sourceTextbook')}")
print(f"  totalChapters: {data.get('totalChapters')}")
print(f"  totalStudyItems: {data.get('totalStudyItems')}")
print(f"  totalExamQuestions: {data.get('totalExamQuestions')}")
print(f"  grandTotalItems: {data.get('grandTotalItems')}\n")

chapters = data.get("chapters", [])
print(f"CHAPTERS COUNT: {len(chapters)}\n")

for i, ch in enumerate(chapters, 1):
    c_num = ch.get("chapterNumber")
    c_title = ch.get("chapterTitle")
    u_title = ch.get("unit")

    summary = ch.get("summary", {})
    principles = ch.get("scientificPrinciples", [])
    glossary = ch.get("glossary", [])
    did_you_know = ch.get("didYouKnow", [])
    activities = ch.get("activities", [])
    formulas = ch.get("numericalsAndFormulas", [])
    practice = ch.get("practiceQuestions", {})
    model_p = ch.get("modelQuestionPaper", {})

    print(f"Chapter {c_num}: {c_title} (Unit: {u_title})")
    print(f"  - summary: overview({bool(summary.get('overview'))}), keySections({len(summary.get('keySections', []))})")
    print(f"  - scientificPrinciples: {len(principles)} principles")
    print(f"  - glossary: {len(glossary)} terms")
    print(f"  - didYouKnow: {len(did_you_know)} facts")
    print(f"  - activities: {len(activities)} experiments")
    print(f"  - numericalsAndFormulas: {len(formulas)} items")
    print(f"  - practiceQuestions: FIB({len(practice.get('fillInTheBlanks', []))}), TF({len(practice.get('trueFalse', []))}), Analytical({len(practice.get('analyticalProblems', []))}), NCERT({len(practice.get('ncertComprehension', []))}), AR({len(practice.get('assertionReason', []))}), MCQ({len(practice.get('multipleChoice', []))}), SA({len(practice.get('shortAnswer', []))}), LA({len(practice.get('longAnswer', []))})")
    print(f"  - modelQuestionPaper: totalMarks({model_p.get('totalMarks')}), duration({model_p.get('duration')}), sections({len(model_p.get('sections', []))})")
    print("-" * 74)

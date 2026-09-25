import json

fpath = r"D:\GURUKUL\Contents\Class 5\Maths\Maths Master.json"
data = json.load(open(fpath, encoding="utf-8"))

print("==========================================================================")
print("MATHS MASTER.JSON FIELD-BY-FIELD AUDIT & PIPELINE TRACE")
print("==========================================================================\n")

print("TOP-LEVEL METADATA:")
print(f"  app_title: {data.get('app_title')}")
print(f"  curriculum: {data.get('curriculum')}")
print(f"  total_chapters: {data.get('total_chapters')}")
print(f"  summary_counts: {data.get('summary_counts')}\n")

notes = data.get("chapter_notes", [])
flashcards = data.get("flashcards", [])
mcqs = data.get("quizzes_mcq", [])
vsas = data.get("vsa_questions", [])
sas = data.get("sa_questions", [])
las = data.get("la_questions", [])
case_studies = data.get("case_study_questions", [])
papers = data.get("sample_question_papers", [])

print(f"COLLECTION COUNTS:")
print(f"  - chapter_notes: {len(notes)}")
print(f"  - flashcards: {len(flashcards)}")
print(f"  - quizzes_mcq: {len(mcqs)}")
print(f"  - vsa_questions: {len(vsas)}")
print(f"  - sa_questions: {len(sas)}")
print(f"  - la_questions: {len(las)}")
print(f"  - case_study_questions: {len(case_studies)}")
print(f"  - sample_question_papers: {len(papers)}\n")

for i in range(1, 16):
    ch_note = next((n for n in notes if n.get("chapter_number") == i), {})
    ch_title = ch_note.get("chapter_title", f"Chapter {i}")
    ch_flash = [f for f in flashcards if f.get("chapter_number") == i]
    ch_mcq = [m for m in mcqs if m.get("chapter_number") == i]
    ch_vsa = [v for v in vsas if v.get("chapter_number") == i]
    ch_sa = [s for s in sas if s.get("chapter_number") == i]
    ch_la = [l for l in las if l.get("chapter_number") == i]
    ch_case = [c for c in case_studies if i in c.get("associated_chapters", [])]
    ch_paper = next((p for p in papers if p.get("chapter_number") == i), {})

    print(f"Chapter {i}: {ch_title} (Theme: {ch_note.get('theme')})")
    print(f"  - notes: summary({bool(ch_note.get('summary'))}), conceptual_foundation({len(ch_note.get('conceptual_foundation', {}).get('core_definitions', []))}), key_methods({len(ch_note.get('key_methods', []))})")
    print(f"  - flashcards: {len(ch_flash)} cards")
    print(f"  - quizzes_mcq: {len(ch_mcq)} MCQs")
    print(f"  - vsa_questions: {len(ch_vsa)} VSAs")
    print(f"  - sa_questions: {len(ch_sa)} SAs")
    print(f"  - la_questions: {len(ch_la)} LAs")
    print(f"  - case_study_questions: {len(ch_case)} Case Studies")
    print(f"  - sample_question_paper: paper_title({bool(ch_paper.get('paper_title'))}), max_marks({ch_paper.get('max_marks')}), sections({4 if ch_paper else 0})")
    print("-" * 74)

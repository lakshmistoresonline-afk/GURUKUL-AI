import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def audit_science_nested():
    print("==========================================================================")
    print("FORENSIC SCIENCE NESTED RECORDS AUDIT (10 CHAPTERS)")
    print("==========================================================================\n")

    files = ContentLoaderService.load_raw_subject_files("5", "Science")
    notes_chs = files.get("Notes.json", {}).get("chapters", [])
    master_chs = files.get("Master.json", {}).get("chapters", [])
    quiz_chs = files.get("Quiz.json", {}).get("chapters", [])
    flash_chs = files.get("Flashcards.json", {}).get("flashcards", [])
    mm_chs = files.get("Mindmaps.json", {}).get("chapters", [])

    print(f"Notes.json chapters: {len(notes_chs)}")
    print(f"Master.json chapters: {len(master_chs)}")
    print(f"Quiz.json chapters: {len(quiz_chs)}")
    print(f"Flashcards.json cards: {len(flash_chs)}")
    print(f"Mindmaps.json chapters: {len(mm_chs)}")

    print("\n--- CHAPTER 1 (G5-SCI-U01-C01) DETAILED NESTED RECORD COUNTS ---")
    ch1_notes = notes_chs[0] if notes_chs else {}
    ch1_master = master_chs[0] if master_chs else {}

    # Notes.json nested lists
    summary_obj = ch1_notes.get("summary", {})
    key_sec = summary_obj.get("keySections", []) if isinstance(summary_obj, dict) else []
    principles = ch1_notes.get("scientificPrinciples", [])
    glossary = ch1_notes.get("glossary", [])
    facts = ch1_notes.get("didYouKnow", [])
    activities = ch1_notes.get("activities", [])
    formulas = ch1_notes.get("numericalsAndFormulas", [])
    practice_notes = ch1_notes.get("practiceQuestions", {})

    print(f"Notes.json Key Sections: {len(key_sec)}")
    print(f"Notes.json Scientific Principles: {len(principles)}")
    print(f"Notes.json Glossary Terms: {len(glossary)}")
    print(f"Notes.json Did You Know Facts: {len(facts)}")
    print(f"Notes.json Activities: {len(activities)}")
    print(f"Notes.json Formulas/Numericals: {len(formulas)}")
    print(f"Notes.json Practice Questions Keys: {list(practice_notes.keys()) if isinstance(practice_notes, dict) else 0}")

    # Master.json nested lists
    concepts = ch1_master.get("concepts", [])
    experiments = ch1_master.get("experiments_and_activities", [])
    case_studies = ch1_master.get("case_studies_and_stories", [])
    qb_master = ch1_master.get("question_bank", {})

    print(f"Master.json Concepts: {len(concepts)}")
    print(f"Master.json Experiments & Activities: {len(experiments)}")
    print(f"Master.json Case Studies: {1 if case_studies else 0}")
    print(f"Master.json Question Bank Keys: {list(qb_master.keys()) if isinstance(qb_master, dict) else 0}")

if __name__ == "__main__":
    audit_science_nested()

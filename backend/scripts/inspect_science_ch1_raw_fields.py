import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

files = ContentLoaderService.load_raw_subject_files("5", "Science")
notes_chs = files.get("Notes.json", {}).get("chapters", [])
ch1 = notes_chs[0] if notes_chs else {}

print("--- Notes.json Chapter 1 Fields ---")
print("scientificPrinciples:", json.dumps(ch1.get("scientificPrinciples"), indent=2, ensure_ascii=False))
print("activities:", json.dumps(ch1.get("activities"), indent=2, ensure_ascii=False))
print("glossary:", json.dumps(ch1.get("glossary"), indent=2, ensure_ascii=False))
print("didYouKnow:", json.dumps(ch1.get("didYouKnow"), indent=2, ensure_ascii=False))
print("practiceQuestions keys:", list(ch1.get("practiceQuestions", {}).keys()))

master_chs = files.get("Master.json", {}).get("chapters", [])
m_ch1 = master_chs[0] if master_chs else {}
print("\n--- Master.json Chapter 1 Fields ---")
print("concepts:", json.dumps(m_ch1.get("concepts"), indent=2, ensure_ascii=False))
print("experiments_and_activities:", json.dumps(m_ch1.get("experiments_and_activities"), indent=2, ensure_ascii=False))
print("question_bank keys:", list(m_ch1.get("question_bank", {}).keys()))

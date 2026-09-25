import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

files = ContentLoaderService.load_raw_subject_files("5", "Hindi")
notes_chs = files.get("Notes.json", {}).get("chapters", [])
master_chs = files.get("Hindi Master.json", {}).get("chapters_master_data", [])

ch1_notes = next((c for c in notes_chs if c.get("chapter_number") == 1 or c.get("chapter_no") == 1), {})
ch1_master = next((c for c in master_chs if c.get("chapter_number") == 1 or c.get("chapter_no") == 1), {})

print("--- Hindi Notes.json Chapter 1 Top Keys ---")
print(list(ch1_notes.keys()))

print("\n--- Hindi Master.json Chapter 1 Top Keys ---")
print(list(ch1_master.keys()))
print("Chapter Info:", list(ch1_master.get("chapter_info", {}).keys()))
print("Question Bank keys:", list(ch1_master.get("question_bank", {}).keys()))
print("Model Question Paper keys:", list(ch1_master.get("model_question_paper", {}).keys()))

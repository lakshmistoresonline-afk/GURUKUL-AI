import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

files = ContentLoaderService.load_raw_subject_files("5", "English")
flash_file = files.get("Flashcards.json", {})
print("English Flashcards.json top keys:", list(flash_file.keys()))
if isinstance(flash_file, dict):
    for k, v in flash_file.items():
        if isinstance(v, list) and v:
            print(f"  {k}: list with {len(v)} items. Sample item 0 keys: {list(v[0].keys()) if isinstance(v[0], dict) else type(v[0])}")
        else:
            print(f"  {k}: {type(v)}")

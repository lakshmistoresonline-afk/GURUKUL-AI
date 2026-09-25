import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

ch_source = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U05-C10")
flash = ch_source.get("flashcards", [])
print(f"Chapter 10 Flashcards count: {len(flash)}")
if flash:
    print("Sample card 0 keys:", list(flash[0].keys()))
    print("Sample card 0 content:", flash[0])

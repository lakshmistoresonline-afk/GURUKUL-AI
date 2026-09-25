import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

ch_source = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
print("English Ch 1 flashcards count:", len(ch_source.get("flashcards", [])))
print("Sample flashcard:", ch_source.get("flashcards", [])[:2])

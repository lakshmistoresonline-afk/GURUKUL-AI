import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

ch_source = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
adapter = AdapterResolver.resolve("NCERT", "5", "English", ch_source)
blocks = adapter.parse_chapter(ch_source, "G5-ENG-U01-C01")

print("English Ch 1 parsed blocks:")
for b in blocks:
    print(f"  id: {b.id} | sourceType: {b.sourceType} | normalizedType: {b.normalizedType} | renderer: {b.renderer}")
    if b.sourceType == "flashcards":
        print(f"    Flashcards data count: {len(b.data) if isinstance(b.data, list) else type(b.data)}")

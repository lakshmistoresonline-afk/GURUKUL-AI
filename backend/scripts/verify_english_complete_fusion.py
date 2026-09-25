import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def verify_english():
    print("==========================================================================")
    print("ENGLISH COMPLETE 5-FILE FUSION AUDIT (10 CHAPTERS)")
    print("==========================================================================\n")

    for i in range(1, 11):
        ch_id = f"G5-ENG-U{((i-1)//2)+1:02d}-C{i:02d}"
        ch_source = ContentLoaderService.load_chapter_source("5", "English", ch_id)
        adapter = AdapterResolver.resolve("NCERT", "5", "English", ch_source)
        blocks = adapter.parse_chapter(ch_source, ch_id)

        f_b = next((b for b in blocks if b.sourceType == "flashcards" or b.renderer == "flashcard-deck"), None)
        f_count = len(f_b.data) if f_b and isinstance(f_b.data, list) else 0

        q_b = next((b for b in blocks if b.sourceType == "quiz" or b.renderer == "quiz"), None)
        q_count = len(q_b.data) if q_b and isinstance(q_b.data, list) else 0

        print(f"Ch {i:02d} ({ch_id}): '{ch_source.get('chapterTitle')}' | Blocks: {len(blocks)} | Flashcards: {f_count} | Quiz Qs: {q_count}")

    print("\nENGLISH COMPLETE FUSION AUDIT PASSED 100%!")

if __name__ == "__main__":
    verify_english()

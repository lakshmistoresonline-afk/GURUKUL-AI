import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def audit_hindi():
    print("==========================================================================")
    print("DEEP FORENSIC AUDIT OF HINDI SOURCE FILES & CHAPTER INGESTION")
    print("==========================================================================\n")

    files = ContentLoaderService.load_raw_subject_files("5", "Hindi")
    notes_chs = files.get("Notes.json", {}).get("chapters", [])
    master_chs = files.get("Hindi Master.json", {}).get("chapters_master_data", [])
    quiz_chs = files.get("Quiz.json", {}).get("chapters", [])
    flash_chs = files.get("Flashcards.json", {}).get("flashcards", [])
    mm_chs = files.get("Mindmaps.json", {}).get("chapters", [])

    print(f"Notes.json chapters count: {len(notes_chs)}")
    print(f"Hindi Master.json chapters count: {len(master_chs)}")
    print(f"Quiz.json chapters count: {len(quiz_chs)}")
    print(f"Flashcards.json cards count: {len(flash_chs)}")
    print(f"Mindmaps.json chapters count: {len(mm_chs)}")

    for i in range(1, 13):
        ch_id = f"G5-HIN-U{((i-1)//3)+1:02d}-C{i:02d}"
        ch_source = ContentLoaderService.load_chapter_source("5", "Hindi", ch_id)
        adapter = AdapterResolver.resolve("NCERT", "5", "Hindi", ch_source)
        blocks = adapter.parse_chapter(ch_source, ch_id)

        print(f"\nHindi Ch {i:02d} ({ch_id}):")
        print(f"  Title: '{ch_source.get('chapterTitle')}'")
        print(f"  Blocks count: {len(blocks)} | Renderers: {[b.renderer for b in blocks]}")
        print(f"  Flashcards count: {len(ch_source.get('flashcards', []))}")
        print(f"  Quiz Qs count: {len(ch_source.get('interactive_quiz', []))}")
        print(f"  Shabdart items: {len(ch_source.get('shabdart', []) or [])}")
        print(f"  Grammar keys: {list(ch_source.get('grammar_extraction', {}).keys()) if isinstance(ch_source.get('grammar_extraction'), dict) else type(ch_source.get('grammar_extraction'))}")

if __name__ == "__main__":
    audit_hindi()

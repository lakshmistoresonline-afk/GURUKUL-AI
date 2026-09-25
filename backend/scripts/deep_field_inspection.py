import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def deep_inspect_all_files():
    p = 'D:/GURUKUL/Contents/Class 5/English'
    print("=== DEEP SOURCE FILE FIELD INSPECTION ===")

    # 1. santoor_chapters_notes.json
    notes_raw = json.load(open(os.path.join(p, 'santoor_chapters_notes.json'), encoding='utf-8'))
    print("\n1. santoor_chapters_notes.json Top Keys:", list(notes_raw.keys()))
    chapters_notes = notes_raw.get('chapters', [])
    print(f"Total chapters in notes: {len(chapters_notes)}")
    all_notes_keys = set()
    for c in chapters_notes:
        all_notes_keys.update(c.keys())
    print("All keys discovered across chapters in notes:", sorted(list(all_notes_keys)))

    # Check studyQuestions internal keys
    all_sq_keys = set()
    for c in chapters_notes:
        sq = c.get('studyQuestions', {})
        if isinstance(sq, dict):
            all_sq_keys.update(sq.keys())
    print("All keys inside studyQuestions:", sorted(list(all_sq_keys)))

    # Check overview internal keys
    all_ov_keys = set()
    for c in chapters_notes:
        ov = c.get('overview', {})
        if isinstance(ov, dict):
            all_ov_keys.update(ov.keys())
    print("All keys inside overview:", sorted(list(all_ov_keys)))

    # 2. santoor_flashcards.json
    flash_raw = json.load(open(os.path.join(p, 'santoor_flashcards.json'), encoding='utf-8'))
    print("\n2. santoor_flashcards.json Top Keys:", list(flash_raw.keys()))
    cards = flash_raw.get('cards', [])
    print(f"Total cards in array: {len(cards)}")
    all_card_keys = set()
    for card in cards:
        all_card_keys.update(card.keys())
    print("All keys discovered across flashcards:", sorted(list(all_card_keys)))

    # 3. santoor_mindmap.json
    mm_raw = json.load(open(os.path.join(p, 'santoor_mindmap.json'), encoding='utf-8'))
    print("\n3. santoor_mindmap.json Top Keys:", list(mm_raw.keys()))
    mm_units = mm_raw.get('units', [])
    print(f"Total units in mindmap: {len(mm_units)}")
    all_mm_ch_keys = set()
    for u in mm_units:
        for ch in u.get('chapters', []):
            all_mm_ch_keys.update(ch.keys())
    print("All keys discovered across chapter mindmaps:", sorted(list(all_mm_ch_keys)))

    # 4. santoor_quiz.json
    quiz_raw = json.load(open(os.path.join(p, 'santoor_quiz.json'), encoding='utf-8'))
    print("\n4. santoor_quiz.json Top Keys:", list(quiz_raw.keys()))
    quiz_questions = quiz_raw.get('questions', [])
    print(f"Total quiz questions: {len(quiz_questions)}")
    all_quiz_keys = set()
    for q in quiz_questions:
        all_quiz_keys.update(q.keys())
    print("All keys discovered across quiz questions:", sorted(list(all_quiz_keys)))

if __name__ == "__main__":
    deep_inspect_all_files()

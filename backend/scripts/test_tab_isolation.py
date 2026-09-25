import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.routes.universal_routes import get_chapter_content_by_type
import asyncio

async def test_isolation():
    ch_id = "G5-ENG-U01-C01"

    quiz_blocks = await get_chapter_content_by_type(ch_id, "quiz")
    flash_blocks = await get_chapter_content_by_type(ch_id, "flashcards")
    mindmap_blocks = await get_chapter_content_by_type(ch_id, "mindmap")

    print("=== TAB ISOLATION AUDIT ===")
    print(f"Quiz Endpoint returned {len(quiz_blocks)} blocks.")
    print("Quiz block sourceType:", [b["sourceType"] for b in quiz_blocks])
    assert all(b["sourceType"] == "quiz" for b in quiz_blocks)

    print(f"\nFlashcards Endpoint returned {len(flash_blocks)} blocks.")
    print("Flashcards block sourceType:", [b["sourceType"] for b in flash_blocks])
    assert all(b["sourceType"] == "flashcards" for b in flash_blocks)

    print(f"\nMindmap Endpoint returned {len(mindmap_blocks)} blocks.")
    print("Mindmap block sourceType:", [b["sourceType"] for b in mindmap_blocks])
    assert all(b["sourceType"] == "mindmap" for b in mindmap_blocks)

    print("\nTAB DATA ISOLATION PASSED WITH 0 LEAKAGE!")

if __name__ == "__main__":
    asyncio.run(test_isolation())

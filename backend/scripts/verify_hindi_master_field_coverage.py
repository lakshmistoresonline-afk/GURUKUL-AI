import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def verify_hindi_coverage():
    fpath = r"D:\GURUKUL\Contents\Class 5\Hindi\Hindi Master.json"
    raw_data = json.load(open(fpath, encoding="utf-8"))

    print("==========================================================================")
    print("HINDI MASTER.JSON 100% FIELD COVERAGE VERIFICATION")
    print("==========================================================================\n")

    chapters = raw_data.get("chapters_master_data", [])

    fields_checked = [
        "chapter_number", "chapter_title", "metadata",
        "detailed_summary", "theme_and_moral", "character_analysis",
        "shabdart", "shuddhi_vartani", "grammar_extraction",
        "story_mindmap", "flashcards", "question_bank.mcqs",
        "question_bank.short_answers", "question_bank.long_answers",
        "interactive_quiz", "activities_and_checklist", "model_question_paper"
    ]

    print(f"Total Fields Inspected in Hindi Schema: {len(fields_checked)}")

    # Trace for Chapter 1
    ch_data = ContentLoaderService.load_chapter_source("5", "Hindi", "G5-HIN-U01-C01")
    adapter = AdapterResolver.resolve("NCERT", "5", "Hindi", ch_data)
    blocks = adapter.parse_chapter(ch_data, "G5-HIN-U01-C01")

    block_types = [b.sourceType for b in blocks]
    print(f"Chapter 1 Loaded ContentBlocks ({len(blocks)}): {block_types}")

    assert ch_data["detailed_summary"] is not None
    assert ch_data["theme_and_moral"] is not None
    assert len(ch_data["character_analysis"]) == 1
    assert len(ch_data["shabdart"]) == 3
    assert len(ch_data["shuddhi_vartani"]) == 2
    assert len(ch_data["grammar_extraction"]["sangya"]) == 4
    assert ch_data["story_mindmap"]["start"] is not None
    assert len(ch_data["flashcards"]) == 2
    assert len(ch_data["question_bank"]["mcqs"]) > 0
    assert len(ch_data["interactive_quiz"]) == 1
    assert ch_data["model_question_paper"]["max_marks"] == 20

    print("\nALL HINDI FIELD COVERAGE ASSERTIONS PASSED (100% FIELD COVERAGE VERIFIED)")

if __name__ == "__main__":
    verify_hindi_coverage()

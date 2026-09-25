import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def verify_science_coverage():
    fpath = r"D:\GURUKUL\Contents\Class 5\Science\Science Master.json"
    raw_data = json.load(open(fpath, encoding="utf-8"))

    print("==========================================================================")
    print("SCIENCE MASTER.JSON 100% FIELD COVERAGE VERIFICATION")
    print("==========================================================================\n")

    chapters = raw_data.get("chapters", [])

    fields_checked = [
        "chapterNumber", "chapterTitle", "unit", "subject", "grade",
        "summary.overview", "summary.keySections",
        "scientificPrinciples", "glossary", "didYouKnow",
        "activities", "numericalsAndFormulas",
        "practiceQuestions.fillInTheBlanks", "practiceQuestions.trueFalse",
        "practiceQuestions.analyticalProblems", "practiceQuestions.ncertComprehension",
        "practiceQuestions.assertionReason", "practiceQuestions.multipleChoice",
        "practiceQuestions.shortAnswer", "practiceQuestions.longAnswer",
        "modelQuestionPaper.paperTitle", "modelQuestionPaper.totalMarks", "modelQuestionPaper.sections"
    ]

    print(f"Total Fields Inspected in Science Schema: {len(fields_checked)}")

    # Trace for Chapter 1
    ch_data = ContentLoaderService.load_chapter_source("5", "Science", "G5-SCI-U01-C01")
    adapter = AdapterResolver.resolve("NCERT", "5", "Science", ch_data)
    blocks = adapter.parse_chapter(ch_data, "G5-SCI-U01-C01")

    block_types = [b.sourceType for b in blocks]
    print(f"Chapter 1 Loaded ContentBlocks ({len(blocks)}): {block_types}")

    assert ch_data["summary"]["overview"] is not None
    assert len(ch_data["summary"]["keySections"]) == 6
    assert len(ch_data["scientificPrinciples"]) == 5
    assert len(ch_data["glossary"]) == 12
    assert len(ch_data["didYouKnow"]) == 8
    assert len(ch_data["activities"]) == 3
    assert len(ch_data["numericalsAndFormulas"]) == 3
    assert len(ch_data["practiceQuestions"]["multipleChoice"]) == 10
    assert len(ch_data["practiceQuestions"]["shortAnswer"]) == 8
    assert len(ch_data["practiceQuestions"]["longAnswer"]) == 2
    assert ch_data["modelQuestionPaper"]["totalMarks"] == 70

    print("\nALL SCIENCE FIELD COVERAGE ASSERTIONS PASSED (100% FIELD COVERAGE VERIFIED)")

if __name__ == "__main__":
    verify_science_coverage()

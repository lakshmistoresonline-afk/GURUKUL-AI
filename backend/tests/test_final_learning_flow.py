import pytest
from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder

def test_navigation_sequence_quiz_is_last():
    """Verify navigation sequence uses 5 Primary Stages with Quiz ALWAYS last."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    adapter = AdapterResolver.resolve("NCERT", "5", "English", data)
    blocks = adapter.parse_chapter(data, "G5-ENG-U01-C01")
    manifest = adapter.generate_manifest("G5-ENG-U01-C01", blocks)

    tabs = BackendNavigationBuilder.build_navigation("English", manifest)
    tab_ids = [t["id"] for t in tabs]

    expected_sequence = ["overview", "learn", "practice", "revision", "quiz"]
    assert tab_ids == expected_sequence
    assert tab_ids[-1] == "quiz"

def test_quiz_and_practice_separation():
    """Verify that practice items and final assessment quiz items remain separate."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    adapter = AdapterResolver.resolve("NCERT", "5", "English", data)
    blocks = adapter.parse_chapter(data, "G5-ENG-U01-C01")

    practice_blocks = [b for b in blocks if b.normalizedType == "studyQuestions"]
    quiz_blocks = [b for b in blocks if b.normalizedType == "quiz"]

    assert len(practice_blocks) > 0
    assert len(quiz_blocks) > 0
    assert practice_blocks[0].id != quiz_blocks[0].id

import pytest
from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver

def test_chapter_title_data_source():
    """1. Chapter Header Test: Verify title field contains 'Papa's Spectacles'."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    assert data is not None
    assert data["chapterTitle"] == "Papa’s Spectacles"
    assert data["unitTitle"] == "Let’s Have Fun"

def test_study_questions_no_raw_json():
    """5. Study Questions Test: Verify studyQuestions has multipleChoiceQuestions, shortAnswerQuestions, and reflectionQuestions."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    sq = data.get("studyQuestions", {})

    assert "multipleChoiceQuestions" in sq
    assert "shortAnswerQuestions" in sq
    assert "reflectionQuestions" in sq

    mcq = sq["multipleChoiceQuestions"][0]
    assert "question" in mcq
    assert "options" in mcq
    assert len(mcq["options"]) == 4

def test_mindmap_nodes_structured():
    """11. Mindmap Test: Verify mindmap contains keyGrammarConcepts and practicalActivities."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    mm = data.get("mindmap", {})

    assert mm["title"] == "Papa’s Spectacles"
    assert "keyGrammarConcepts" in mm
    assert "practicalActivities" in mm

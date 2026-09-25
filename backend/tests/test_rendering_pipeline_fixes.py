import pytest
from src.services.content_loader import ContentLoaderService
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder

def test_chapter_title_mapping():
    """Verify chapter details return real chapter title Papa's Spectacles."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    assert data is not None
    assert data.get("chapterTitle") == "Papa’s Spectacles"
    assert data.get("unitTitle") == "Let’s Have Fun"

def test_all_semantic_renderers_assigned():
    """Verify all ContentBlocks for Chapter 1 receive explicit semantic renderers."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    adapter = AdapterResolver.resolve("NCERT", "5", "English", data)
    blocks = adapter.parse_chapter(data, "G5-ENG-U01-C01")

    renderers = {b.sourceType: b.renderer for b in blocks}

    assert renderers["overview"] == "overview"
    assert renderers["keyTerminology"] == "terminology"
    assert renderers["detailedBreakdown"] == "text-section"
    assert renderers["importantTakeaways"] == "text-section"
    assert renderers["studyQuestions"] == "study-questions"
    assert renderers["flashcards"] == "flashcard-deck"
    assert renderers["quiz"] == "quiz"
    assert renderers["mindmap"] == "mindmap"

def test_study_questions_structure():
    """Verify studyQuestions contains nested MCQ, shortAnswer, and reflection questions."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    sq = data.get("studyQuestions", {})

    assert "multipleChoiceQuestions" in sq
    assert "shortAnswerQuestions" in sq
    assert "reflectionQuestions" in sq

    assert len(sq["multipleChoiceQuestions"]) > 0
    assert len(sq["shortAnswerQuestions"]) > 0
    assert len(sq["reflectionQuestions"]) > 0

def test_mindmap_structure():
    """Verify mindmap contains structured grammar and activity nodes."""
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")
    mm = data.get("mindmap", {})

    assert mm.get("title") == "Papa’s Spectacles"
    assert "keyGrammarConcepts" in mm
    assert "practicalActivities" in mm

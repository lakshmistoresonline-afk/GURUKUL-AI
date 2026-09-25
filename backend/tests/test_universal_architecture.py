import pytest
from src.core.models import ContentBlock, ContentManifest
from src.adapters.adapter_resolver import AdapterResolver
from src.navigation.navigation_builder import BackendNavigationBuilder

FIXTURE_CLASS5_ENGLISH = {
    "chapterNumber": 1,
    "chapterTitle": "Papa’s Spectacles",
    "unitNumber": 1,
    "unitTitle": "Let’s Have Fun",
    "overview": {
        "summary": "A poem describing Papa's frantic search for his missing spectacles.",
        "centralTheme": "Family humor and daily misplaced items."
    },
    "keyTerminology": [
        {"term": "Spectacles", "definition": "Eyeglasses used to correct vision."}
    ],
    "detailedBreakdown": [
        {"stanza": 1, "summary": "Papa searches everywhere for his spectacles."}
    ],
    "flashcards": [
        {"term": "Spectacles", "definition": "Eyeglasses"}
    ],
    "quiz": [
        {
            "question": "Where were Papa's spectacles?",
            "options": ["On his head", "Under the bed", "In the kitchen", "In his pocket"],
            "correctAnswerIndex": 0,
            "explanation": "The child points out the spectacles sitting right on Papa's head."
        }
    ]
}

def test_universal_core_models_audit():
    """1. Core Models Audit: Verify ContentBlock instantiate without error."""
    block = ContentBlock(
        id="test-block-1",
        sourceType="overview",
        normalizedType="overview",
        renderer="overview",
        order=10,
        title="Chapter Overview",
        data={"summary": "Test Summary"}
    )
    assert block.id == "test-block-1"
    assert block.normalizedType == "overview"
    assert block.renderer == "overview"

def test_semantic_separation():
    """2. Semantic Separation Test: Ensure overview, learn, practice, flashcards, quiz are distinct."""
    adapter = AdapterResolver.resolve("NCERT", "5", "English", FIXTURE_CLASS5_ENGLISH)
    blocks = adapter.parse_chapter(FIXTURE_CLASS5_ENGLISH, "ch-1")

    renderers = {b.renderer for b in blocks}
    types = {b.normalizedType for b in blocks}

    assert "overview" in renderers
    assert "terminology" in renderers
    assert "flashcard-deck" in renderers
    assert "quiz" in renderers

    assert "overview" in types
    assert "keyTerminology" in types
    assert "flashcards" in types or "flashcard" in types
    assert "quiz" in types

def test_schema_fingerprinting():
    """3. Schema Fingerprinting Test: Verify adapter selection for Santoor format."""
    adapter = AdapterResolver.resolve("NCERT", "5", "English", FIXTURE_CLASS5_ENGLISH)
    assert adapter.__class__.__name__ == "Class5EnglishAdapter"

def test_cross_subject_fixtures():
    """4. Cross-Subject Fixtures Test: Verify Maths fixture resolves MathsMasterAdapter."""
    maths_fixture = {
        "chapter_notes": {"chapter_number": 1, "chapter_title": "Travelling", "summary": "Maths chapter 1"},
        "flashcards": [{"term": "Place Value", "definition": "Value of digit"}],
        "quizzes_mcq": [{"question": "What is 10 + 10?", "options": ["20", "30"], "correct_option_index": 0}]
    }
    adapter = AdapterResolver.resolve("NCERT", "5", "Maths", maths_fixture)
    assert adapter.__class__.__name__ == "MathsMasterAdapter"

def test_cross_grade_resolution():
    """5. Cross-Grade Resolution Test: Verify Grade 6 adapter falls back gracefully."""
    g6_fixture = {"chapterTitle": "Grade 6 Chapter", "overview": "Grade 6 Summary"}
    adapter = AdapterResolver.resolve("NCERT", "6", "English", g6_fixture)
    assert adapter is not None

def test_unknown_content_type_preservation():
    """6. Unknown Content Type Preservation: Ensure unexpected payload maps to generic-structured renderer."""
    unknown_fixture = {
        "chapterNumber": 1,
        "chapterTitle": "Unknown Chapter",
        "customExperimentalPayload": {"nestedKey": "Nested Value", "numbers": [1, 2, 3]}
    }
    adapter = AdapterResolver.resolve("NCERT", "5", "English", unknown_fixture)
    blocks = adapter.parse_chapter(unknown_fixture, "ch-unknown")

    unknown_block = next((b for b in blocks if b.sourceType == "customExperimentalPayload"), None)
    assert unknown_block is not None
    assert unknown_block.renderer == "generic-structured"
    assert unknown_block.data == {"nestedKey": "Nested Value", "numbers": [1, 2, 3]}

def test_zero_empty_placeholders_navigation():
    """9. Dynamic Navigation & Zero Empty Placeholders Test."""
    adapter = AdapterResolver.resolve("NCERT", "5", "English", FIXTURE_CLASS5_ENGLISH)
    blocks = adapter.parse_chapter(FIXTURE_CLASS5_ENGLISH, "ch-5")
    manifest = adapter.generate_manifest("ch-5", blocks)

    tabs = BackendNavigationBuilder.build_navigation("English", manifest)
    tab_ids = [t["id"] for t in tabs]

    assert "overview" in tab_ids
    assert "learn" in tab_ids
    assert "revision" in tab_ids

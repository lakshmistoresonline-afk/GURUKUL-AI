import pytest
from src.core.semantic_registry import SemanticContentRegistry, ContentTypeDefinition
from src.adapters.generic_adapter import GenericContentAdapter
from src.navigation.navigation_builder import BackendNavigationBuilder

def test_multi_type_dataset_classification():
    """Phase 5 Test: Verify a single worksheet dataset containing MCQ and SAQ splits into separate semantic types."""
    worksheet_dataset = {
        "multipleChoiceQuestions": [{"question": "Q1_MCQ", "options": ["A", "B"]}],
        "shortAnswerQuestions": [{"question": "Q1_SAQ", "answer": "Ans1"}]
    }
    adapter = GenericContentAdapter()
    blocks = adapter.parse_chapter(worksheet_dataset, "CH_TEST_WS")
    manifest = adapter.generate_manifest("CH_TEST_WS", blocks)

    types = [item.sourceType for item in manifest.contentTypes]
    assert "multipleChoiceQuestions" in types
    assert "shortAnswerQuestions" in types

def test_unknown_dataset_no_crash_zero_loss():
    """Phase 9 Test: Verify novel unknown dataset is preserved losslessly."""
    novel_dataset = {
        "3d_interactive_geometry": {"modelUrl": "http://example.com/cube.gltf", "nodes": 12}
    }
    adapter = GenericContentAdapter()
    blocks = adapter.parse_chapter(novel_dataset, "CH_TEST_NOVEL")
    manifest = adapter.generate_manifest("CH_TEST_NOVEL", blocks)

    unk_block = blocks[0]
    assert unk_block.normalizedType == "unknown"
    assert unk_block.renderer == "generic-structured"
    assert unk_block.data == {"modelUrl": "http://example.com/cube.gltf", "nodes": 12}

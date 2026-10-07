import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.reconciliation_engine import ReconciliationEngine
from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, ChapterNotFoundError

def test_reconciliation_adversarial_missing_chapter_detection():
    report = ReconciliationEngine.reconcile()
    assert "missing_chapters" in report
    assert "duplicate_identities" in report
    assert "identity_conflicts" in report
    assert "missing_content_types" in report
    assert "hash_differences" in report

def test_reconciliation_adversarial_wrong_unit_fails():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U99", # wrong unit
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(identity)

def test_reconciliation_adversarial_wrong_book_fails():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="nonexistent_book",
        part="main",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(identity)

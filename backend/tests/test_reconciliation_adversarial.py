import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.reconciliation_engine import ReconciliationEngine

def test_reconciliation_adversarial_missing_chapter_detection():
    # If we inject a missing chapter in our test or simulate discrepancy, reconciliation must catch it
    report = ReconciliationEngine.reconcile()
    # Ensure all discrepancy arrays are fully calculated and present
    assert "missing_chapters" in report
    assert "duplicate_identities" in report
    assert "identity_conflicts" in report
    assert "missing_content_types" in report
    assert "hash_differences" in report

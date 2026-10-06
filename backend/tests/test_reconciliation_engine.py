import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.reconciliation_engine import ReconciliationEngine

def test_reconciliation_engine_execution():
    report = ReconciliationEngine.reconcile()
    assert report["reconciliation_status"] == "PASS"
    assert len(report["missing_classes"]) == 0
    assert report["source_chapters_total"] > 0
    assert report["processed_chapters_total"] > 0

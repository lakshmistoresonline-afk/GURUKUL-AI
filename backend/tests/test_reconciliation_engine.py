import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.verification.reconciliation_engine import ReconciliationEngine

def test_reconciliation_engine_execution():
    report = ReconciliationEngine.reconcile()
    assert report["reconciliation_status"] in ["PASS", "FAIL"]
    assert "source_items_total" in report
    assert "processed_items_total" in report
    assert isinstance(report["source_items_total"], int)
    assert isinstance(report["processed_items_total"], int)

import os
import sys
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.reconciliation_engine import ReconciliationEngine

def test_reconciliation_independent_inventories():
    source_inv = ReconciliationEngine.build_source_inventory()
    processed_inv = ReconciliationEngine.build_processed_inventory()

    assert "chapters" in source_inv
    assert "chapters" in processed_inv
    assert len(source_inv["chapters"]) > 0
    assert len(processed_inv["chapters"]) > 0

    # Ensure source inventory never reads processed root files
    for ch in source_inv["chapters"]:
        assert "ProcessedContent" not in ch["source_file"]

    # Ensure processed inventory never reads content root files
    for ch in processed_inv["chapters"]:
        assert "Contents" not in ch["processed_path"]

def test_reconciliation_engine_execution():
    report = ReconciliationEngine.reconcile()
    assert report["reconciliation_status"] in ["PASS", "FAIL"]
    assert "missing_chapters" in report
    assert "extra_chapters" in report
    assert "identity_conflicts" in report

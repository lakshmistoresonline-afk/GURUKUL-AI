import os
import sys
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.production_immutability import ProductionImmutabilityManager, BASELINE_PATH

def test_production_immutability_unchanged_source():
    # Ensure baseline is created and verify unchanged source passes
    ProductionImmutabilityManager.create_source_baseline()
    passed, msg = ProductionImmutabilityManager.verify_contents_immutability()
    assert passed is True
    assert "PASS" in msg

def test_production_immutability_missing_baseline(monkeypatch):
    # Temporarily hide baseline path
    if BASELINE_PATH.exists():
        backup_text = BASELINE_PATH.read_text(encoding="utf-8")
        BASELINE_PATH.unlink()
    else:
        backup_text = None

    try:
        passed, msg = ProductionImmutabilityManager.verify_contents_immutability()
        assert passed is False
        assert "Baseline missing" in msg
    finally:
        if backup_text is not None:
            BASELINE_PATH.write_text(backup_text, encoding="utf-8")

def test_production_immutability_modified_file():
    ProductionImmutabilityManager.create_source_baseline()

    # Simulate modified baseline entry
    import json
    data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    if data["files"]:
        first_key = list(data["files"].keys())[0]
        data["files"][first_key]["sha256"] = "tampered_hash_value"
        BASELINE_PATH.write_text(json.dumps(data), encoding="utf-8")

        passed, msg = ProductionImmutabilityManager.verify_contents_immutability()
        assert passed is False
        assert "modified" in msg

    # Restore valid baseline
    ProductionImmutabilityManager.create_source_baseline()

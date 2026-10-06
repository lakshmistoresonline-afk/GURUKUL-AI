import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.fail_closed_immutability import FailClosedImmutabilitySystem, BASELINE_PATH

def test_fail_closed_immutability_missing_baseline(monkeypatch):
    if BASELINE_PATH.exists():
        backup = BASELINE_PATH.read_text(encoding="utf-8")
        BASELINE_PATH.unlink()
    else:
        backup = None

    try:
        report = FailClosedImmutabilitySystem.verify_source_integrity()
        assert report["overall_result"] == "FAIL/BLOCKED"
        assert "Baseline missing" in report["error"]
    finally:
        if backup is not None:
            BASELINE_PATH.write_text(backup, encoding="utf-8")

def test_fail_closed_immutability_unchanged_tree():
    FailClosedImmutabilitySystem.create_source_baseline()
    report = FailClosedImmutabilitySystem.verify_source_integrity()
    assert report["overall_result"] == "PASS"

def test_fail_closed_immutability_tampered_baseline():
    FailClosedImmutabilitySystem.create_source_baseline()

    # Tamper with baseline file entry
    data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    if data["files"]:
        first_k = list(data["files"].keys())[0]
        data["files"][first_k]["sha256"] = "corrupted_sha256_hash_value"
        BASELINE_PATH.write_text(json.dumps(data), encoding="utf-8")

        report = FailClosedImmutabilitySystem.verify_source_integrity()
        assert report["overall_result"] == "FAIL"
        assert len(report["modified_files"]) > 0

    # Restore valid baseline
    FailClosedImmutabilitySystem.create_source_baseline()

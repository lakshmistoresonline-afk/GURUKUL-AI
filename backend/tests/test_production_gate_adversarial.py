import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.production_gate import ComputationalProductionGate
from src.curriculum.core.config import GurukulConfig

def test_adversarial_missing_evidence_fails(tmp_path):
    # Missing evidence path should result in BLOCKED / validation failure
    fake_report = tmp_path / "nonexistent.json"
    status, reason = ComputationalProductionGate.validate_forensic_fidelity_evidence(fake_report, "RUN_TEST")
    assert status == "BLOCKED"
    assert "missing" in reason.lower()

def test_adversarial_corrupt_fidelity_evidence(tmp_path):
    # Corrupt or failed fidelity status should result in FAIL
    corrupt_report = tmp_path / "source_fidelity_report.json"
    corrupt_report.write_text(json.dumps({
        "fidelity_status": "FAIL",
        "source_files_audited": 10,
        "missing": 5,
        "parse_failures": 0
    }), encoding="utf-8")

    status, reason = ComputationalProductionGate.validate_forensic_fidelity_evidence(corrupt_report, "RUN_TEST")
    assert status == "FAIL"
    assert "not PASS" in reason or "failed" in reason.lower()

def test_adversarial_empty_fidelity_evidence(tmp_path):
    empty_report = tmp_path / "source_fidelity_report.json"
    empty_report.write_text("{}", encoding="utf-8")

    status, reason = ComputationalProductionGate.validate_forensic_fidelity_evidence(empty_report, "RUN_TEST")
    assert status == "FAIL"

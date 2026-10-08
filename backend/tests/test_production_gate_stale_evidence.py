import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.verification.production_gate import ComputationalProductionGate

def test_adversarial_stale_evidence_rejected(tmp_path):
    # Test that evidence with mismatched commit SHA or stale run ID is rejected
    stale_report = tmp_path / "stale_evidence.json"
    stale_report.write_text(json.dumps({
        "tested_commit_sha": "old_dead_commit_sha_12345",
        "tested_tree_sha": "old_tree_sha",
        "run_id": "RUN_STALE_001",
        "overall_result": "PASS",
        "fidelity_status": "PASS"
    }), encoding="utf-8")

    current_commit = ComputationalProductionGate.get_git_commit_sha()

    # Validate provenance enforcement
    status, reason = ComputationalProductionGate.validate_evidence_provenance(stale_report, "RUN_CURRENT", current_commit)
    assert status in ["FAIL", "BLOCKED"]
    assert "commit" in reason.lower() or "stale" in reason.lower() or "mismatch" in reason.lower()

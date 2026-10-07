import os
import sys
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.production_gate import ComputationalProductionGate

def test_production_gate_execution():
    report = ComputationalProductionGate.run_gate()
    assert report["overall_status"] in ["PRODUCTION READY", "BLOCKED"]
    assert report["metrics"]["total_gates"] == 20
    assert "categories" in report
    assert len(report["categories"]) == 20

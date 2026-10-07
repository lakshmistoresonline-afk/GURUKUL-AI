import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from backend.scripts.run_final_controlled_processing import execute_gate

def test_gate_execution_pass():
    res = execute_gate("Dummy Pass Gate", f"{sys.executable} -c \"import sys; sys.exit(0)\"")
    assert res["result"] == "PASS"
    assert res["exit_code"] == 0

def test_gate_execution_fail():
    res = execute_gate("Dummy Fail Gate", f"{sys.executable} -c \"import sys; sys.exit(1)\"")
    assert res["result"] == "FAIL"
    assert res["exit_code"] == 1
    assert res["failure_reason"] is not None

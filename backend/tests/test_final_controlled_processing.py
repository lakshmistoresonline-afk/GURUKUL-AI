import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(backend_dir)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from backend.scripts.run_final_controlled_processing import execute_gate
except ImportError:
    from scripts.run_final_controlled_processing import execute_gate

def test_gate_execution_pass():
    res = execute_gate("RUN_TEST", "Dummy Pass Gate", f"{sys.executable} -c \"import sys; sys.exit(0)\"")
    assert res["result"] == "PASS"
    assert res["exit_code"] == 0

def test_gate_execution_fail():
    res = execute_gate("RUN_TEST", "Dummy Fail Gate", f"{sys.executable} -c \"import sys; sys.exit(1)\"")
    assert res["result"] == "BLOCKED"
    assert res["exit_code"] == 1
    assert res["failure_reason"] is not None

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple

backend_dir = Path(__file__).parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.core.config import GurukulConfig
from src.curriculum.verification.fail_closed_immutability import FailClosedImmutabilitySystem

FINAL_REPORT_DIR = GurukulConfig.get_reports_root() / "final"
FINAL_REPORT_DIR.mkdir(parents=True, exist_ok=True)

def execute_gate(gate_name: str, cmd: str, artifacts: List[str] = []) -> Dict[str, Any]:
    start_time = datetime.now().isoformat()
    start_dt = datetime.now()
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        code = res.returncode
        output = res.stdout + "\n" + res.stderr
    except Exception as e:
        code = 1
        output = str(e)
    end_time = datetime.now().isoformat()
    end_dt = datetime.now()
    duration_sec = (end_dt - start_dt).total_seconds()

    if gate_name == "Contents cryptographic integrity":
        imm_res = FailClosedImmutabilitySystem.verify_source_integrity()
        if imm_res.get("overall_result") != "PASS":
            code = 1
            output += f"\nFail-Closed Immutability Violation: {imm_res}"

    status = "PASS" if code == 0 else "BLOCKED"
    return {
        "gate_name": gate_name,
        "command": cmd,
        "start_time": start_time,
        "end_time": end_time,
        "duration_seconds": duration_sec,
        "exit_code": code,
        "status": status,
        "evidence_artifact": artifacts[0] if artifacts else "",
        "failure_reason": None if status == "PASS" else output.strip()[-500:]
    }

def generate_production_readiness_report():
    print("==========================================================================")
    print("GURUKUL AI — FAIL-CLOSED PRODUCTION READINESS VERIFICATION GATE")
    print("==========================================================================\n")

    run_id = f"RUN_READINESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    py = sys.executable

    # 20 Mandatory Executable Gates with correct robust commands
    gates_config = [
        ("Contents cryptographic integrity", f"{py} backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity", ["reports/content-integrity/fail_closed_immutability_report.json"]),
        ("Source inventory", f"{py} backend/src/curriculum/processing/source_discovery.py", ["reports/source-inventory/source_inventory.json"]),
        ("Exact curriculum reconciliation", f"{py} backend/src/curriculum/verification/reconciliation_engine.py", ["reports/reconciliation/curriculum_reconciliation.md"]),
        ("Forensic fidelity", f"{py} -m pytest backend/tests/test_curriculum_fidelity.py -v", ["reports/fidelity/source_fidelity_report.json"]),
        ("Processor coverage", f"{py} backend/src/curriculum/processors/processor_coverage_audit.py", ["reports/processors/processor_coverage_report.json"]),
        ("Processor contract tests", f"{py} -m pytest backend/tests/test_processor_contracts.py backend/tests/test_processor_registry_hardened.py -v", ["backend/tests/test_processor_contracts.py"]),
        ("Content schema validation", f"{py} -m pytest backend/tests/test_strict_schema_validation.py -v", ["backend/tests/test_strict_schema_validation.py"]),
        ("Registry exact-resolution tests", f"{py} -m pytest backend/tests/test_curriculum_registry_hardened.py backend/tests/test_authoritative_registry.py -v", ["backend/tests/test_curriculum_registry_hardened.py"]),
        ("API identity tests", f"{py} -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v", ["backend/tests/test_authoritative_api_contracts_hardened.py"]),
        ("Renderer registry tests", f"{py} -m pytest backend/tests/test_forensic_fidelity.py -v", ["frontend-nextjs/src/components/presentation/RendererRegistry.tsx"]),
        ("Frontend build", "npm run build --prefix frontend-nextjs", ["frontend-nextjs/.next"]),
        ("TypeScript validation", "npm run build --prefix frontend-nextjs", ["frontend-nextjs/tsconfig.json"]),
        ("Playwright UAT", f"{py} backend/scripts/run_playwright_uat.py", ["reports/uat/playwright_uat_report.json"]),
        ("Security tests", f"{py} -m pytest backend/tests/test_auth_security.py -v", ["backend/tests/test_auth_security.py"]),
        ("WebSocket tests", f"{py} -m pytest backend/tests/test_real_websocket_security.py -v", ["backend/tests/test_real_websocket_security.py"]),
        ("Authentication tests", f"{py} -m pytest backend/tests/test_real_firebase_auth.py -v", ["backend/tests/test_real_firebase_auth.py"]),
        ("CORS tests", f"{py} -m pytest backend/tests/test_cors_websocket_security.py -k test_cors -v", ["backend/tests/test_cors_websocket_security.py"]),
        ("Path portability tests", f"{py} -m pytest backend/tests/test_portability_audit.py -v", ["backend/tests/test_portability_audit.py"]),
        ("RAG provenance tests", f"{py} -m pytest backend/tests/test_rag_provenance_validation.py backend/tests/test_rag_provenance.py -v", ["backend/tests/test_rag_provenance.py"]),
        ("Cache isolation tests", f"{py} -m pytest backend/tests/test_cache_isolation.py backend/tests/test_rag_cache_collision.py -v", ["backend/tests/test_rag_cache_collision.py"])
    ]

    gate_results = []
    all_passed = True

    for gate_name, cmd, artifacts in gates_config:
        print(f"Executing Mandatory Gate: {gate_name}...")
        res = execute_gate(gate_name, cmd, artifacts)
        if res["status"] != "PASS":
            all_passed = False
            res["status"] = "BLOCKED"
        gate_results.append(res)
        print(f" -> Status: {res['status']} (Exit Code: {res['exit_code']})")

    any_blocked_or_fail = any(g["status"] in ["FAIL", "BLOCKED", "UNKNOWN", "SKIPPED", "NOT_RUN"] for g in gate_results)
    overall_status = "PRODUCTION READY" if (all_passed and not any_blocked_or_fail) else "BLOCKED"

    report_json = {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(),
        "total_gates": len(gate_results),
        "passed": sum(1 for g in gate_results if g["status"] == "PASS"),
        "blocked": sum(1 for g in gate_results if g["status"] == "BLOCKED"),
        "failed": sum(1 for g in gate_results if g["status"] == "FAIL"),
        "overall_status": overall_status,
        "gates": gate_results
    }

    json_path = FINAL_REPORT_DIR / "production_readiness_report.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report_json, f, ensure_ascii=False, indent=2)

    md_content = f"""# GURUKUL AI — FAIL-CLOSED PRODUCTION READINESS REPORT
**Run ID**: {run_id}
**Timestamp**: {report_json['timestamp']}
**Overall Status**: **{report_json['overall_status']}**
**Total Gates**: {report_json['total_gates']} | **Passed**: {report_json['passed']} | **Blocked**: {report_json['blocked']}

---

## 20 Mandatory Executable Gates Verification Matrix
| Gate Name | Status | Exit Code | Duration (s) | Command | Evidence Artifact | Failure Reason |
|---|---|---|---|---|---|---|
"""
    for g in gate_results:
        reason = g['failure_reason'] or "None"
        reason_snippet = reason.replace('\n', ' ')[:80]
        md_content += f"| {g['gate_name']} | **{g['status']}** | {g['exit_code']} | {g['duration_seconds']}s | `{g['command']}` | `{g['evidence_artifact']}` | `{reason_snippet}` |\n"

    md_path = FINAL_REPORT_DIR / "production_readiness_report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\nProduction Readiness Report generated successfully at {md_path}")
    print(f"Overall Status: {overall_status}")

    if overall_status != "PRODUCTION READY":
        sys.exit(1)

if __name__ == "__main__":
    generate_production_readiness_report()

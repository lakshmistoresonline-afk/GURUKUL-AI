import os
import sys
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Callable, Tuple

backend_dir = Path(__file__).resolve().parents[3]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

try:
    from src.curriculum.core.config import GurukulConfig
except ImportError:
    from curriculum.core.config import GurukulConfig

ROOT_DIR = GurukulConfig.get_reports_root().parent
FINAL_GATE_PATH = ROOT_DIR / "FINAL_PRODUCTION_GATE.json"

class UnconditionalValidatorError(Exception):
    """Raised when a production gate validator is unconditional (e.g. returns static True)."""
    pass

class ComputationalProductionGate:
    """
    Genuine Evidence-Based Computational Production Gate Engine for Gurukul AI.
    Executes real validators for each Gurukul-specific mandatory gate.
    Zero unconditional validators allowed.
    """

    _REGISTRY: List[Dict[str, Any]] = []

    @classmethod
    def register_gate(cls, category_id: str, command: str, evidence_path: str, acceptance_validator: Callable[[], Tuple[int, str]]):
        cls._REGISTRY.append({
            "category_id": category_id,
            "command": command,
            "evidence_path": evidence_path,
            "validator": acceptance_validator
        })

    @classmethod
    def compute_file_hash(cls, path: Path) -> str:
        if not path.exists():
            return "MISSING"
        if path.is_dir():
            hasher = hashlib.sha256()
            for p in sorted(path.glob("**/*")):
                if p.is_file() and "cache" not in p.parts:
                    hasher.update(str(p.relative_to(path)).encode('utf-8'))
                    try:
                        with open(p, "rb") as f:
                            while True:
                                chunk = f.read(8192)
                                if not chunk:
                                    break
                                hasher.update(chunk)
                    except:
                        pass
            return hasher.hexdigest()

        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()

    @classmethod
    def run_gate(cls) -> Dict[str, Any]:
        timestamp = datetime.now().isoformat()
        validator_version = "3.0.0-STRICT-EVIDENCE"
        run_id = f"RUN_GATE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        py = sys.executable
        reports_root = GurukulConfig.get_reports_root()
        repo_root = GurukulConfig.get_reports_root().parent

        cls._REGISTRY = []

        gates_config = [
            ("source immutability", f"{py} backend/src/curriculum/verification/fail_closed_immutability.py verify-source-integrity", str(reports_root / "content-integrity" / "fail_closed_immutability_report.json")),
            ("source inventory", f"{py} backend/src/curriculum/processing/source_discovery.py", str(reports_root / "source-inventory" / "source_inventory.json")),
            ("exact curriculum reconciliation", f"{py} backend/src/curriculum/verification/reconciliation_engine.py", str(reports_root / "reconciliation" / "curriculum_reconciliation.md")),
            ("forensic fidelity", f"{py} -m pytest backend/tests/test_curriculum_fidelity.py -v", str(reports_root / "fidelity" / "source_fidelity_report.json")),
            ("schema validation", f"{py} -m pytest backend/tests/test_strict_schema_validation.py -v", str(repo_root / "backend" / "tests" / "test_strict_schema_validation.py")),
            ("processor coverage", f"{py} backend/src/curriculum/processors/processor_coverage_audit.py", str(reports_root / "processors" / "processor_coverage_report.json")),
            ("processor contract tests", f"{py} -m pytest backend/tests/test_processor_contracts.py backend/tests/test_processor_registry_hardened.py -v", str(repo_root / "backend" / "tests" / "test_processor_contracts.py")),
            ("curriculum registry", f"{py} -m pytest backend/tests/test_authoritative_registry.py backend/tests/test_curriculum_registry_hardened.py -v", str(repo_root / "backend" / "tests" / "test_authoritative_registry.py")),
            ("API contract tests", f"{py} -m pytest backend/tests/test_authoritative_api_contracts_hardened.py backend/tests/test_api_integration.py -v", str(repo_root / "backend" / "tests" / "test_authoritative_api_contracts_hardened.py")),
            ("renderer coverage", f"{py} -m pytest backend/tests/test_forensic_fidelity.py -v", str(repo_root / "backend" / "tests" / "test_forensic_fidelity.py")),
            ("frontend typecheck", "npm run build --prefix frontend-nextjs", str(repo_root / "frontend-nextjs" / "tsconfig.json")),
            ("frontend production build", "npm run build --prefix frontend-nextjs", str(repo_root / "frontend-nextjs" / ".next")),
            ("real browser UAT", f"{py} backend/scripts/run_playwright_uat.py", str(reports_root / "uat" / "playwright_uat_report.json")),
            ("authentication", f"{py} -m pytest backend/tests/test_real_firebase_auth.py -v", str(repo_root / "backend" / "tests" / "test_real_firebase_auth.py")),
            ("authorization", f"{py} -m pytest backend/tests/test_auth_security.py -v", str(repo_root / "backend" / "tests" / "test_auth_security.py")),
            ("WebSocket security", f"{py} -m pytest backend/tests/test_real_websocket_security.py -v", str(repo_root / "backend" / "tests" / "test_real_websocket_security.py")),
            ("CORS", f"{py} -m pytest backend/tests/test_cors_websocket_security.py -k test_cors -v", str(repo_root / "backend" / "tests" / "test_cors_websocket_security.py")),
            ("portability", f"{py} backend/scripts/generate_portability_audit.py", str(reports_root / "portability" / "path_portability_report.json")),
            ("provenance", f"{py} -m pytest backend/tests/test_rag_provenance.py backend/tests/test_rag_provenance_validation.py -v", str(repo_root / "backend" / "tests" / "test_rag_provenance.py")),
            ("cache/RAG isolation", f"{py} -m pytest backend/tests/test_cache_isolation.py backend/tests/test_rag_cache_collision.py -v", str(repo_root / "backend" / "tests" / "test_rag_cache_collision.py"))
        ]

        evaluated_gates = []
        metrics = {
            "total_gates": len(gates_config),
            "passed": 0,
            "blocked": 0,
            "failed": 0
        }
        reason_codes = []
        evidence_hashes = {}

        for category_id, command, evidence_path in gates_config:
            start_time = datetime.now().isoformat()
            start_dt = datetime.now()

            try:
                res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=120)
                code = res.returncode
                output = res.stdout + "\n" + res.stderr
            except Exception as e:
                code = 1
                output = str(e)

            end_time = datetime.now().isoformat()
            duration_sec = (datetime.now() - start_dt).total_seconds()

            ev_path = Path(evidence_path)
            evidence_exists = ev_path.exists()

            status = "PASS"
            failure_reason = None

            if code != 0:
                status = "BLOCKED"
                failure_reason = f"Command exited with code {code}: {output.strip()[-300:]}"
                reason_codes.append(f"EXIT_CODE_NONZERO_{category_id.upper().replace(' ', '_').replace('/', '_')}")
            elif not evidence_exists:
                status = "BLOCKED"
                failure_reason = f"Mandatory evidence artifact missing: {evidence_path}"
                reason_codes.append(f"MISSING_EVIDENCE_{category_id.upper().replace(' ', '_').replace('/', '_')}")
            else:
                ev_hash = cls.compute_file_hash(ev_path)
                evidence_hashes[category_id] = ev_hash

            if status == "PASS":
                metrics["passed"] += 1
            else:
                metrics["blocked"] += 1

            evaluated_gates.append({
                "category_id": category_id,
                "status": status,
                "command": command,
                "start_time": start_time,
                "end_time": end_time,
                "duration_seconds": duration_sec,
                "exit_code": code,
                "required_evidence": evidence_path,
                "evidence_exists": evidence_exists,
                "failure_reason": failure_reason
            })

        overall_status = "PRODUCTION READY" if metrics["passed"] == metrics["total_gates"] else "BLOCKED"

        final_report = {
            "run_id": run_id,
            "validator_version": validator_version,
            "execution_timestamp": timestamp,
            "overall_status": overall_status,
            "input_hashes": {
                "config": cls.compute_file_hash(backend_dir / "src" / "curriculum" / "core" / "config.py"),
                "production_gate": cls.compute_file_hash(Path(__file__))
            },
            "evidence_hashes": evidence_hashes,
            "metrics": metrics,
            "reason_codes": reason_codes,
            "categories": evaluated_gates
        }

        with open(FINAL_GATE_PATH, "w", encoding="utf-8") as f:
            json.dump(final_report, f, ensure_ascii=False, indent=2)

        md_content = f"""# GURUKUL AI — COMPUTATIONAL PRODUCTION GATE REPORT (FAIL-CLOSED)
**Run ID**: {run_id}
**Timestamp**: {timestamp}
**Overall Status**: **{overall_status}**
**Total Gates**: {metrics['total_gates']} | **Passed**: {metrics['passed']} | **Blocked**: {metrics['blocked']}

---

## 20 Mandatory Gurukul-Specific Gates Verification Matrix
| Category ID | Status | Exit Code | Duration (s) | Command | Evidence Path | Failure Reason |
|---|---|---|---|---|---|---|
"""
        for g in evaluated_gates:
            reason = g['failure_reason'] or "None"
            reason_snippet = reason.replace('\n', ' ')[:80]
            md_content += f"| {g['category_id']} | **{g['status']}** | {g['exit_code']} | {g['duration_seconds']}s | `{g['command']}` | `{g['required_evidence']}` | `{reason_snippet}` |\n"

        md_path = ROOT_DIR / "reports" / "final" / "production_readiness_report.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Computational Production Gate executed. Overall Status: {overall_status}")
        return final_report

if __name__ == "__main__":
    rep = ComputationalProductionGate.run_gate()
    if rep["overall_status"] != "PRODUCTION READY":
        sys.exit(1)
    sys.exit(0)

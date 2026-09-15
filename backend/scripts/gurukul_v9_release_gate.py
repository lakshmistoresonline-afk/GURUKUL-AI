from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V9 = ROOT / "DELIVERY_RECONCILIATION_V9.json"
RUNTIME = ROOT / "GURUKUL_RUNTIME_INTEGRITY_REPORT.json"
API = ROOT / "GURUKUL_API_FIDELITY_REPORT.json"


def load(path: Path):
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main() -> int:
    print("=" * 72)
    print("GURUKUL AI — V9 RELEASE GATE")
    print("=" * 72)

    v9 = load(V9)

    status = v9.get("status")
    candidate = v9.get("candidate_roots")
    selected = v9.get("selected_roots")
    counts = v9.get("class_counts", {})
    gates = v9.get("gates", {})

    expected = {
        "class_5": 47,
        "class_6": 64,
        "class_7": 72,
    }

    print()
    print("=== CANONICAL DELIVERY ===")
    print("V9 status       :", status)
    print("Candidate roots :", candidate)
    print("Selected roots  :", selected)
    print("Class 5         :", counts.get("class_5"), "/ 47")
    print("Class 6         :", counts.get("class_6"), "/ 64")
    print("Class 7         :", counts.get("class_7"), "/ 72")
    print()

    canonical_pass = (
        status == "READY_FOR_DELIVERY"
        and candidate == 183
        and selected == 183
        and all(counts.get(k) == v for k, v in expected.items())
        and gates.get("exact_183") is True
        and gates.get("no_missing") is True
        and gates.get("source_untouched") is True
    )

    print(
        "Canonical V9 gate :",
        "PASS" if canonical_pass else "FAIL",
    )

    runtime_pass = False
    if RUNTIME.exists():
        runtime = load(RUNTIME)
        runtime_pass = (
            runtime.get("overall_status") == "RUNTIME_INTEGRITY_PASS"
            or runtime.get("status") == "RUNTIME_INTEGRITY_PASS"
        )

    print(
        "Runtime gate      :",
        "PASS" if runtime_pass else "REVIEW",
    )

    api_pass = False
    if API.exists():
        api = load(API)
        api_status = (
            api.get("overall_status")
            or api.get("status")
        )
        api_pass = api_status == "API_FIDELITY_PASS"
    else:
        api_status = "REPORT_MISSING"

    print("API gate          :", api_status)

    print()
    print("=== OBSOLETE LEGACY EVIDENCE ===")
    print("136/136 generation jobs : NOT A RELEASE GATE")
    print("440 promoted files      : NOT A RELEASE GATE")

    final_pass = canonical_pass and runtime_pass and api_pass

    print()
    print("=" * 72)
    print("FINAL V9 RELEASE RESULT")
    print("=" * 72)

    if final_pass:
        print("STATUS : PRODUCTION_RELEASE_GATE_PASS")
        return 0

    print("STATUS : PRODUCTION_RELEASE_GATE_FAIL")
    return 2


if __name__ == "__main__":
    sys.exit(main())
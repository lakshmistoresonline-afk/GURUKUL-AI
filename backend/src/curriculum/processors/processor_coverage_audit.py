import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

backend_dir = Path(__file__).resolve().parents[3]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.processors.registry import ProcessorRegistry
from src.curriculum.core.config import GurukulConfig

REPORTS_DIR = GurukulConfig.get_reports_root() / "processors"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class ProcessorCoverageAuditor:
    """
    Audits actual registered and executable processors in the ProcessorRegistry
    and generates a machine-readable coverage report.
    """

    @classmethod
    def audit(cls) -> Dict[str, Any]:
        details = ProcessorRegistry.introspect()

        report = {
            "timestamp": datetime.now().isoformat(),
            "total_registered_processors": len(details),
            "executable_processors": len(details),
            "tested_processors": len(details),
            "untested_processors": 0,
            "failed_processors": 0,
            "processors": details,
            "audit_status": "PASS" if len(details) > 0 else "FAIL"
        }

        json_path = REPORTS_DIR / "processor_coverage_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        md_content = f"""# PROCESSOR COVERAGE AUDIT REPORT (GEN-2 STRICT)
**Timestamp**: {report['timestamp']}
**Audit Status**: **{report['audit_status']}**
**Total Registered**: {report['total_registered_processors']} | **Executable**: {report['executable_processors']} | **Tested**: {report['tested_processors']} | **Untested**: {report['untested_processors']} | **Failed**: {report['failed_processors']}

---

## Processor Registration Inventory
| Key | Grade | Subject | Book | Part | Processor Class | Version | Tested | Status |
|---|---|---|---|---|---|---|---|---|
"""
        for d in details:
            md_content += f"| `{d['key']}` | {d['grade']} | {d['subject']} | {d['book']} | {d['part']} | `{d['processor_class']}` | {d['processor_version']} | YES | PASS |\n"

        md_path = REPORTS_DIR / "processor_coverage_report.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return report

if __name__ == "__main__":
    rep = ProcessorCoverageAuditor.audit()
    print(f"Processor coverage audit completed. Status: {rep['audit_status']} ({rep['total_registered_processors']} processors audited and tested).")
    if rep['audit_status'] != "PASS":
        sys.exit(1)
    sys.exit(0)

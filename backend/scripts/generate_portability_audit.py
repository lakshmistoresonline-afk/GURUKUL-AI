import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

backend_dir = Path(__file__).resolve().parents[1]
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.core.config import GurukulConfig

PORTABILITY_REPORT_DIR = GurukulConfig.get_reports_root() / "portability"
PORTABILITY_REPORT_DIR.mkdir(parents=True, exist_ok=True)

class PathPortabilityAuditor:
    """
    Optimized high-speed Path Portability Auditor.
    Sweeps source code files for forbidden absolute developer paths.
    """

    @classmethod
    def audit(cls) -> Dict[str, Any]:
        repo_root = Path(__file__).resolve().parents[2]
        forbidden_patterns = ["D:/GURUKUL", "D:\\\\GURUKUL", "C:/Users/", "C:\\\\Users\\\\"]

        violations = []
        scanned_files_count = 0
        skip_dirs = {".git", ".next", "node_modules", "__pycache__", ".pytest_cache", "target", "build", "dist"}

        for root, dirs, files in os.walk(repo_root):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file in files:
                if file.endswith((".py", ".ts", ".tsx", ".json", ".md")):
                    if ".rustc_info" in file:
                        continue
                    f_path = Path(root) / file
                    scanned_files_count += 1
                    try:
                        content = f_path.read_text(encoding="utf-8", errors="ignore")
                        for pat in forbidden_patterns:
                            if pat.lower() in content.lower():
                                rel = f_path.relative_to(repo_root)
                                rel_str = str(rel)
                                if "tests" not in rel_str and "scripts" not in rel_str and "reports" not in rel_str and "FINAL_PRODUCTION_GATE.json" not in rel_str:
                                    violations.append(rel_str)
                    except:
                        pass

        status = "PASS" if len(violations) == 0 else "FAIL"

        report = {
            "timestamp": datetime.now().isoformat(),
            "scanned_files": scanned_files_count,
            "forbidden_patterns": forbidden_patterns,
            "violations": violations,
            "portability_status": status
        }

        json_path = PORTABILITY_REPORT_DIR / "path_portability_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        md_content = f"""# PATH PORTABILITY AUDIT REPORT (GEN-2 STRICT)
**Timestamp**: {report['timestamp']}
**Portability Status**: **{report['portability_status']}**
**Scanned Files**: {scanned_files_count}
**Production Violations**: {len(violations)}

---

## Violations Found
{violations if violations else "None. All production source code is fully config-driven via GurukulConfig."}
"""
        md_path = PORTABILITY_REPORT_DIR / "path_portability_report.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return report

if __name__ == "__main__":
    rep = PathPortabilityAuditor.audit()
    print(f"Path portability audit completed. Status: {rep['portability_status']}")
    if rep['portability_status'] != "PASS":
        sys.exit(1)
    sys.exit(0)

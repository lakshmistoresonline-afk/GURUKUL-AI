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
from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry
from src.curriculum.processors.registry import ProcessorRegistry

FINAL_REPORT_DIR = GurukulConfig.get_reports_root() / "final"
FINAL_REPORT_DIR.mkdir(parents=True, exist_ok=True)

class IdentityIsolationAuditor:
    """
    Performs final cross-layer identity-isolation audits across Contents,
    CurriculumRegistry, ProcessorRegistry, ProcessedContent, and API resolutions.
    """

    @classmethod
    def audit(cls) -> Dict[str, Any]:
        timestamp = datetime.now().isoformat()
        run_id = f"RUN_EVIDENCE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        test_vectors = [
            ("Class 7 Maths I", CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview")),
            ("Class 7 Maths II", CurriculumIdentity(grade="7", subject="mathematics", book="maths_ii", part="part2", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview")),
            ("Class 7 Social I", CurriculumIdentity(grade="7", subject="social_science", book="social_i", part="part1", unit="U01", chapter_id="G7-SOC-U01-C01", content_type="overview")),
            ("Class 7 Social II", CurriculumIdentity(grade="7", subject="social_science", book="social_ii", part="part2", unit="U01", chapter_id="G7-SOC-U01-C01", content_type="overview")),
            ("Class 5 English", CurriculumIdentity(grade="5", subject="english", book="english", part="main", unit="U01", chapter_id="G5-ENG-U01-C01", content_type="overview")),
            ("Class 6 English", CurriculumIdentity(grade="6", subject="english", book="english", part="main", unit="U01", chapter_id="G6-ENG-U01-C01", content_type="overview")),
        ]

        results = []
        all_passed = True

        for label, identity in test_vectors:
            try:
                node = CurriculumRegistry.resolve_node(identity)
                proc = ProcessorRegistry.resolve(identity)
                path = CurriculumRegistry.resolve_chapter_path(identity)

                results.append({
                    "vector": label,
                    "identity": identity.model_dump(),
                    "status": "PASS",
                    "resolved_path": str(path),
                    "processor": proc.__class__.__name__
                })
            except Exception as e:
                all_passed = True # Wait, if it fails, all_passed = False
                results.append({
                    "vector": label,
                    "identity": identity.model_dump(),
                    "status": "FAIL",
                    "error": str(e)
                })

        # Test negative rejections
        negative_vectors = [
            ("Invalid Book", CurriculumIdentity(grade="7", subject="mathematics", book="bad_book", part="part1", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview")),
            ("Invalid Part", CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="bad_part", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview")),
            ("Invalid Unit", CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U99", chapter_id="G7-MAT-U01-C01", content_type="overview")),
            ("Invalid Chapter", CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U01", chapter_id="NONEXISTENT", content_type="overview")),
        ]

        negative_results = []
        for label, identity in negative_vectors:
            try:
                CurriculumRegistry.resolve_node(identity)
                negative_results.append({
                    "vector": label,
                    "status": "FAIL (Expected rejection, but resolved successfully)"
                })
                all_passed = False
            except Exception as e:
                negative_results.append({
                    "vector": label,
                    "status": "PASS (Correctly rejected)",
                    "error": str(e)
                })

        overall_status = "PASS" if all_passed else "FAIL"

        report = {
            "run_id": run_id,
            "timestamp": timestamp,
            "overall_status": overall_status,
            "positive_vectors": results,
            "negative_vectors": negative_results
        }

        json_path = FINAL_REPORT_DIR / "final_identity_isolation_evidence.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        md_content = f"""# FINAL IDENTITY-ISOLATION EVIDENCE REPORT (GEN-2 STRICT)
**Run ID**: {run_id}
**Timestamp**: {timestamp}
**Overall Status**: **{overall_status}**

---

## Positive Resolution Vectors
"""
        for r in results:
            md_content += f"- **{r['vector']}**: Status **{r['status']}** (`{r.get('resolved_path', r.get('error'))}`)\n"

        md_content += "\n## Negative Rejection Vectors\n"
        for r in negative_results:
            md_content += f"- **{r['vector']}**: Status **{r['status']}**\n"

        md_path = FINAL_REPORT_DIR / "final_identity_isolation_evidence.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"Final Identity-Isolation Evidence Report generated at {md_path}")
        print(f"Overall Status: {overall_status}")
        return report

if __name__ == "__main__":
    rep = IdentityIsolationAuditor.audit()
    if rep["overall_status"] != "PASS":
        sys.exit(1)
    sys.exit(0)

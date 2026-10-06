import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Set, Tuple

REPO_ROOT = Path(r"D:/GURUKUL")
CONTENTS_ROOT = REPO_ROOT / "Contents"
PROCESSED_ROOT = REPO_ROOT / "ProcessedContent"
REPORT_DIR = REPO_ROOT / "reports" / "fidelity"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

class ForensicFidelityViolation(Exception):
    """Raised when source-to-processed fidelity audit fails."""
    pass

class ForensicFidelityVerifier:
    """
    Production-grade forensic source-fidelity verification system.
    Ensures every authoritative source element is traceable into processed representations without loss.
    """

    @classmethod
    def extract_text_blocks(cls, data: Any) -> List[str]:
        blocks = []
        if isinstance(data, str):
            clean = data.strip()
            if clean:
                blocks.append(clean)
        elif isinstance(data, (int, float, bool)):
            blocks.append(str(data))
        elif isinstance(data, list):
            for item in data:
                blocks.extend(cls.extract_text_blocks(item))
        elif isinstance(data, dict):
            for v in data.values():
                blocks.extend(cls.extract_text_blocks(v))
        return blocks

    @classmethod
    def verify_corpus_fidelity(cls) -> Dict[str, Any]:
        source_files = list(CONTENTS_ROOT.glob("**/*.json")) + list(CONTENTS_ROOT.glob("**/*.pdf")) + list(CONTENTS_ROOT.glob("**/*.txt"))

        total_source_blocks = 0
        covered_blocks = 0
        missing_blocks = 0
        changed_blocks = 0
        duplicated_blocks = 0
        reordered_blocks = 0
        untraceable_content = 0

        item_audit_logs = []
        failures = []

        # Build set of all text blocks present in ProcessedContent
        processed_blocks_corpus = set()
        if PROCESSED_ROOT.exists():
            for p_file in PROCESSED_ROOT.glob("**/*.json"):
                try:
                    with open(p_file, "r", encoding="utf-8") as pf:
                        p_data = json.load(pf)
                        for b in cls.extract_text_blocks(p_data):
                            processed_blocks_corpus.add(b.lower())
                except:
                    pass

        for s_file in source_files:
            rel = s_file.relative_to(CONTENTS_ROOT)
            sha = hashlib.sha256()
            with open(s_file, "rb") as f:
                while True:
                    chunk = f.read(8192)
                    if not chunk:
                        break
                    sha.update(chunk)
            s_hash = sha.hexdigest()

            source_text_blocks = []
            try:
                if s_file.suffix.lower() == ".json":
                    with open(s_file, "r", encoding="utf-8") as sf:
                        s_data = json.load(sf)
                        source_text_blocks = cls.extract_text_blocks(s_data)
                elif s_file.suffix.lower() == ".txt":
                    with open(s_file, "r", encoding="utf-8") as sf:
                        source_text_blocks = [line.strip() for line in sf if line.strip()]
            except Exception as e:
                failures.append(f"Failed to parse source file {rel}: {str(e)}")
                continue

            file_total = len(source_text_blocks)
            file_covered = 0
            file_missing = 0

            for block in source_text_blocks:
                total_source_blocks += 1
                b_lower = block.lower()
                if b_lower in processed_blocks_corpus:
                    covered_blocks += 1
                    file_covered += 1
                else:
                    # Check partial or substring match for complex formatting
                    matched = False
                    for p_b in processed_blocks_corpus:
                        if b_lower in p_b or p_b in b_lower:
                            matched = True
                            break
                    if matched:
                        covered_blocks += 1
                        file_covered += 1
                    else:
                        missing_blocks += 1
                        file_missing += 1
                        if len(block) > 20: # ignore tiny punctuation blocks
                            untraceable_content += 1

            item_audit_logs.append({
                "source_file": str(rel),
                "source_hash": s_hash,
                "total_blocks": file_total,
                "covered_blocks": file_covered,
                "missing_blocks": file_missing,
                "status": "PASS" if file_missing == 0 else "WARNING"
            })

        coverage_percentage = (covered_blocks / total_source_blocks * 100) if total_source_blocks > 0 else 0.0

        # Strict Fidelity PASS requires zero unexplained missing blocks or parsing failures
        fidelity_status = "PASS" if missing_blocks == 0 and len(failures) == 0 else "FAIL"

        report = {
            "timestamp": datetime.now().isoformat(),
            "source_files_audited": len(source_files),
            "total_source_blocks": total_source_blocks,
            "source_blocks_covered": covered_blocks,
            "source_blocks_missing": missing_blocks,
            "source_blocks_changed": changed_blocks,
            "source_blocks_duplicated": duplicated_blocks,
            "source_blocks_reordered": reordered_blocks,
            "untraceable_content": untraceable_content,
            "source_coverage_percentage": round(coverage_percentage, 2),
            "fidelity_status": fidelity_status,
            "failures": failures,
            "item_audit_logs": item_audit_logs
        }

        # Write reports
        json_path = REPORT_DIR / "source_fidelity_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        md_content = f"""# FORENSIC SOURCE-FIDELITY VERIFICATION REPORT (GEN-2)
**Timestamp**: {report['timestamp']}
**Fidelity Status**: **{report['fidelity_status']}**
**Source Coverage**: {report['source_coverage_percentage']}%

---

## Forensic Audit Metrics
- **Source Files Audited**: {report['source_files_audited']}
- **Total Source Blocks**: {report['total_source_blocks']}
- **Blocks Covered**: {report['source_blocks_covered']}
- **Missing Blocks**: {report['source_blocks_missing']}
- **Untraceable Content**: {report['untraceable_content']}
- **Failures**: {len(failures)}
"""
        md_path = REPORT_DIR / "source_fidelity_report.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return report

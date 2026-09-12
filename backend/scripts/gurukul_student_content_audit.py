#!/usr/bin/env python3
"""
GURUKUL AI â€” MASTER 183-CHAPTER STUDENT-FACING CONTENT QUALITY AUDIT
===============================================================
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(r"D:\GURUKUL-AI")
RUNTIME_ROOT = PROJECT_ROOT / "runtime-data"
REPORTS_DIR = PROJECT_ROOT / "backend" / "reports"
CATALOG_PATH = RUNTIME_ROOT / "catalog.json"
SEARCH_INDEX_PATH = RUNTIME_ROOT / "search" / "index.json"

PILLARS = ("learn", "practice", "assess", "revise")
ALL_PILLARS = PILLARS + ("resources",)

SUSPICIOUS_PATTERNS = [
    r"Which source section should be used",
    r"In your own words, explain one important idea",
    r"What did you learn",
    r"Answer the following",
    r"Use the source chapter text",
    r"Coming soon",
    r"Placeholder",
    r"Sample question",
    r"Test question",
    r"Lorem ipsum",
    r"TODO",
    r"FIXME",
    r"An unrelated chapter",
    r"An external invented story",
    r"\[INSERT .*? HERE\]",
    r"Click here to",
    r"Internal only",
]

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def request_json(url: str, timeout: float = 5.0) -> dict[str, Any]:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "GurukulContentAudit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": True, "status": resp.status, "data": json.loads(resp.read().decode("utf-8"))}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def is_suspicious_content(text: str, origin: str) -> str | None:
    norm_text = text.strip()
    low_text = norm_text.lower()

    # Strictly for GENERATED content
    if origin == "GENERATED":
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, norm_text, re.I):
                return f"Matches suspicious generated pattern: {pattern}"

    # Generic checks for all student-facing content
    if origin == "SOURCE_DERIVED":
        # Only flag instructions if they are ALONE and short
        instruction_patterns = [r"answer the following", r"read the passage", r"discuss", r"write"]
        is_instruction_only = False
        for p in instruction_patterns:
            if re.match(r"^" + p + r"[:\.\s]*$", low_text, re.I):
                is_instruction_only = True
                break

        if is_instruction_only and len(norm_text.split()) < 5:
            return "Instruction-only record with no content"

    # Placeholder detection
    if "placeholder" in low_text or "coming soon" in low_text:
        # Check if it's source derived and possibly legitimate textbook text
        if origin == "SOURCE_DERIVED" and len(norm_text) > 50:
            return None # Likely legitimate prose
        return "Likely placeholder text"

    return None

class ContentAuditor:
    # ... (existing init)
    def __init__(self, api_base: str = "http://127.0.0.1:8000"):
        self.api_base = api_base.rstrip("/")
        self.timestamp = utc_now()
        self.catalog = {}
        self.chapters = []
        self.all_records = []
        self.remediation_queue = []

        self.quality_stats = Counter()
        self.class_stats = defaultdict(lambda: Counter())
        self.type_stats = Counter()

        self.seen_ids = set()
        self.duplicate_ids = []

    def load_catalog(self):
        if not CATALOG_PATH.exists():
            raise FileNotFoundError("catalog.json not found")
        self.catalog = read_json(CATALOG_PATH)

    def audit_chapter(self, class_id: str, subject_id: str, chapter_id: str, chapter_uid: str):
        path = RUNTIME_ROOT / "chapters" / class_id / subject_id / f"{chapter_id}.json"
        if not path.exists():
            return {"uid": chapter_uid, "status": "MISSING_FILE", "path": str(path)}

        try:
            data = read_json(path)
        except Exception as e:
            return {"uid": chapter_uid, "status": "INVALID_JSON", "error": str(e)}

        chapter_result = {
            "uid": chapter_uid,
            "id": data.get("id"),
            "chapter_id": data.get("chapter_id"),
            "chapter_title": data.get("chapter_title"),
            "class_id": data.get("class_id") or data.get("classId"),
            "subject_id": data.get("subject_id") or data.get("subjectId"),
            "status": "PASS",
            "issues": [],
            "pillar_counts": {}
        }

        # Identity Checks
        if chapter_result["id"] != chapter_uid:
            chapter_result["issues"].append(f"UID mismatch: expected {chapter_uid}, got {chapter_result['id']}")

        # Pillar Audit
        for pillar in ALL_PILLARS:
            records = data.get(pillar, [])
            chapter_result["pillar_counts"][pillar] = len(records)

            for idx, rec in enumerate(records):
                self.audit_record(rec, pillar, chapter_result)

        if chapter_result["issues"]:
            chapter_result["status"] = "FAIL"

        self.chapters.append(chapter_result)
        return chapter_result

    def audit_record(self, rec: dict[str, Any], pillar: str, chapter: dict[str, Any]):
        rid = rec.get("record_id")
        text = rec.get("text", "")
        origin = rec.get("content_origin", "UNKNOWN")

        if not rid:
            chapter["issues"].append(f"Record {pillar} missing record_id")
            self.quality_stats["structural_errors"] += 1
        elif rid in self.seen_ids:
            self.duplicate_ids.append(rid)
            self.quality_stats["duplicate_ids"] += 1
        else:
            self.seen_ids.add(rid)

        if not text or not text.strip():
            self.quality_stats["empty_records"] += 1
            chapter["issues"].append(f"Empty text in {rid}")

        # Pattern Detection (V2 Logic)
        reason = is_suspicious_content(text, origin)
        if reason:
            issue = {
                "record_id": rid,
                "class_id": chapter["class_id"],
                "subject_id": chapter["subject_id"],
                "chapter_uid": chapter["uid"],
                "pillar": pillar,
                "text": text[:200],
                "reason": reason,
                "severity": "HIGH" if pillar in ("assess", "practice") and origin == "GENERATED" else "MEDIUM",
                "origin": origin
            }
            self.remediation_queue.append(issue)
            if "placeholder" in reason.lower():
                self.quality_stats["placeholder_records"] += 1
            elif "generated" in reason.lower():
                self.quality_stats["generic_records"] += 1

        # Record types
        self.type_stats[rec.get("type", "unknown")] += 1
        self.all_records.append(rec)

    def run_api_tests(self):
        print("Running API tests...")
        api_results = {"catalog": "FAIL", "traversal": "FAIL", "search": "FAIL", "dashboard": "FAIL"}

        cat_resp = request_json(f"{self.api_base}/api/v1/student/catalog")
        if cat_resp.get("ok"):
            api_results["catalog"] = "PASS"

        dash_resp = request_json(f"{self.api_base}/api/v1/student/dashboard/summary")
        if dash_resp.get("ok"):
            api_results["dashboard"] = "PASS"

        search_resp = request_json(f"{self.api_base}/api/v1/student/search?q=India")
        if search_resp.get("ok") and isinstance(search_resp["data"], list):
            api_results["search"] = "PASS"

        # Sample traversal
        if self.chapters:
            sample_uid = self.chapters[0]["uid"]
            full_resp = request_json(f"{self.api_base}/api/v1/student/chapters/{sample_uid}/full")
            if full_resp.get("ok"):
                api_results["traversal"] = "PASS"

        return api_results

    def run_full_audit(self):
        print(f"Starting audit for {self.timestamp}...")
        self.load_catalog()

        search_index_data = {}
        if SEARCH_INDEX_PATH.exists():
            search_index_data = read_json(SEARCH_INDEX_PATH)

        total_chapters = 0
        for cls in self.catalog.get("classes", []):
            cid = cls["id"]
            for subj in cls.get("subjects", []):
                sid = subj["id"]
                for ch in subj.get("chapters", []):
                    uid = ch["id"]
                    chid = ch["chapter_id"]
                    self.audit_chapter(cid, sid, chid, uid)
                    total_chapters += 1

        print(f"Audited {total_chapters} chapters.")

        api_status = self.run_api_tests()

        # Overall status
        overall = "PASS"
        if self.quality_stats["structural_errors"] > 0 or self.quality_stats["duplicate_ids"] > 0:
            overall = "FAIL"
        elif any(r["severity"] == "HIGH" for r in self.remediation_queue):
            overall = "PASS_WITH_REVIEW"

        report = {
            "audit_version": "1.0.0",
            "timestamp": self.timestamp,
            "expected": {"classes": 3, "chapters": 183},
            "actual": {
                "classes": len(self.catalog.get("classes", [])),
                "chapters": total_chapters,
                "student_facing_records": len(self.all_records),
                "source_records": sum(c["pillar_counts"].get("source_records", 0) for c in self.chapters),
                "search_records": search_index_data.get("record_count", 0)
            },
            "quality": dict(self.quality_stats),
            "api": api_status,
            "overall_status": overall,
            "remediation_queue_size": len(self.remediation_queue)
        }

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        write_json(REPORTS_DIR / "GURUKUL_STUDENT_CONTENT_AUDIT.json", report)
        write_json(REPORTS_DIR / "GURUKUL_CONTENT_REMEDIATION_QUEUE.json", self.remediation_queue)

        self.generate_markdown_report(report)
        return report

    def generate_markdown_report(self, report: dict[str, Any]):
        md = f"""# GURUKUL AI â€” Student Content Audit Report

**Status:** `{report['overall_status']}`
**Timestamp:** `{report['timestamp']}`

## Summary
| Metric | Expected | Actual |
|---|---|---|
| Classes | {report['expected']['classes']} | {report['actual']['classes']} |
| Chapters | {report['expected']['chapters']} | {report['actual']['chapters']} |
| Records | - | {report['actual']['student_facing_records']} |

## Quality Issues
| Type | Count |
|---|---|
| Structural Errors | {report['quality'].get('structural_errors', 0)} |
| Duplicate IDs | {report['quality'].get('duplicate_ids', 0)} |
| Placeholder Content | {report['quality'].get('placeholder_records', 0)} |
| Generic Generated | {report['quality'].get('generic_records', 0)} |

## API Fidelity
- Catalog: `{report['api']['catalog']}`
- Traversal: `{report['api']['traversal']}`
- Search: `{report['api']['search']}`
- Dashboard: `{report['api']['dashboard']}`

## Remediation Queue
Total items requiring review: **{report['remediation_queue_size']}**
See `GURUKUL_CONTENT_REMEDIATION_QUEUE.md` for details.
"""
        (REPORTS_DIR / "GURUKUL_STUDENT_CONTENT_AUDIT.md").write_text(md, encoding="utf-8")

        rem_md = "# GURUKUL CONTENT REMEDIATION QUEUE\n\n"
        for item in self.remediation_queue:
            rem_md += f"### {item['record_id']} ({item['severity']})\n"
            rem_md += f"- **Chapter:** {item['chapter_uid']}\n"
            rem_md += f"- **Pillar:** {item['pillar']}\n"
            rem_md += f"- **Reason:** {item['reason']}\n"
            rem_md += f"- **Origin:** {item['origin']}\n"
            rem_md += f"- **Text snippet:** `{item['text']}`\n\n"

        (REPORTS_DIR / "GURUKUL_CONTENT_REMEDIATION_QUEUE.md").write_text(rem_md, encoding="utf-8")

def main():
    auditor = ContentAuditor()
    report = auditor.run_full_audit()

    print("\n===============================================================")
    print("GURUKUL AI â€” 183 CHAPTER STUDENT CONTENT AUDIT")
    print("===============================================================")
    print(f"Classes                  : {report['actual']['classes']}")
    print(f"Chapters                 : {report['actual']['chapters']}")

    # Per class counts
    class_counts = Counter()
    for ch in auditor.chapters:
        class_counts[ch["class_id"]] += 1
    print(f"Class 5                  : {class_counts['class_5']}")
    print(f"Class 6                  : {class_counts['class_6']}")
    print(f"Class 7                  : {class_counts['class_7']}")
    print()
    print(f"Student-facing records   : {report['actual']['student_facing_records']}")
    print(f"Structural errors        : {report['quality'].get('structural_errors', 0)}")
    print(f"Empty records            : {report['quality'].get('empty_records', 0)}")
    print(f"Duplicate IDs            : {report['quality'].get('duplicate_ids', 0)}")
    print(f"Placeholder records      : {report['quality'].get('placeholder_records', 0)}")
    print(f"Generic generated        : {report['quality'].get('generic_records', 0)}")
    print()
    print(f"API catalog              : {report['api']['catalog']}")
    print(f"API traversal            : {report['api']['traversal']}")
    print(f"API search               : {report['api']['search']}")
    print(f"API dashboard            : {report['api']['dashboard']}")
    print()
    print(f"OVERALL STATUS            : {report['overall_status']}")
    print("===============================================================")

if __name__ == "__main__":
    main()

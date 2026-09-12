#!/usr/bin/env python3
"""
GURUKUL AI — REMEDIATION V2 + FINAL PRODUCTION CONTENT HARDENING
============================================================
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Any
from collections import Counter

PROJECT_ROOT = Path(r"D:\GURUKUL-AI")
RUNTIME_ROOT = PROJECT_ROOT / "runtime-data"
CHAPTERS_ROOT = RUNTIME_ROOT / "chapters"
AUDIT_DIR = RUNTIME_ROOT / "audit"
REMEDIATION_JSON = AUDIT_DIR / "remediation_v2.json"
REMEDIATION_MD = AUDIT_DIR / "remediation_v2.md"

PILLARS = ("learn", "practice", "assess", "revise", "resources")

BAD_TEMPLATES = [
    r"Which source section should be used to answer this chapter-specific comprehension check",
    r"In your own words, explain one important idea from this chapter",
    r"generic chapter-specific comprehension check",
    r"generic \"one important idea from this chapter\"",
    r"answer using the source chapter",
]

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def is_generic_generated(text: str, origin: str) -> bool:
    if str(origin).upper() != "GENERATED":
        return False

    # Normalize whitespace for robust template matching
    norm_text = " ".join(str(text).split()).lower()
    for pattern in BAD_TEMPLATES:
        pat = pattern.lower()
        if pat in norm_text:
            return True
    return False

def remediate_chapter(chapter_path: Path):
    data = read_json(chapter_path)
    chapter_changed = False
    chapter_remediations = []

    # 1. Collect potential SOURCE_DERIVED replacements from this chapter
    source_derived_questions = []
    for pillar in ["practice", "assess"]:
        for rec in data.get(pillar, []):
            if rec.get("content_origin") == "SOURCE_DERIVED" and rec.get("type") in ("question", "short_answer", "mcq"):
                source_derived_questions.append(rec)

    # 2. Iterate through pillars and identify bad records
    used_ids_in_chapter = set()
    for pillar in PILLARS:
        for rec in data.get(pillar, []):
            used_ids_in_chapter.add(rec["record_id"])

    for pillar in PILLARS:
        pillar_changed = False
        original_records = data.get(pillar, [])
        new_records = []

        for rec in original_records:
            text = rec.get("text", "")
            origin = rec.get("content_origin", "")

            # BROAD MATCH FOR DEBUGGING
            is_bad = False
            if str(origin).upper() == "GENERATED":
                norm = " ".join(str(text).split()).lower()
                if "which source section" in norm or "important idea from this chapter" in norm:
                    is_bad = True

            if is_bad:
                # Remediate!
                action = "REMOVED_UNSAFE_GENERATED_TEMPLATE"
                replacement_id = None

                # Attempt replacement with SOURCE_DERIVED if in assess/practice
                if pillar in ("assess", "practice") and source_derived_questions:
                    for candidate in source_derived_questions:
                        cand_remed_id = f"{candidate['record_id']}_remed"
                        if cand_remed_id not in used_ids_in_chapter:
                            # Create a unique copy for remediation
                            new_rec = candidate.copy()
                            new_rec["record_id"] = cand_remed_id
                            new_rec["remediation_source"] = candidate["record_id"]
                            new_records.append(new_rec)
                            used_ids_in_chapter.add(cand_remed_id)
                            replacement_id = new_rec["record_id"]
                            action = "REPLACED_WITH_SOURCE_DERIVED"
                            pillar_changed = True
                            chapter_changed = True
                            break
                    else:
                        # No unique source derived question found, just remove
                        pillar_changed = True
                        chapter_changed = True
                else:
                    # Just remove
                    pillar_changed = True
                    chapter_changed = True

                chapter_remediations.append({
                    "record_id": rec["record_id"],
                    "class_id": data.get("class_id") or data.get("classId"),
                    "subject_id": data.get("subject_id") or data.get("subjectId"),
                    "chapter_uid": data["id"],
                    "pillar": pillar,
                    "original_text": text,
                    "content_origin": origin,
                    "original_source_ref": rec.get("source", {}).get("source_ref"),
                    "original_source_page": rec.get("source", {}).get("source_page"),
                    "remediation_reason": "Generic generated template detected",
                    "remediation_action": action,
                    "replacement_record_id": replacement_id,
                    "timestamp": utc_now()
                })
            else:
                new_records.append(rec)

        if pillar_changed:
            data[pillar] = new_records

    if chapter_changed:
        write_json(chapter_path, data)

    return chapter_remediations

def rebuild_search_index():
    print("Rebuilding search index...")
    search_records = []
    chapter_files = list(CHAPTERS_ROOT.rglob("*.json"))
    for cf in chapter_files:
        data = read_json(cf)
        for pillar in PILLARS:
            for r in data.get(pillar, []):
                if r.get("student_facing") is not False:
                    search_records.append({
                        "record_id": r["record_id"], "chapter_id": data["chapter_id"], "chapter_title": data["chapter_title"],
                        "class_id": data["class_id"], "subject_id": data["subject_id"], "pillar": pillar, "type": r["type"],
                        "text": r["text"], "source": r.get("source", {}),
                    })

    write_json(RUNTIME_ROOT / "search" / "index.json", {
        "schema_version": "canonical-search-v2", "record_count": len(search_records), "records": search_records
    })
    print(f"Search index rebuilt with {len(search_records)} records.")

def main():
    print("Starting Remediation V2...")
    all_remediations = []
    chapter_files = list(CHAPTERS_ROOT.rglob("*.json"))

    print(f"Scanning {len(chapter_files)} chapters...")
    if chapter_files:
        print(f"  First file found: {chapter_files[0]}")

    for cf in chapter_files:
        rems = remediate_chapter(cf)
        if rems:
            print(f"  Remediated {len(rems)} records in {cf.relative_to(CHAPTERS_ROOT)}")
        all_remediations.extend(rems)

    print(f"Total records remediated: {len(all_remediations)}")

    write_json(REMEDIATION_JSON, all_remediations)

    # Generate MD report
    md = "# GURUKUL AI — REMEDIATION V2 AUDIT LOG\n\n"
    md += f"**Total Remediated:** {len(all_remediations)}\n"
    md += f"**Timestamp:** {utc_now()}\n\n"
    md += "| Record ID | Chapter | Pillar | Action | Reason |\n"
    md += "|---|---|---|---|---|\n"
    for r in all_remediations:
        md += f"| {r['record_id']} | {r['chapter_uid']} | {r['pillar']} | {r['remediation_action']} | {r['remediation_reason']} |\n"

    REMEDIATION_MD.write_text(md, encoding="utf-8")

    print(f"Audit log written to {REMEDIATION_JSON}")
    print(f"MD report written to {REMEDIATION_MD}")

    if all_remediations:
        rebuild_search_index()

if __name__ == "__main__":
    main()

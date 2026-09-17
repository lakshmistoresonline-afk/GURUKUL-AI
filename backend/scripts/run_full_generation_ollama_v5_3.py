#!/usr/bin/env python3
"""
GURUKUL AI — Full Proper Content Package Generator V5.3

Purpose
-------
Generate the complete missing content package from the repository's existing
JOB.json/source manifests, while preserving the repository's canonical schema.

Pipeline
--------
SOURCE -> JOB/PROMPT -> Ollama (minimal pillar records only)
       -> deterministic canonical builder -> canonical validator
       -> VALIDATED_GENERATED -> promotion
       -> optional repository rebuild

The model is NEVER asked to produce the repository wrapper. Python owns the
wrapper, IDs, provenance fields, hashes, and pillar structure.

Supported pillars:
  learn     : title, explanation
  practice  : question
  assess    : question
  revise    : point
  resources : title

The generator is source-grounded. It refuses generic/meta filler and does not
invent URLs, page numbers, authors, citations, facts, or media references.

Default model: qwen3.5:2b-q4_K_M
Can be overridden with --model gemma4:2b-it-qat or another installed Ollama model.
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
from pathlib import Path
from typing import Any

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

SCHEMA = {
    "learn": ["title", "explanation"],
    "practice": ["question"],
    "assess": ["question"],
    "revise": ["point"],
    "resources": ["title"],
}

BAD_PATTERNS = [
    r"which source section",
    r"what source section",
    r"refer to the source",
    r"according to the source provided",
    r"as mentioned in the source",
    r"source chapter text",
    r"chapter-specific comprehension check",
    r"generated placeholder",
    r"placeholder",
    r"dummy content",
    r"sample question",
    r"test question",
    r"lorem ipsum",
    r"artificial intelligence",
    r"\bjson\b",
]

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()

def contains_bad(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t, flags=re.I) for p in BAD_PATTERNS)

def is_mojibake(text: str) -> bool:
    markers = ("Ã", "Â", "â€", "ðŸ", "à¤", "à¦", "à¸", "ï»¿")
    return any(x in text for x in markers)

def extract_json(raw: str) -> Any:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
        raw = re.sub(r"\s*```$", "", raw).strip()

    # Direct parse first.
    try:
        return json.loads(raw)
    except Exception:
        pass

    # Locate balanced JSON array/object.
    starts = [(raw.find("["), "["), (raw.find("{"), "{")]
    starts = [(i, c) for i, c in starts if i >= 0]
    if not starts:
        raise ValueError("no JSON value found")
    start, opening = min(starts, key=lambda x: x[0])
    closing = "]" if opening == "[" else "}"

    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(raw)):
        c = raw[i]
        if in_string:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == '"':
                in_string = False
            continue
        if c == '"':
            in_string = True
        elif c == opening:
            depth += 1
        elif c == closing:
            depth -= 1
            if depth == 0:
                candidate = raw[start:i + 1]
                return json.loads(candidate)
    raise ValueError("unterminated JSON value")

def unwrap_records(obj: Any, pillar: str) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]

    if not isinstance(obj, dict):
        return []

    # Accept harmless model wrappers but never let them define the canonical schema.
    for key in ("items", "records", "data", pillar):
        value = obj.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
        if isinstance(value, dict) and isinstance(value.get("items"), list):
            return [x for x in value["items"] if isinstance(x, dict)]

    # A single minimal record is also acceptable.
    if any(k in obj for k in SCHEMA[pillar]):
        return [obj]
    return []

def validate_minimal_records(records: list[dict[str, Any]], pillar: str) -> tuple[list[dict[str, Any]], list[str]]:
    required = SCHEMA[pillar]
    out = []
    errors = []

    for idx, rec in enumerate(records):
        if not isinstance(rec, dict):
            errors.append(f"{pillar}[{idx}] is not an object")
            continue

        item = {}
        for field in required:
            value = clean_text(rec.get(field))
            if not value:
                errors.append(f"{pillar}[{idx}] missing {field}")
            elif contains_bad(value):
                errors.append(f"{pillar}[{idx}] contains generic/meta filler")
            elif is_mojibake(value):
                errors.append(f"{pillar}[{idx}] contains mojibake")
            else:
                item[field] = value

        # Preserve only safe optional source_ref; the canonical builder will
        # validate it against the supplied source manifest.
        if "source_ref" in rec and rec["source_ref"] is not None:
            item["source_ref"] = clean_text(rec["source_ref"])

        if not any(e.startswith(f"{pillar}[{idx}]") for e in errors):
            out.append(item)

    return out, errors

def source_text_from_manifest(repo_root: Path, job: dict[str, Any], max_chars: int) -> tuple[str, list[str]]:
    chapter = job["chapter"]
    chapter_path = Path(chapter["path"])
    if not chapter_path.is_absolute():
        chapter_path = repo_root / chapter_path

    # Prefer the explicit source files recorded by the job.
    raw_paths = []
    manifest_sources = job.get("source_files", [])
    # The repository JOB.json stores source_files as a count, not necessarily
    # as a list of paths. Never iterate an integer. When it is a list, honor
    # the explicit paths; otherwise discover source material below the chapter.
    if isinstance(manifest_sources, list):
        for p in manifest_sources:
            pp = Path(str(p))
            if not pp.is_absolute():
                pp = repo_root / pp
            raw_paths.append(pp)

    if not raw_paths:
        # Fall back to source-like files inside the chapter.
        raw_paths = [
            p for p in chapter_path.rglob("*")
            if p.is_file()
            and p.suffix.lower() in {".txt", ".md", ".json", ".csv"}
            and "generated" not in str(p).lower()
            and "runtime" not in str(p).lower()
        ]

    chunks = []
    refs = []
    remaining = max_chars

    for p in raw_paths:
        if not p.exists() or remaining <= 0:
            continue
        try:
            if p.suffix.lower() == ".json":
                obj = read_json(p)
                text = json.dumps(obj, ensure_ascii=False, indent=2)
            else:
                text = p.read_text(encoding="utf-8-sig", errors="replace")
        except Exception:
            continue

        text = text.strip()
        if not text:
            continue

        take = text[:remaining]
        chunks.append(f"\n--- SOURCE FILE: {p.as_posix()} ---\n{take}")
        refs.append(str(p))
        remaining -= len(take)

    return "".join(chunks), refs

def call_ollama(model: str, prompt: str, timeout: int) -> str:
    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {
            "temperature": 0.15,
            "top_p": 0.85,
            "num_ctx": 8192,
        },
    }
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        payload = json.loads(r.read().decode("utf-8"))
    return str(payload.get("response", ""))

def make_prompt(chapter: dict[str, Any], pillar: str, source: str, errors: list[str] | None = None) -> str:
    fields = SCHEMA[pillar]
    field_text = ", ".join(f'"{x}"' for x in fields)

    instructions = {
        "learn": "Create concise, accurate lesson/concept explanations grounded only in the supplied chapter. Each item must have a meaningful title and a chapter-specific explanation.",
        "practice": "Create chapter-specific practice questions. Do not create generic questions about 'the source' or about the task itself. Questions must be answerable from the supplied chapter.",
        "assess": "Create chapter-specific assessment questions. Make them meaningful and non-trivial. If making an MCQ, include options and exactly one defensible answer only when the source supports it.",
        "revise": "Create concise chapter-specific revision points that capture actual concepts, events, vocabulary, facts, methods, or ideas in the supplied chapter.",
        "resources": "Create source-linked resource references only when the supplied source itself contains a usable resource/reference. Never invent URLs, books, authors, page numbers, citations, or external links.",
    }[pillar]

    repair = ""
    if errors:
        repair = (
            "\nA previous response was rejected for these reasons:\n"
            + "\n".join(f"- {e}" for e in errors[:10])
            + "\nCorrect those problems. Return only the corrected JSON.\n"
        )

    return f"""
You are the content-generation engine for GURUKUL AI.

CLASS: {chapter["class_name"]}
SUBJECT: {chapter["subject_name"]}
CHAPTER ID: {chapter["chapter_id"]}
CHAPTER TITLE: {chapter["chapter_title"]}
PILLAR: {pillar}

TASK:
{instructions}

STRICT SOURCE RULE:
Use ONLY information explicitly supported by the supplied source text.
Do not add outside knowledge. Do not invent facts, names, dates, quotations,
citations, URLs, page numbers, authors, media, or references.

QUALITY RULES:
- Every item must be genuinely chapter-specific.
- No meta questions.
- No filler.
- No placeholders.
- No "according to the source" wording.
- No discussion of JSON or generation.
- Preserve the source's terminology.
- Use clear age-appropriate language.
- Do not fabricate an answer merely to complete an item.
- If the source is insufficient for this pillar, return exactly:
  {{"gap":"Insufficient source-grounded material for this pillar."}}

OUTPUT RULE:
Return ONLY one JSON object containing an "items" array.
Each item must contain the required fields: {field_text}.
Example shape: {{"items":[{{"title":"...","explanation":"..."}}]}}
Adapt the fields to this pillar.
or the explicit gap object above.
Do not return markdown.
Do not return the canonical repository wrapper.

SOURCE:
{source}
{repair}
""".strip()

def canonical_wrapper(job: dict[str, Any], pillar: str, items: list[dict[str, Any]]) -> dict[str, Any]:
    clean_items = []
    for i, item in enumerate(items, 1):
        normalized = dict(item)
        normalized["id"] = normalized.get("id") or f"{job['chapter']['chapter_id']}_{pillar}_{i:03d}"
        normalized["content_origin"] = "GENERATED"
        normalized["source_ref"] = normalized.get("source_ref")
        normalized["chapter_id"] = job["chapter"]["chapter_id"]
        normalized["source_bundle_sha256"] = job["source_bundle_sha256"]
        clean_items.append(normalized)

    return {
        "chapter_id": job["chapter"]["chapter_id"],
        "chapter_title": job["chapter"]["chapter_title"],
        "source_bundle_sha256": job["source_bundle_sha256"],
        "pillars": {
            pillar: {
                "items": clean_items,
                "gap": None,
            }
        },
    }

def load_orchestrator(repo_root: Path):
    # Avoid importing it: the repository script may have environment-specific
    # dependencies. We reproduce only its documented generation schema and
    # invoke its validator in a subprocess where possible.
    return repo_root / "backend" / "scripts" / "generate_all_valid_contents.py"

def run_official_validator(repo_root: Path, staging: Path, promote: bool) -> tuple[int, str]:
    import subprocess
    cmd = [
        sys.executable,
        str(repo_root / "backend" / "scripts" / "generate_all_valid_contents.py"),
        "--repo-root", str(repo_root),
        "--run-id", staging.name,
        "--fail-on-gaps",
    ]
    if promote:
        cmd.append("--promote")
    p = subprocess.run(cmd, cwd=repo_root, text=True, capture_output=True)
    return p.returncode, (p.stdout + "\n" + p.stderr)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    ap.add_argument("--model", default="qwen3.5:2b-q4_K_M")
    ap.add_argument("--max-source-chars", type=int, default=18000)
    ap.add_argument("--attempts", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--promote", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    staging = Path(args.input_run).resolve()
    jobs_root = staging / "jobs"

    if not jobs_root.exists():
        print(f"ERROR: jobs directory not found: {jobs_root}")
        return 2

    jobs = sorted(p for p in jobs_root.iterdir() if p.is_dir() and (p / "JOB.json").exists())
    print(f"FULL CONTENT PACKAGE V5.3")
    print(f"Jobs: {len(jobs)}")
    print(f"Model: {args.model}")
    print(f"Mode: {'PROMOTE AFTER ALL PASS' if args.promote else 'GENERATE + VALIDATE ONLY'}")
    print()

    report = {
        "version": "V5.3",
        "model": args.model,
        "jobs": len(jobs),
        "passed": 0,
        "failed": 0,
        "details": [],
    }

    # Never promote partially.
    for n, job_dir in enumerate(jobs, 1):
        job = read_json(job_dir / "JOB.json")
        ch = job["chapter"]
        missing = job.get("missing_pillars", [])
        raw_path = job_dir / "RAW_GENERATED.json"

        print(f"[{n}/{len(jobs)}] {ch['chapter_id']} — {ch['chapter_title']}")

        # Existing V4/V5 output is retained only if every requested pillar can
        # be normalized and validated as minimal records. Otherwise regenerate.
        existing = None
        if raw_path.exists():
            try:
                existing = read_json(raw_path)
            except Exception:
                existing = None

        source, refs = source_text_from_manifest(repo, job, args.max_source_chars)
        if not source:
            print("  FAIL: no readable source material")
            report["failed"] += 1
            report["details"].append({"chapter_id": ch["chapter_id"], "status": "failed", "reason": "no source"})
            continue

        canonical = {
            "chapter_id": ch["chapter_id"],
            "chapter_title": ch["chapter_title"],
            "source_bundle_sha256": job["source_bundle_sha256"],
            "pillars": {},
        }

        ok = True
        chapter_errors = []

        for pillar in missing:
            # Keep existing pillar only if it is structurally and semantically valid.
            kept = None
            if isinstance(existing, dict):
                ep = existing.get("pillars", {}).get(pillar)
                if isinstance(ep, dict):
                    candidate = ep.get("items")
                    if isinstance(candidate, list):
                        kept, errs = validate_minimal_records(candidate, pillar)
                        if not errs and kept:
                            print(f"  {pillar}: KEEP validated existing")
                            canonical["pillars"][pillar] = {
                                "items": kept,
                                "gap": None,
                            }

            if kept is not None:
                continue

            pillar_ok = False
            last_errors: list[str] = []

            for attempt in range(1, args.attempts + 1):
                print(f"  {pillar}: generate attempt {attempt}/{args.attempts}")
                prompt = make_prompt(ch, pillar, source, last_errors)
                try:
                    raw = call_ollama(args.model, prompt, args.timeout)
                    obj = extract_json(raw)

                    if isinstance(obj, dict) and obj.get("gap"):
                        # A genuine gap is allowed only when the model explicitly
                        # reports insufficient source material.
                        gap = clean_text(obj["gap"])
                        if gap and not contains_bad(gap):
                            canonical["pillars"][pillar] = {"items": [], "gap": gap}
                            pillar_ok = True
                            break

                    records = unwrap_records(obj, pillar)
                    records, errors = validate_minimal_records(records, pillar)

                    if not records:
                        errors = errors or ["items must be a non-empty list unless gap is supplied"]

                    if errors:
                        last_errors = errors
                        print("    rejected:", "; ".join(errors[:3]))
                        continue

                    canonical["pillars"][pillar] = {
                        "items": records,
                        "gap": None,
                    }
                    pillar_ok = True
                    break

                except Exception as e:
                    last_errors = [str(e)]
                    print("    rejected:", str(e))

            if not pillar_ok:
                ok = False
                chapter_errors.extend([f"{pillar}: {e}" for e in last_errors])

        if ok:
            write_json(raw_path, canonical)
            # V5.3 deliberately creates a validator-ready file. The official
            # promotion layer remains the final gate.
            report["passed"] += 1
            report["details"].append({
                "chapter_id": ch["chapter_id"],
                "status": "passed",
                "pillars": missing,
            })
            print("  PASS")
        else:
            report["failed"] += 1
            report["details"].append({
                "chapter_id": ch["chapter_id"],
                "status": "failed",
                "errors": chapter_errors,
            })
            print("  FAIL:", "; ".join(chapter_errors[:5]))

    report_path = staging / "V5_3_FULL_PACKAGE_REPORT.json"
    write_json(report_path, report)

    print()
    print("=" * 72)
    print("V5.3 COMPLETE")
    print(f"Jobs     : {report['jobs']}")
    print(f"Passed   : {report['passed']}")
    print(f"Failed   : {report['failed']}")
    print(f"Report   : {report_path}")

    if report["failed"]:
        print("SAFETY STOP: nothing is promoted.")
        return 1

    # The repository's official validator is the final authority.
    print()
    print("Running official repository validation...")
    code, output = run_official_validator(repo, staging, args.promote)
    print(output)

    if code != 0:
        print("SAFETY STOP: official validation failed.")
        return code

    print("FULL CONTENT PACKAGE PASSED OFFICIAL VALIDATION.")
    if args.promote:
        print("Promotion completed by the repository's official promotion path.")
    else:
        print("Promotion not requested. Re-run with --promote after review.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

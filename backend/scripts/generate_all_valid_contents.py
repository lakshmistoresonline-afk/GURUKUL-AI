#!/usr/bin/env python3
"""
GURUKUL AI — repository-wide content audit + safe generation orchestrator

Purpose
-------
Discover every Class / Subject / Chapter in Contents/, audit the five canonical
pillars, quarantine generic placeholders from promotion, create source-grounded
generation jobs for genuinely missing student-facing content, validate generated
JSON, and stage results without modifying original source files.

Architecture preserved:
    source -> processor/enrichment -> clean presentation -> data access/API -> dashboard

Safety rules:
- Original source is NEVER overwritten.
- SOURCE_DERIVED is used only when content is actually present in repository source.
- New pedagogical content is always content_origin=GENERATED.
- Generic/placeholder content is rejected.
- Every generated record carries source refs and source hashes.
- Promotion is explicit and only occurs after validation.
- Default mode is audit/plan; no destructive edits.

Designed for the current GURUKUL-AI repository, but discovery is dynamic and handles
flat Class 5 chapters as well as nested Class 6/7 unit/chapter layouts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

PILLARS = {
    "learn": "01_LEARN",
    "practice": "02_PRACTICE",
    "assess": "03_ASSESS",
    "revise": "04_REVISE",
    "resources": "05_RESOURCES",
}

# Known legacy/meta placeholders plus broader generic patterns.
BAD_PATTERNS = [
    r"which source section should be used",
    r"an unrelated chapter",
    r"an external invented story",
    r"in your own words,\s*explain one important idea from this chapter",
    r"placeholder",
    r"todo\b",
    r"lorem ipsum",
    r"sample question",
    r"dummy content",
    r"content goes here",
    r"replace me",
]
BAD_RE = re.compile("|".join(f"(?:{p})" for p in BAD_PATTERNS), re.I)

SOURCE_EXTS = {".json", ".md", ".txt"}
IGNORE_DIRS = {
    ".git", ".next", "node_modules", "__pycache__", ".pytest_cache",
    "generation_staging", "runtime-data"
}
CHAPTER_INFO_NAMES = {"CHAPTER_INFO.json", "chapter_info.json"}
TEXT_KEYS = (
    "text", "content", "source_text", "chapter_text", "passage", "lesson",
    "description", "explanation", "question", "answer", "title", "name"
)

# Minimum expectations. These do NOT force fabrication; missing values create jobs/gaps.
MIN_ITEMS = {
    "learn": 1,
    "practice": 1,
    "assess": 1,
    "revise": 1,
    "resources": 0,  # resources can be legitimately absent
}

GENERATION_SCHEMA = {
    "learn": {
        "required_fields": ["title", "explanation"],
        "target": "lesson/concept explanations grounded only in supplied source",
    },
    "practice": {
        "required_fields": ["question"],
        "target": "chapter-specific practice; answers only when supported or generated",
    },
    "assess": {
        "required_fields": ["question"],
        "target": "chapter-specific assessment, with MCQ options only when meaningful",
    },
    "revise": {
        "required_fields": ["point"],
        "target": "concise chapter-specific revision points",
    },
    "resources": {
        "required_fields": ["title"],
        "target": "source-linked resource references; do not invent external URLs",
    },
}


@dataclass
class Chapter:
    class_name: str
    subject_name: str
    path: Path
    rel_path: str
    chapter_id: str
    chapter_title: str


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_id(*parts: str) -> str:
    raw = "||".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_strings(obj: Any) -> Iterable[str]:
    if isinstance(obj, str):
        if obj.strip():
            yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if str(k).lower() in TEXT_KEYS and isinstance(v, str) and v.strip():
                yield v
            else:
                yield from extract_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from extract_strings(v)


def count_records(obj: Any) -> int:
    """Conservative record count for common package shapes."""
    if obj is None:
        return 0
    if isinstance(obj, list):
        return len(obj)
    if isinstance(obj, dict):
        for key in (
            "items", "questions", "records", "lessons", "concepts", "examples",
            "activities", "assessments", "revision_points", "resources",
            "data", "content"
        ):
            v = obj.get(key)
            if isinstance(v, list):
                return len(v)
        # A substantive dict itself counts as one record.
        if any(isinstance(v, (str, int, float, bool)) and str(v).strip()
               for v in obj.values()):
            return 1
    return 0


def is_placeholder(obj: Any) -> bool:
    txt = "\n".join(extract_strings(obj))
    return bool(BAD_RE.search(txt))


def find_subject_root(chapter: Path, class_root: Path) -> Path:
    """Nearest ancestor under class root that behaves like a subject package."""
    cur = chapter.parent
    candidates = []
    while cur != class_root and class_root in cur.parents:
        candidates.append(cur)
        if (cur / "00_SUBJECT_INFO").exists() or (cur / "00_SUBJECT_MAPPING").exists():
            return cur
        cur = cur.parent
    # Fallback: direct child of class root on chapter's ancestry.
    for p in reversed(chapter.parents):
        if p.parent == class_root:
            return p
    return chapter.parent


def infer_chapter_meta(path: Path) -> tuple[str, str]:
    info = None
    info_dir = path / "00_CHAPTER_INFO"
    if info_dir.exists():
        for name in CHAPTER_INFO_NAMES:
            p = info_dir / name
            if p.exists():
                info = read_json(p)
                if info is not None:
                    break
    name = path.name
    m = re.match(r"(\d+)[_\-\s]*(.*)", name)
    fallback_id = m.group(1) if m else stable_id(name)[:8]
    fallback_title = (m.group(2) if m else name).replace("_", " ").strip() or name
    if isinstance(info, dict):
        cid = str(info.get("chapter_id") or info.get("id") or info.get("chapterId") or fallback_id)
        title = str(info.get("chapter_title") or info.get("title") or info.get("chapterName") or fallback_title)
        return cid, title
    return fallback_id, fallback_title


def discover_chapters(contents_root: Path) -> list[Chapter]:
    chapters: list[Chapter] = []
    for class_root in sorted(p for p in contents_root.iterdir()
                             if p.is_dir() and p.name.lower().startswith("class ")):
        seen: set[Path] = set()

        # Canonical signal: 00_CHAPTER_INFO directory.
        for info_dir in class_root.rglob("00_CHAPTER_INFO"):
            ch = info_dir.parent
            if any(part in IGNORE_DIRS for part in ch.parts):
                continue
            seen.add(ch)

        # Fallback for packages without chapter_info: all five-pillar/partial-pillar dirs.
        for p in class_root.rglob("*"):
            if not p.is_dir() or p in seen:
                continue
            if any(part in IGNORE_DIRS for part in p.parts):
                continue
            pillar_hits = sum((p / dirname).exists() for dirname in PILLARS.values())
            if pillar_hits >= 2 and re.match(r"^\d+", p.name):
                seen.add(p)

        for ch in sorted(seen):
            subject_root = find_subject_root(ch, class_root)
            cid, title = infer_chapter_meta(ch)
            chapters.append(Chapter(
                class_name=class_root.name,
                subject_name=subject_root.name,
                path=ch,
                rel_path=ch.relative_to(contents_root.parent).as_posix(),
                chapter_id=cid,
                chapter_title=title,
            ))
    return chapters


def collect_json_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        p for p in root.rglob("*.json")
        if p.is_file() and not any(part in IGNORE_DIRS for part in p.parts)
    )


def pillar_audit(chapter: Chapter, pillar: str) -> dict[str, Any]:
    root = chapter.path / PILLARS[pillar]
    files = collect_json_files(root)
    records = 0
    placeholder_files = []
    invalid_json_files = []
    source_derived = 0
    generated = 0

    for f in files:
        obj = read_json(f)
        if obj is None:
            invalid_json_files.append(str(f))
            continue
        c = count_records(obj)
        records += c
        if is_placeholder(obj):
            placeholder_files.append(str(f))
        text = json.dumps(obj, ensure_ascii=False)
        source_derived += len(re.findall(r'"(?:content_origin|status)"\s*:\s*"SOURCE_DERIVED"', text, re.I))
        generated += len(re.findall(r'"(?:content_origin|status)"\s*:\s*"GENERATED"', text, re.I))

    valid_records = max(0, records - sum(
        count_records(read_json(Path(f))) for f in placeholder_files if Path(f).exists()
    ))
    return {
        "pillar": pillar,
        "exists": root.exists(),
        "json_files": len(files),
        "records": records,
        "valid_records_estimate": valid_records,
        "placeholder_files": placeholder_files,
        "invalid_json_files": invalid_json_files,
        "source_derived_markers": source_derived,
        "generated_markers": generated,
        "needs_generation": valid_records < MIN_ITEMS[pillar],
    }


def source_candidates(chapter: Chapter) -> list[Path]:
    """
    Gather chapter-local source material.
    Prioritize actual source/source-derived text and inventories.
    Exclude generated staging/runtime data.
    """
    scored = []
    for p in chapter.path.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in SOURCE_EXTS:
            continue
        if any(part in IGNORE_DIRS for part in p.parts):
            continue
        lower = p.as_posix().lower()
        score = 0
        if "source" in lower:
            score += 50
        if "textbook" in lower:
            score += 40
        if "transcript" in lower:
            score += 40
        if "full_chapter" in lower or "source_content" in lower:
            score += 60
        if "question_inventory" in lower or "activity_inventory" in lower:
            score += 30
        if "03_assess/02_mcq" in lower or "03_assess/03_short_answer" in lower:
            score -= 30
        if "90_generated" in lower or "generated_" in p.name.lower():
            score -= 100
        try:
            size = p.stat().st_size
        except OSError:
            size = 0
        score += min(size // 1000, 20)
        scored.append((score, p))
    scored.sort(key=lambda x: (-x[0], x[1].as_posix()))
    return [p for score, p in scored if score >= 0]


def source_bundle(chapter: Chapter, max_chars: int = 120_000) -> dict[str, Any]:
    files = source_candidates(chapter)
    bundle_files = []
    excerpts = []
    remaining = max_chars

    for p in files:
        try:
            raw = p.read_text(encoding="utf-8-sig")
        except Exception:
            continue
        digest = sha256_file(p)
        rel = p.as_posix()
        bundle_files.append({
            "path": rel,
            "sha256": digest,
            "bytes": p.stat().st_size,
        })
        if remaining > 0:
            text = raw
            if p.suffix.lower() == ".json":
                obj = read_json(p)
                if obj is not None:
                    text = "\n".join(extract_strings(obj))
            text = text.strip()
            if text:
                take = text[:remaining]
                excerpts.append(f"\n--- SOURCE: {rel} sha256={digest} ---\n{take}")
                remaining -= len(take)

    concat_hash = sha256_bytes(
        "\n".join(f"{x['path']}:{x['sha256']}" for x in bundle_files).encode("utf-8")
    )
    return {
        "files": bundle_files,
        "bundle_sha256": concat_hash,
        "text": "\n".join(excerpts),
    }


def make_prompt(chapter: Chapter, missing_pillars: list[str], bundle: dict[str, Any]) -> str:
    schema = {p: GENERATION_SCHEMA[p] for p in missing_pillars}
    return f"""GURUKUL AI SOURCE-GROUNDED CONTENT GENERATION JOB

CLASS: {chapter.class_name}
SUBJECT PACKAGE: {chapter.subject_name}
CHAPTER ID: {chapter.chapter_id}
CHAPTER TITLE: {chapter.chapter_title}
CHAPTER PATH: {chapter.rel_path}
SOURCE BUNDLE SHA256: {bundle['bundle_sha256']}

Generate ONLY the missing pillars:
{json.dumps(missing_pillars, ensure_ascii=False)}

STRICT RULES:
1. Use only the supplied repository source below.
2. Never claim a generated question/activity is copied from the textbook.
3. Every newly authored record MUST set content_origin="GENERATED".
4. Preserve exact textbook/source-derived wording only when it is directly present in source;
   such copied records may be content_origin="SOURCE_DERIVED" and MUST include source_ref.
5. Do not invent external URLs, citations, page numbers, authors, names, facts, or media.
6. Do not output generic/meta questions about "the source chapter", "which source section",
   "an unrelated chapter", validation, pipelines, files, JSON, or AI.
7. Content must be chapter-specific, student-facing, age-appropriate, and useful.
8. For MCQs: exactly one defensible answer, non-trivial distractors, no "None" filler unless
   pedagogically justified by the actual content.
9. If source is insufficient for a requested pillar, return a gap object instead of fabricating.
10. Output JSON only. No Markdown fences.

OUTPUT JSON SHAPE:
{{
  "chapter_id": {json.dumps(chapter.chapter_id)},
  "chapter_title": {json.dumps(chapter.chapter_title, ensure_ascii=False)},
  "source_bundle_sha256": {json.dumps(bundle['bundle_sha256'])},
  "pillars": {{
    "<pillar>": {{
      "items": [
        {{
          "id": "optional; orchestrator will assign deterministic id if absent",
          "content_origin": "GENERATED or SOURCE_DERIVED",
          "source_ref": "repository-relative source path when applicable",
          "...": "pillar-specific fields"
        }}
      ],
      "gap": null
    }}
  }}
}}

PILLAR REQUIREMENTS:
{json.dumps(schema, ensure_ascii=False, indent=2)}

SOURCE MATERIAL:
{bundle['text']}
"""


def validate_generated_payload(payload: Any, chapter: Chapter,
                               missing_pillars: list[str],
                               bundle: dict[str, Any]) -> tuple[bool, list[str], Any]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return False, ["payload is not an object"], payload

    if str(payload.get("chapter_id")) != str(chapter.chapter_id):
        errors.append("chapter_id mismatch")
    if payload.get("source_bundle_sha256") != bundle["bundle_sha256"]:
        errors.append("source_bundle_sha256 mismatch")

    pillars = payload.get("pillars")
    if not isinstance(pillars, dict):
        return False, errors + ["pillars missing/not object"], payload

    source_paths = {x["path"] for x in bundle["files"]}
    normalized = {
        "chapter_id": str(chapter.chapter_id),
        "chapter_title": chapter.chapter_title,
        "class": chapter.class_name,
        "subject": chapter.subject_name,
        "chapter_path": chapter.rel_path,
        "source_bundle_sha256": bundle["bundle_sha256"],
        "generated_at": now_utc(),
        "pillars": {},
    }

    for pillar in missing_pillars:
        pobj = pillars.get(pillar)
        if not isinstance(pobj, dict):
            errors.append(f"{pillar}: missing object")
            continue
        gap = pobj.get("gap")
        items = pobj.get("items", [])
        if gap and items:
            errors.append(f"{pillar}: cannot contain both gap and items")
        if gap:
            normalized["pillars"][pillar] = {"items": [], "gap": gap}
            continue
        if not isinstance(items, list):
            errors.append(f"{pillar}: items must be list")
            continue
        clean_items = []
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                errors.append(f"{pillar}[{i}]: item not object")
                continue
            if is_placeholder(item):
                errors.append(f"{pillar}[{i}]: generic/placeholder content rejected")
                continue

            origin = str(item.get("content_origin") or "GENERATED").upper()
            if origin not in {"GENERATED", "SOURCE_DERIVED"}:
                errors.append(f"{pillar}[{i}]: invalid content_origin={origin}")
                continue
            item["content_origin"] = origin

            src = item.get("source_ref")
            if origin == "SOURCE_DERIVED":
                if not src or src not in source_paths:
                    errors.append(f"{pillar}[{i}]: SOURCE_DERIVED requires exact source_ref")
                    continue
            elif src and src not in source_paths:
                # Generated records may cite one of the provided sources, but not invent refs.
                errors.append(f"{pillar}[{i}]: invented/unknown source_ref")
                continue

            required = GENERATION_SCHEMA[pillar]["required_fields"]
            missing_fields = [k for k in required if not str(item.get(k, "")).strip()]
            if missing_fields:
                errors.append(f"{pillar}[{i}]: missing fields {missing_fields}")
                continue

            item["id"] = item.get("id") or stable_id(
                chapter.class_name, chapter.subject_name, chapter.chapter_id,
                pillar, str(i), json.dumps(item, sort_keys=True, ensure_ascii=False)
            )
            item["chapter_id"] = str(chapter.chapter_id)
            item["source_bundle_sha256"] = bundle["bundle_sha256"]
            clean_items.append(item)

        normalized["pillars"][pillar] = {"items": clean_items, "gap": None}

    return not errors, errors, normalized


def run_generator(command_template: str, prompt_path: Path, output_path: Path) -> int:
    """
    External generator adapter.
    Use placeholders {prompt} and {output}.
    Example:
      --generator-cmd 'python backend/scripts/my_llm_runner.py --prompt {prompt} --output {output}'
    """
    cmd = command_template.format(
        prompt=shlex.quote(str(prompt_path)),
        output=shlex.quote(str(output_path)),
    )
    print(f"[GEN] {cmd}")
    return subprocess.run(cmd, shell=True).returncode


def stage_chapter(chapter: Chapter, run_root: Path, audits: dict[str, Any],
                  generator_cmd: str | None, max_source_chars: int) -> dict[str, Any]:
    missing = [p for p, a in audits.items() if a["needs_generation"]]
    chapter_key = chapter.rel_path.replace("/", "__")
    job_dir = run_root / "jobs" / chapter_key
    result = {
        "chapter": asdict(chapter) | {"path": str(chapter.path)},
        "missing_pillars": missing,
        "status": "complete" if not missing else "planned",
    }
    if not missing:
        return result

    bundle = source_bundle(chapter, max_source_chars)
    result["source_files"] = len(bundle["files"])
    result["source_bundle_sha256"] = bundle["bundle_sha256"]

    if not bundle["files"] or not bundle["text"].strip():
        result["status"] = "gap_no_source"
        result["gap"] = "No usable chapter-local source material found; generation prohibited."
        return result

    prompt = make_prompt(chapter, missing, bundle)
    prompt_path = job_dir / "PROMPT.txt"
    raw_out = job_dir / "RAW_GENERATED.json"
    valid_out = job_dir / "VALIDATED_GENERATED.json"
    meta_out = job_dir / "JOB.json"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(prompt, encoding="utf-8")

    source_manifest = {
        "source_bundle_sha256": bundle["bundle_sha256"],
        "files": bundle["files"],
    }
    dump_json(job_dir / "SOURCE_MANIFEST.json", source_manifest)

    if generator_cmd:
        rc = run_generator(generator_cmd, prompt_path, raw_out)
        if rc != 0:
            result["status"] = "generator_failed"
            result["returncode"] = rc
        elif not raw_out.exists():
            result["status"] = "generator_no_output"
        else:
            payload = read_json(raw_out)
            ok, errors, normalized = validate_generated_payload(
                payload, chapter, missing, bundle
            )
            result["validation_errors"] = errors
            if ok:
                dump_json(valid_out, normalized)
                result["status"] = "validated"
                result["validated_output"] = str(valid_out)
            else:
                result["status"] = "invalid_generated_output"

    dump_json(meta_out, result)
    return result


def promote_validated(run_root: Path, repo_root: Path, manifest: dict[str, Any]) -> list[str]:
    """
    Promote only validated generation results into chapter-local 90_GENERATED folders.
    Original files are never replaced or deleted.
    """
    promoted = []
    for item in manifest["chapters"]:
        if item.get("status") != "validated":
            continue
        validated_path = Path(item["validated_output"])
        payload = read_json(validated_path)
        if not isinstance(payload, dict):
            continue
        chapter_path = repo_root / payload["chapter_path"]
        for pillar, pobj in payload.get("pillars", {}).items():
            if pillar not in PILLARS or not isinstance(pobj, dict):
                continue
            items = pobj.get("items") or []
            gap = pobj.get("gap")
            target_dir = chapter_path / PILLARS[pillar] / "90_GENERATED"
            target = target_dir / f"GENERATED_{pillar.upper()}.json"
            target_obj = {
                "chapter_id": payload["chapter_id"],
                "chapter_title": payload["chapter_title"],
                "content_origin": "GENERATED_PACKAGE",
                "generation_run_id": manifest["run_id"],
                "source_bundle_sha256": payload["source_bundle_sha256"],
                "items": items,
                "gap": gap,
            }
            dump_json(target, target_obj)
            promoted.append(str(target.relative_to(repo_root)))
    return promoted


def try_existing_rebuilders(repo_root: Path) -> list[dict[str, Any]]:
    """
    Run known, existing repository rebuild/audit scripts when present.
    This deliberately avoids inventing a parallel runtime adapter.
    """
    candidates = [
        "backend/scripts/canonical_adapter_class5.py",
        "backend/scripts/forensic_audit_v2.py",
        "backend/scripts/internal_records_forensics.py",
        "backend/scripts/generate_final_certification.py",
    ]
    results = []
    for rel in candidates:
        p = repo_root / rel
        if not p.exists():
            continue
        proc = subprocess.run(
            [sys.executable, str(p)],
            cwd=str(repo_root),
            text=True,
            capture_output=True,
        )
        results.append({
            "script": rel,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        })
    return results


def audit_runtime(repo_root: Path) -> dict[str, Any]:
    rt = repo_root / "runtime-data"
    result = {
        "exists": rt.exists(),
        "catalog_exists": (rt / "catalog.json").exists(),
        "chapter_json_count": 0,
        "placeholder_runtime_files": [],
        "duplicate_ids": [],
    }
    if not rt.exists():
        return result

    ids = Counter()
    for f in rt.rglob("*.json"):
        obj = read_json(f)
        if obj is None:
            continue
        if "chapters" in f.parts:
            result["chapter_json_count"] += 1
        if is_placeholder(obj):
            result["placeholder_runtime_files"].append(str(f.relative_to(repo_root)))

        def walk(v: Any):
            if isinstance(v, dict):
                if "id" in v and isinstance(v["id"], (str, int)):
                    ids[str(v["id"])] += 1
                for x in v.values():
                    walk(x)
            elif isinstance(v, list):
                for x in v:
                    walk(x)
        walk(obj)

    # Runtime may intentionally repeat IDs across indexes; report for review, don't auto-delete.
    result["duplicate_ids"] = [k for k, n in ids.items() if n > 1][:500]
    result["duplicate_id_count"] = sum(1 for n in ids.values() if n > 1)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".", help="GURUKUL-AI repository root")
    ap.add_argument("--run-id", default=os.getenv("GENERATION_RUN_ID"))
    ap.add_argument("--generator-cmd", default=os.getenv("GURUKUL_GENERATOR_CMD"),
                    help="External source-grounded generator command; use {prompt} and {output}")
    ap.add_argument("--max-source-chars", type=int, default=120_000)
    ap.add_argument("--promote", action="store_true",
                    help="Promote ONLY validated staged outputs to 90_GENERATED")
    ap.add_argument("--rebuild", action="store_true",
                    help="Run existing repository canonical/audit scripts after promotion")
    ap.add_argument("--fail-on-gaps", action="store_true")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    contents_root = repo_root / "Contents"
    if not contents_root.exists():
        print(f"ERROR: {contents_root} not found", file=sys.stderr)
        return 2

    run_id = args.run_id or dt.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    run_root = repo_root / "generation_staging" / run_id
    run_root.mkdir(parents=True, exist_ok=True)

    chapters = discover_chapters(contents_root)
    if not chapters:
        print("ERROR: no chapters discovered", file=sys.stderr)
        return 3

    manifest: dict[str, Any] = {
        "run_id": run_id,
        "created_at": now_utc(),
        "repo_root": str(repo_root),
        "policy": {
            "preserve_original_source": True,
            "source_derived_requires_repository_evidence": True,
            "new_pedagogical_content_origin": "GENERATED",
            "generic_placeholders_rejected": True,
            "staging_first": True,
        },
        "summary": {},
        "chapters": [],
    }

    class_subjects: dict[str, set[str]] = defaultdict(set)
    total_placeholders = 0
    total_invalid_json = 0
    total_missing_pillars = 0
    statuses = Counter()

    inventory = []
    for n, chapter in enumerate(chapters, 1):
        class_subjects[chapter.class_name].add(chapter.subject_name)
        audits = {p: pillar_audit(chapter, p) for p in PILLARS}
        total_placeholders += sum(len(a["placeholder_files"]) for a in audits.values())
        total_invalid_json += sum(len(a["invalid_json_files"]) for a in audits.values())
        total_missing_pillars += sum(1 for a in audits.values() if a["needs_generation"])

        staged = stage_chapter(
            chapter, run_root, audits, args.generator_cmd, args.max_source_chars
        )
        staged["pillar_audit"] = audits
        manifest["chapters"].append(staged)
        statuses[staged["status"]] += 1

        inventory.append({
            "class": chapter.class_name,
            "subject": chapter.subject_name,
            "chapter_id": chapter.chapter_id,
            "chapter_title": chapter.chapter_title,
            "path": chapter.rel_path,
            "missing_pillars": staged["missing_pillars"],
            "status": staged["status"],
        })
        print(f"[{n:04d}/{len(chapters):04d}] {chapter.class_name} | "
              f"{chapter.subject_name} | {chapter.chapter_id} {chapter.chapter_title} "
              f"=> {staged['status']} missing={','.join(staged['missing_pillars']) or '-'}")

    manifest["summary"] = {
        "classes": len(class_subjects),
        "class_names": sorted(class_subjects),
        "subjects_by_class": {k: sorted(v) for k, v in sorted(class_subjects.items())},
        "subject_packages": sum(len(v) for v in class_subjects.values()),
        "chapters": len(chapters),
        "missing_pillar_instances": total_missing_pillars,
        "placeholder_files_detected": total_placeholders,
        "invalid_json_files_detected": total_invalid_json,
        "status_counts": dict(statuses),
    }

    dump_json(run_root / "INVENTORY.json", inventory)
    dump_json(run_root / "RUN_MANIFEST.json", manifest)

    gap_manifest = []
    for c in manifest["chapters"]:
        if c["status"] in {"gap_no_source", "invalid_generated_output",
                           "generator_failed", "generator_no_output"}:
            gap_manifest.append({
                "chapter_path": c["chapter"]["rel_path"],
                "chapter_id": c["chapter"]["chapter_id"],
                "missing_pillars": c["missing_pillars"],
                "status": c["status"],
                "gap": c.get("gap"),
                "validation_errors": c.get("validation_errors", []),
            })
    dump_json(run_root / "GAPS.json", gap_manifest)

    if args.promote:
        promoted = promote_validated(run_root, repo_root, manifest)
        manifest["promoted_files"] = promoted
        manifest["promoted_count"] = len(promoted)
        print(f"[PROMOTE] {len(promoted)} validated files/packages promoted.")

    if args.rebuild:
        rebuild = try_existing_rebuilders(repo_root)
        manifest["existing_rebuilder_results"] = rebuild
        print("[REBUILD] existing repository rebuild/audit scripts executed.")

    runtime_audit = audit_runtime(repo_root)
    manifest["runtime_audit"] = runtime_audit

    dump_json(run_root / "RUN_MANIFEST.json", manifest)

    print("\n=== GURUKUL REPOSITORY-WIDE SUMMARY ===")
    print(json.dumps(manifest["summary"], indent=2, ensure_ascii=False))
    print(f"Run artifacts: {run_root}")

    if args.fail_on_gaps and (
        gap_manifest or total_invalid_json or runtime_audit["placeholder_runtime_files"]
    ):
        return 10
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

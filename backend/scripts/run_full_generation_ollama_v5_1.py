#!/usr/bin/env python3
"""
GURUKUL AI V5.1
Schema-driven, validator-first Ollama generator.

V5.1 changes:
- Ollama returns ONLY an array of educational records (or an explicit gap object).
- Python constructs the canonical pillar wrapper.
- Existing V4 pillars are retained only if the repository canonical validator accepts them.
- Invalid pillars are regenerated independently.
- No promotion/rebuild is performed.
- A fresh staging run is used; V4 and previous V5 artifacts remain untouched.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import importlib.util
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

DEFAULT_MODEL = "qwen3.5:2b-q4_K_M"
DEFAULT_URL = "http://127.0.0.1:11434/api/generate"

SCHEMA = {
    "learn": {"required_fields": ["title", "explanation"],
              "target": "lesson/concept explanations grounded only in supplied source"},
    "practice": {"required_fields": ["question"],
                 "target": "chapter-specific practice questions"},
    "assess": {"required_fields": ["question"],
               "target": "chapter-specific assessment questions"},
    "revise": {"required_fields": ["point"],
               "target": "concise chapter-specific revision points"},
    "resources": {"required_fields": ["title"],
                  "target": "source-linked resource references only"},
}

BAD_PATTERNS = [
    r"which source section", r"the source chapter", r"unrelated chapter",
    r"validation", r"pipeline", r"placeholder", r"test question",
    r"metadata", r"file path", r"generated content", r"json",
]
MOJIBAKE = ("Ã", "Â", "â€", "à¤", "à¦", "à®", "à°", "à²", "à³")


def rjson(p: Path):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def wjson(p: Path, obj: Any):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
                 encoding="utf-8")


def load_canonical(repo: Path):
    p = repo / "backend" / "scripts" / "generate_all_valid_contents.py"
    spec = importlib.util.spec_from_file_location("gavc_v51", p)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load {p}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def source_text(repo: Path, raw: str) -> str:
    p = Path(raw)
    if not p.is_absolute():
        p = repo / p
    if not p.exists() or not p.is_file():
        return ""
    try:
        if p.suffix.lower() in {".json", ".jsonl"}:
            return json.dumps(rjson(p), ensure_ascii=False, indent=2)
        return p.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""


def make_bundle(repo: Path, job_dir: Path, limit: int):
    m = rjson(job_dir / "SOURCE_MANIFEST.json")
    files = m.get("files") or []
    chunks = []
    clean_files = []
    for e in files:
        if isinstance(e, str):
            rel = e
            meta = {"path": e}
        elif isinstance(e, dict):
            rel = e.get("path")
            meta = dict(e)
        else:
            continue
        if not rel:
            continue
        clean_files.append(meta)
        txt = source_text(repo, str(rel))
        if txt.strip():
            chunks.append(f"\n===== SOURCE: {rel} =====\n{txt}")
    text = "\n".join(chunks)
    if len(text) > limit:
        text = text[:limit] + "\n[END OF SOURCE BUDGET]"
    return {
        "bundle_sha256": m.get("source_bundle_sha256"),
        "files": clean_files,
        "text": text,
    }


def extract_json(s: str):
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.I)
        s = re.sub(r"\s*```$", "", s)
    try:
        return json.loads(s)
    except Exception:
        pass

    for start, ch in enumerate(s):
        if ch not in "[{":
            continue
        stack = []
        string = False
        escape = False
        for i in range(start, len(s)):
            c = s[i]
            if string:
                if escape:
                    escape = False
                elif c == "\\":
                    escape = True
                elif c == '"':
                    string = False
                continue
            if c == '"':
                string = True
            elif c in "[{":
                stack.append(c)
            elif c in "]}":
                if not stack:
                    break
                op = stack.pop()
                if (op, c) not in {("[", "]"), ("{", "}")}:
                    break
                if not stack:
                    try:
                        return json.loads(s[start:i + 1])
                    except Exception:
                        break
    raise ValueError("No valid JSON found in Ollama response")


def call(model, url, prompt_text, temperature):
    body = {
        "model": model,
        "prompt": prompt_text,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": temperature},
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        return str(json.loads(resp.read().decode("utf-8")).get("response", ""))


def prompt(ch, pillar, b):
    spec = SCHEMA[pillar]
    fields = ", ".join(spec["required_fields"])
    return f"""GURUKUL AI EDUCATIONAL CONTENT GENERATION

Generate records for exactly ONE pillar of this textbook chapter.

Class: {ch['class_name']}
Subject: {ch['subject_name']}
Chapter ID: {ch['chapter_id']}
Chapter title: {ch['chapter_title']}
Pillar: {pillar}
Purpose: {spec['target']}
Required fields: {fields}

SOURCE RULES:
- Use ONLY the supplied source material.
- Content must be chapter-specific and student-facing.
- Do not invent facts, names, events, quotations, URLs, citations, page numbers,
  authors, media or textbook wording.
- New material must use content_origin="GENERATED".
- SOURCE_DERIVED may be used only for material directly present in the supplied
  source and must use an exact source_ref from the supplied source list.
- Never invent source_ref.
- Do not mention AI, JSON, validation, pipelines, files, metadata or instructions.
- If the source genuinely cannot support this pillar, return a gap instead of
  fabricating.
- For assessment MCQs, exactly one answer must be defensible and distractors
  must be meaningful.

PILLAR RULES:
learn: every record MUST have title and explanation; teach distinct concepts.
practice: every record MUST have question; make questions specific to this chapter.
assess: every record MUST have question; use MCQ structure only when meaningful.
revise: every record MUST have point; keep points concise and chapter-specific.
resources: every record MUST have title; use only resources actually present in source.

OUTPUT ONLY ONE OF THESE TWO JSON FORMS.

SUCCESS:
[
  {{
    "content_origin": "GENERATED",
    "source_ref": null,
    "{spec['required_fields'][0]}": "..."
  }}
]

GAP:
{{
  "gap": "Specific source-based reason this pillar cannot be generated."
}}

IMPORTANT:
- The outer response MUST be a JSON array for successful generation.
- Do NOT wrap it inside "items".
- Do NOT output chapter_id, pillars, generated_at or other repository metadata.
- Do NOT output Markdown.

SOURCE MATERIAL:
{b['text']}
"""


def validate_items(pillar, result, source_paths):
    if isinstance(result, dict) and result.get("gap"):
        gap = result["gap"]
        if isinstance(gap, str) and gap.strip():
            return True, [], {"items": [], "gap": gap.strip()}
        return False, ["invalid gap"], None

    if not isinstance(result, list):
        return False, ["model output must be a JSON array or explicit gap object"], None
    if not result:
        return False, ["empty array; use an explicit gap if source is insufficient"], None

    errors = []
    items = []
    for i, item in enumerate(result):
        if not isinstance(item, dict):
            errors.append(f"{pillar}[{i}] is not an object")
            continue

        origin = str(item.get("content_origin") or "GENERATED").upper()
        if origin not in {"GENERATED", "SOURCE_DERIVED"}:
            errors.append(f"{pillar}[{i}] invalid content_origin")
            continue

        src = item.get("source_ref")
        if origin == "SOURCE_DERIVED" and (not src or src not in source_paths):
            errors.append(f"{pillar}[{i}] invalid SOURCE_DERIVED source_ref")
            continue
        if origin == "GENERATED" and src and src not in source_paths:
            errors.append(f"{pillar}[{i}] invented source_ref")
            continue

        missing = [
            f for f in SCHEMA[pillar]["required_fields"]
            if not str(item.get(f, "")).strip()
        ]
        if missing:
            errors.append(f"{pillar}[{i}] missing fields {missing}")
            continue

        text_values = []
        for v in item.values():
            if isinstance(v, str):
                text_values.append(v)
            elif isinstance(v, list):
                text_values.extend(x for x in v if isinstance(x, str))
        joined = " ".join(text_values)
        if any(re.search(p, joined, re.I) for p in BAD_PATTERNS):
            errors.append(f"{pillar}[{i}] generic/meta content")
            continue
        if any(x in joined for x in MOJIBAKE):
            errors.append(f"{pillar}[{i}] mojibake detected")
            continue

        x = copy.deepcopy(item)
        x["content_origin"] = origin
        items.append(x)

    return (not errors), errors, ({"items": items, "gap": None} if not errors else None)


def canonical_validate(mod, ch, b, pillars, payload):
    C = mod.Chapter(
        class_name=ch["class_name"],
        subject_name=ch["subject_name"],
        path=Path(ch["path"]),
        rel_path=ch["rel_path"],
        chapter_id=str(ch["chapter_id"]),
        chapter_title=ch["chapter_title"],
    )
    return mod.validate_generated_payload(payload, C, pillars, b)


def jobs(inp):
    root = inp / "jobs"
    if not root.exists():
        return []
    return sorted(p for p in root.iterdir()
                  if p.is_dir() and (p / "JOB.json").exists())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    ap.add_argument("--output-run", default=None)
    ap.add_argument("--model", default=os.getenv("OLLAMA_MODEL", DEFAULT_MODEL))
    ap.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", DEFAULT_URL))
    ap.add_argument("--max-source-chars", type=int,
                    default=int(os.getenv("V51_MAX_SOURCE_CHARS", "50000")))
    ap.add_argument("--temperature", type=float,
                    default=float(os.getenv("V51_TEMPERATURE", "0.15")))
    ap.add_argument("--max-retries", type=int,
                    default=int(os.getenv("V51_MAX_RETRIES", "4")))
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    inp = Path(args.input_run).resolve()
    out = (Path(args.output_run).resolve() if args.output_run
           else Path(str(inp) + "_V51"))

    mod = load_canonical(repo)
    job_list = jobs(inp)
    if not job_list:
        print("ERROR: no JOB.json files found")
        return 2

    out.mkdir(parents=True, exist_ok=True)
    report = {
        "version": "V5.1",
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "model": args.model,
        "input_run": str(inp),
        "output_run": str(out),
        "jobs": [],
    }

    passed = failed = 0

    for n, jd in enumerate(job_list, 1):
        job = rjson(jd / "JOB.json")
        ch = job["chapter"]
        missing = list(job.get("missing_pillars") or [])
        od = out / "jobs" / jd.name
        od.mkdir(parents=True, exist_ok=True)
        wjson(od / "JOB.json", job)
        wjson(od / "SOURCE_MANIFEST.json", rjson(jd / "SOURCE_MANIFEST.json"))

        entry = {
            "job": jd.name,
            "chapter_id": str(ch["chapter_id"]),
            "chapter_title": ch["chapter_title"],
            "missing_pillars": missing,
            "status": "failed",
            "errors": [],
        }

        print(f"\n[{n}/{len(job_list)}] {ch['chapter_id']} — {ch['chapter_title']}")

        try:
            b = make_bundle(repo, jd, args.max_source_chars)
            if not b["bundle_sha256"] or not b["text"].strip():
                raise RuntimeError("No usable source material")

            source_paths = {
                str(x["path"]) for x in b["files"]
                if isinstance(x, dict) and x.get("path")
            }

            pillars = {}

            # Salvage V4 only at pillar granularity, using the actual canonical validator.
            v4 = jd / "RAW_GENERATED.json"
            if v4.exists():
                try:
                    old = rjson(v4)
                    for p in missing:
                        candidate = (old.get("pillars") or {}).get(p)
                        if not isinstance(candidate, dict):
                            continue
                        payload = {
                            "chapter_id": str(ch["chapter_id"]),
                            "chapter_title": ch["chapter_title"],
                            "source_bundle_sha256": b["bundle_sha256"],
                            "pillars": {p: candidate},
                        }
                        ok, errs, norm = canonical_validate(
                            mod, ch, b, [p], payload
                        )
                        if ok:
                            pillars[p] = norm["pillars"][p]
                            print(f"  {p}: KEEP V4 canonical-valid")
                except Exception:
                    pass

            for p in missing:
                if p in pillars:
                    continue

                base = prompt(ch, p, b)
                last_errors = []

                for attempt in range(1, args.max_retries + 1):
                    try:
                        print(f"  {p}: attempt {attempt}/{args.max_retries}")
                        raw = call(
                            args.model,
                            args.ollama_url,
                            base if attempt == 1 else
                            base + "\n\nREPAIR THE PREVIOUS OUTPUT.\n"
                            "Errors:\n" +
                            json.dumps(last_errors, ensure_ascii=False) +
                            "\nReturn ONLY the corrected JSON array or explicit gap object.",
                            args.temperature,
                        )
                        parsed = extract_json(raw)
                        ok, errs, norm = validate_items(p, parsed, source_paths)
                        if not ok:
                            last_errors = errs
                            print("    LOCAL REJECT:", "; ".join(errs[:3]))
                            continue

                        payload = {
                            "chapter_id": str(ch["chapter_id"]),
                            "chapter_title": ch["chapter_title"],
                            "source_bundle_sha256": b["bundle_sha256"],
                            "pillars": {p: norm},
                        }
                        ok, errs, cnorm = canonical_validate(
                            mod, ch, b, [p], payload
                        )
                        if not ok:
                            last_errors = errs
                            print("    CANONICAL REJECT:", "; ".join(errs[:3]))
                            continue

                        pillars[p] = cnorm["pillars"][p]
                        print(f"  {p}: PASS")
                        break

                    except Exception as exc:
                        last_errors = [f"{type(exc).__name__}: {exc}"]
                        print("    ERROR:", last_errors[0])
                    time.sleep(1)

                if p not in pillars:
                    entry["errors"].append(f"{p}: {last_errors}")
                    break

            if len(pillars) != len(missing):
                failed += 1
            else:
                final_payload = {
                    "chapter_id": str(ch["chapter_id"]),
                    "chapter_title": ch["chapter_title"],
                    "source_bundle_sha256": b["bundle_sha256"],
                    "pillars": pillars,
                }
                ok, errs, normalized = canonical_validate(
                    mod, ch, b, missing, final_payload
                )
                if not ok:
                    entry["errors"].extend(errs)
                    failed += 1
                else:
                    wjson(od / "RAW_GENERATED.json", final_payload)
                    wjson(od / "VALIDATED_GENERATED.json", normalized)
                    entry["status"] = "validated"
                    entry["validated_output"] = str(
                        od / "VALIDATED_GENERATED.json"
                    )
                    passed += 1
                    print("  JOB: CANONICALLY VALIDATED")

        except Exception as exc:
            entry["errors"].append(f"{type(exc).__name__}: {exc}")
            failed += 1

        wjson(od / "JOB_RESULT.json", entry)
        report["jobs"].append(entry)

    report["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    report["summary"] = {
        "total_jobs": len(job_list),
        "passed": passed,
        "failed": failed,
    }
    wjson(out / "V5_1_GENERATION_REPORT.json", report)

    print("\n" + "=" * 72)
    print("V5.1 COMPLETE")
    print(f"Total : {len(job_list)}")
    print(f"Pass  : {passed}")
    print(f"Fail  : {failed}")
    print(f"Report: {out / 'V5_1_GENERATION_REPORT.json'}")
    print("=" * 72)

    if failed:
        print("SAFETY STOP: promotion/rebuild NOT performed.")
        return 1

    print("ALL JOBS PASSED CANONICAL VALIDATION.")
    print("Promotion/rebuild NOT performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

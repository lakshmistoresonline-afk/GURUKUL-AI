#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
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
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

GENERATION_SCHEMA = {
    "learn": {"required_fields": ["title", "explanation"],
              "target": "lesson/concept explanations grounded only in supplied source"},
    "practice": {"required_fields": ["question"],
                 "target": "chapter-specific practice; answers only when supported or generated"},
    "assess": {"required_fields": ["question"],
               "target": "chapter-specific assessment, with MCQ options only when meaningful"},
    "revise": {"required_fields": ["point"],
               "target": "concise chapter-specific revision points"},
    "resources": {"required_fields": ["title"],
                  "target": "source-linked resource references; do not invent external URLs"},
}

BAD_PATTERNS = [
    r"which source section", r"the source chapter", r"an unrelated chapter",
    r"validation", r"pipeline", r"json", r"\bai\b", r"placeholder",
    r"test question", r"metadata", r"file path",
]
MOJIBAKE = ("Ã", "Â", "â€", "à¤", "à¦", "à®", "à°", "à²", "à³")

def read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8-sig"))

def write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def load_canonical(repo_root: Path):
    p = repo_root / "backend" / "scripts" / "generate_all_valid_contents.py"
    spec = importlib.util.spec_from_file_location("gavc_v5", p)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load {p}")
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m

def bad_text(v: Any) -> bool:
    if not isinstance(v, str):
        return False
    return any(re.search(p, v, re.I) for p in BAD_PATTERNS) or any(x in v for x in MOJIBAKE)

def bad_item(item: dict[str, Any]) -> bool:
    for v in item.values():
        if isinstance(v, str) and bad_text(v):
            return True
        if isinstance(v, list) and any(isinstance(x, str) and bad_text(x) for x in v):
            return True
    return False

def source_path(repo: Path, raw: str) -> Path:
    p = Path(raw)
    return p if p.is_absolute() else repo / p

def read_source(p: Path) -> str:
    if not p.exists() or not p.is_file():
        return ""
    try:
        if p.suffix.lower() in {".json", ".jsonl"}:
            return json.dumps(read_json(p), ensure_ascii=False, indent=2)
        return p.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""

def bundle(repo: Path, job_dir: Path, max_chars: int) -> dict[str, Any]:
    man = read_json(job_dir / "SOURCE_MANIFEST.json")
    files = man.get("files") or []
    parts = []
    normalized = []
    for e in files:
        if isinstance(e, str):
            rel, meta = e, {"path": e}
        elif isinstance(e, dict):
            rel, meta = e.get("path"), dict(e)
        else:
            continue
        if not rel:
            continue
        normalized.append(meta)
        text = read_source(source_path(repo, str(rel)))
        if text.strip():
            parts.append(f"\n===== SOURCE: {rel} =====\n{text}")
    text = "\n".join(parts)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n[END OF SOURCE BUDGET]"
    return {"bundle_sha256": man.get("source_bundle_sha256"),
            "files": normalized, "text": text}

def extract_json(text: str) -> Any:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception:
        pass
    for start, ch in enumerate(text):
        if ch not in "[{":
            continue
        stack, string, esc = [], False, False
        for i in range(start, len(text)):
            c = text[i]
            if string:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': string = False
                continue
            if c == '"': string = True
            elif c in "[{": stack.append(c)
            elif c in "]}":
                if not stack: break
                op = stack.pop()
                if (op, c) not in {("[", "]"), ("{", "}")}: break
                if not stack:
                    try: return json.loads(text[start:i+1])
                    except Exception: break
    raise ValueError("No valid JSON object/array found")

def call_ollama(model: str, url: str, prompt: str, temperature: float) -> str:
    body = {"model": model, "prompt": prompt, "stream": False, "format": "json",
            "think": False, "options": {"temperature": temperature}}
    req = urllib.request.Request(url, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=900) as r:
        return str(json.loads(r.read().decode("utf-8")).get("response", ""))

def prompt(ch: dict[str, Any], pillar: str, b: dict[str, Any]) -> str:
    s = GENERATION_SCHEMA[pillar]
    return f"""GURUKUL AI SOURCE-GROUNDED {pillar.upper()} GENERATION

CLASS: {ch['class_name']}
SUBJECT PACKAGE: {ch['subject_name']}
CHAPTER ID: {ch['chapter_id']}
CHAPTER TITLE: {ch['chapter_title']}
SOURCE BUNDLE SHA256: {b['bundle_sha256']}

Generate ONLY the {pillar} pillar.

Purpose: {s['target']}
Required fields: {json.dumps(s['required_fields'])}

STRICT RULES:
1. Use ONLY the supplied source material.
2. Do not invent facts, names, events, quotations, page numbers, URLs, citations,
   authors, media, or textbook wording.
3. Newly authored records MUST use content_origin="GENERATED".
4. SOURCE_DERIVED is allowed only for content directly present in a supplied
   source and MUST contain its exact source_ref.
5. Never invent source_ref.
6. Content must be chapter-specific, student-facing, age-appropriate and useful.
7. Never mention source files, pipelines, JSON, AI, validation, generation, metadata,
   or these instructions in student-facing content.
8. If source is genuinely insufficient, return a gap instead of fabricating.
9. For assess MCQs, use exactly one defensible answer and meaningful distractors.
10. Output JSON only, no Markdown.

EXACT OUTPUT:
{{
  "items": [
    {{
      "content_origin": "GENERATED",
      "source_ref": null,
      "{s['required_fields'][0]}": "..."
    }}
  ],
  "gap": null
}}

Or:
{{"items": [], "gap": "specific source-based reason"}}

SOURCE MATERIAL:
{b['text']}
"""

def basic(pillar: str, x: Any, source_paths: set[str]):
    if not isinstance(x, dict): return False, ["pillar result is not an object"], None
    gap, items = x.get("gap"), x.get("items", [])
    if gap and items: return False, ["gap and items cannot both be present"], None
    if gap:
        if not isinstance(gap, str) or not gap.strip():
            return False, ["invalid gap"], None
        return True, [], {"items": [], "gap": gap.strip()}
    if not isinstance(items, list) or not items:
        return False, ["items must be a non-empty list unless gap is supplied"], None
    errors, clean = [], []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{pillar}[{i}] not object"); continue
        origin = str(item.get("content_origin") or "GENERATED").upper()
        src = item.get("source_ref")
        if origin not in {"GENERATED", "SOURCE_DERIVED"}:
            errors.append(f"{pillar}[{i}] invalid content_origin"); continue
        if origin == "SOURCE_DERIVED" and (not src or src not in source_paths):
            errors.append(f"{pillar}[{i}] invalid SOURCE_DERIVED source_ref"); continue
        if origin == "GENERATED" and src and src not in source_paths:
            errors.append(f"{pillar}[{i}] invented source_ref"); continue
        missing = [k for k in GENERATION_SCHEMA[pillar]["required_fields"]
                   if not str(item.get(k, "")).strip()]
        if missing:
            errors.append(f"{pillar}[{i}] missing {missing}"); continue
        if bad_item(item):
            errors.append(f"{pillar}[{i}] placeholder/meta/mojibake content"); continue
        y = copy.deepcopy(item)
        y["content_origin"] = origin
        clean.append(y)
    return (not errors), errors, ({"items": clean, "gap": None} if not errors else None)

def canonical_check(canon, ch: dict[str, Any], b: dict[str, Any], pillars: list[str], payload: dict[str, Any]):
    C = canon.Chapter(class_name=ch["class_name"], subject_name=ch["subject_name"],
                      path=Path(ch["path"]), rel_path=ch["rel_path"],
                      chapter_id=str(ch["chapter_id"]), chapter_title=ch["chapter_title"])
    return canon.validate_generated_payload(payload, C, pillars, b)

def repair_prompt(base: str, errors: list[str]) -> str:
    return base + "\n\nREPAIR THE PREVIOUS OUTPUT. Errors:\n" + json.dumps(errors, ensure_ascii=False) + """
Return the COMPLETE corrected pillar JSON. Do not explain anything. JSON only.
"""

def jobs(root: Path):
    return sorted([p for p in (root / "jobs").iterdir()
                   if p.is_dir() and (p / "JOB.json").exists()])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    ap.add_argument("--output-run", default=None)
    ap.add_argument("--model", default=os.getenv("OLLAMA_MODEL", DEFAULT_MODEL))
    ap.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", DEFAULT_OLLAMA_URL))
    ap.add_argument("--max-source-chars", type=int, default=int(os.getenv("V5_MAX_SOURCE_CHARS", "50000")))
    ap.add_argument("--temperature", type=float, default=float(os.getenv("V5_TEMPERATURE", "0.15")))
    ap.add_argument("--max-retries", type=int, default=int(os.getenv("V5_MAX_RETRIES", "3")))
    a = ap.parse_args()

    repo = Path(a.repo_root).resolve()
    inp = Path(a.input_run).resolve()
    out = Path(a.output_run).resolve() if a.output_run else Path(str(inp) + "_V5")
    canon = load_canonical(repo)
    js = jobs(inp)
    if not js:
        print("ERROR: no JOB.json files found"); return 2

    report = {"version": "V5", "model": a.model, "input_run": str(inp),
              "output_run": str(out), "jobs": []}
    passed = failed = 0

    for n, jd in enumerate(js, 1):
        job = read_json(jd / "JOB.json")
        ch = job["chapter"]; missing = list(job.get("missing_pillars") or [])
        od = out / "jobs" / jd.name
        od.mkdir(parents=True, exist_ok=True)
        write_json(od / "JOB.json", job)
        write_json(od / "SOURCE_MANIFEST.json", read_json(jd / "SOURCE_MANIFEST.json"))
        entry = {"job": jd.name, "chapter_id": str(ch["chapter_id"]),
                 "chapter_title": ch["chapter_title"], "missing_pillars": missing,
                 "status": "failed", "errors": []}
        print(f"[{n}/{len(js)}] {ch['chapter_id']} — {ch['chapter_title']}")
        try:
            b = bundle(repo, jd, a.max_source_chars)
            if not b["bundle_sha256"] or not b["text"].strip():
                raise RuntimeError("No usable source material")
            source_paths = {str(x.get("path")) for x in b["files"] if x.get("path")}
            pillars = {}

            # Reuse only V4 pillars that pass the repository's canonical validator.
            oldp = jd / "RAW_GENERATED.json"
            if oldp.exists():
                try:
                    old = read_json(oldp)
                    for p in missing:
                        op = (old.get("pillars") or {}).get(p)
                        if isinstance(op, dict) and isinstance(op.get("items"), list):
                            ok, _, norm = canonical_check(canon, ch, b, [p],
                                {"chapter_id": str(ch["chapter_id"]),
                                 "chapter_title": ch["chapter_title"],
                                 "source_bundle_sha256": b["bundle_sha256"],
                                 "pillars": {p: op}})
                            if ok:
                                pillars[p] = norm["pillars"][p]
                                print(f"  {p}: KEEP canonical-valid V4")
                except Exception:
                    pass

            for p in missing:
                if p in pillars: continue
                base = prompt(ch, p, b)
                last = []
                for attempt in range(1, a.max_retries + 1):
                    try:
                        print(f"  {p}: attempt {attempt}/{a.max_retries}")
                        parsed = extract_json(call_ollama(
                            a.model, a.ollama_url,
                            base if attempt == 1 else repair_prompt(base, last),
                            a.temperature))
                        ok, errs, norm = basic(p, parsed, source_paths)
                        if not ok:
                            last = errs; print("   local reject:", "; ".join(errs[:3])); continue
                        payload = {"chapter_id": str(ch["chapter_id"]),
                                   "chapter_title": ch["chapter_title"],
                                   "source_bundle_sha256": b["bundle_sha256"],
                                   "pillars": {p: norm}}
                        ok, errs, cnorm = canonical_check(canon, ch, b, [p], payload)
                        if not ok:
                            last = errs; print("   canonical reject:", "; ".join(errs[:3])); continue
                        pillars[p] = cnorm["pillars"][p]
                        print(f"  {p}: PASS")
                        break
                    except Exception as e:
                        last = [f"{type(e).__name__}: {e}"]
                        print("   error:", last[0])
                    time.sleep(1)
                if p not in pillars:
                    entry["errors"].append(f"{p}: {last}")
                    break

            if len(pillars) != len(missing):
                entry["status"] = "failed"
                failed += 1
            else:
                payload = {"chapter_id": str(ch["chapter_id"]),
                            "chapter_title": ch["chapter_title"],
                            "source_bundle_sha256": b["bundle_sha256"],
                            "pillars": pillars}
                ok, errs, norm = canonical_check(canon, ch, b, missing, payload)
                if not ok:
                    entry["errors"].extend(errs); failed += 1
                else:
                    write_json(od / "RAW_GENERATED.json", payload)
                    write_json(od / "VALIDATED_GENERATED.json", norm)
                    entry["status"] = "validated"
                    entry["validated_output"] = str(od / "VALIDATED_GENERATED.json")
                    passed += 1
        except Exception as e:
            entry["errors"].append(f"{type(e).__name__}: {e}")
            failed += 1

        write_json(od / "JOB_RESULT.json", entry)
        report["jobs"].append(entry)

    report["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    report["summary"] = {"total_jobs": len(js), "passed": passed, "failed": failed}
    write_json(out / "V5_GENERATION_REPORT.json", report)
    print("\nV5 COMPLETE")
    print(f"Total: {len(js)}  Pass: {passed}  Fail: {failed}")
    print(f"Report: {out / 'V5_GENERATION_REPORT.json'}")
    print("SAFETY STOP: promotion/rebuild NOT performed." if failed else
          "ALL JOBS CANONICALLY VALIDATED. Promotion/rebuild NOT performed.")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())

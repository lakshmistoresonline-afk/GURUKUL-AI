#!/usr/bin/env python3
"""
GURUKUL AI V5.2 — production recovery generator.

Purpose:
  Recover the 136 missing generation jobs using Ollama while letting the
  repository's canonical validator remain the authority.

Key hardening:
- Accepts safe JSON variants from small local models:
    {"items":[...]}
    {"learn":[...]}
    {"learn":{"items":[...]}}
    {"records":[...]}
    {"data":[...]}
    [{"..."}]
    {"title":"...", "explanation":"..."}   (single item)
- NEVER invents missing required fields.
- NEVER invents source_ref.
- NEVER turns a model failure into a fake gap.
- Validates every pillar with the repository's actual validator.
- Reuses only canonically-valid V4 pillars.
- Creates a fresh V5.2 staging run.
- Optional --promote-and-rebuild performs promotion/rebuild ONLY after 100%
  canonical validation; otherwise it hard-stops.

Default model: qwen3.5:2b-q4_K_M
"""

from __future__ import annotations
import argparse, copy, datetime as dt, importlib.util, json, os, re, sys, time
import urllib.request
from pathlib import Path
from typing import Any

MODEL_DEFAULT = "qwen3.5:2b-q4_K_M"
URL_DEFAULT = "http://127.0.0.1:11434/api/generate"

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

BAD = [
    r"which source section", r"the source chapter", r"unrelated chapter",
    r"validation", r"pipeline", r"placeholder", r"test question",
    r"metadata", r"file path", r"json", r"artificial intelligence",
    r"\bai\b",
]
MOJI = ("Ã", "Â", "â€", "à¤", "à¦", "à®", "à°", "à²", "à³")


def readj(p: Path):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def writej(p: Path, x):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n",
                  encoding="utf-8")


def canonical(repo: Path):
    p = repo / "backend" / "scripts" / "generate_all_valid_contents.py"
    spec = importlib.util.spec_from_file_location("gavc_v52", p)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load canonical generator: {p}")
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


def read_source(repo, raw):
    p = Path(raw)
    if not p.is_absolute():
        p = repo / p
    if not p.exists() or not p.is_file():
        return ""
    try:
        if p.suffix.lower() in {".json", ".jsonl"}:
            return json.dumps(readj(p), ensure_ascii=False, indent=2)
        return p.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""


def make_bundle(repo, jd, limit):
    m = readj(jd / "SOURCE_MANIFEST.json")
    files = m.get("files") or []
    out, usable = [], []
    for e in files:
        if isinstance(e, str):
            rel, meta = e, {"path": e}
        elif isinstance(e, dict):
            rel, meta = e.get("path"), dict(e)
        else:
            continue
        if not rel:
            continue
        usable.append(meta)
        txt = read_source(repo, rel)
        if txt.strip():
            out.append(f"\n===== SOURCE: {rel} =====\n{txt}")
    text = "\n".join(out)
    if len(text) > limit:
        text = text[:limit] + "\n[END OF SOURCE BUDGET]"
    return {"bundle_sha256": m.get("source_bundle_sha256"),
            "files": usable, "text": text}


def extract_json(s):
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.I)
        s = re.sub(r"\s*```$", "", s)
    try:
        return json.loads(s)
    except Exception:
        pass
    # Safe balanced JSON extraction from a response containing surrounding text.
    for start, c0 in enumerate(s):
        if c0 not in "[{":
            continue
        stack, quoted, esc = [], False, False
        for i in range(start, len(s)):
            c = s[i]
            if quoted:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': quoted = False
                continue
            if c == '"': quoted = True
            elif c in "[{": stack.append(c)
            elif c in "]}":
                if not stack: break
                op = stack.pop()
                if (op, c) not in {("[", "]"), ("{", "}")}: break
                if not stack:
                    try:
                        return json.loads(s[start:i+1])
                    except Exception:
                        break
    raise ValueError("No parseable JSON in model response")


def ollama(model, url, p, temp):
    body = {
        "model": model, "prompt": p, "stream": False, "format": "json",
        "think": False, "options": {"temperature": temp}
    }
    req = urllib.request.Request(
        url, data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=900) as r:
        x = json.loads(r.read().decode("utf-8"))
    return str(x.get("response", ""))


def bad_text(s):
    return any(re.search(p, s, re.I) for p in BAD) or any(x in s for x in MOJI)


def bad_item(item):
    for v in item.values():
        if isinstance(v, str) and bad_text(v):
            return True
        if isinstance(v, list) and any(isinstance(x, str) and bad_text(x) for x in v):
            return True
    return False


def unwrap_records(pillar, parsed):
    """Convert only unambiguous model JSON into a list of records or a gap."""
    if isinstance(parsed, list):
        return parsed, None

    if not isinstance(parsed, dict):
        return None, None

    if isinstance(parsed.get("gap"), str) and parsed["gap"].strip() and not parsed.get("items"):
        return [], parsed["gap"].strip()

    # Common wrappers emitted by small models.
    for key in ("items", "records", "data", "results", pillar):
        if key not in parsed:
            continue
        v = parsed[key]
        if isinstance(v, list):
            return v, None
        if isinstance(v, dict):
            if isinstance(v.get("items"), list):
                return v["items"], v.get("gap")
            # A single record under the pillar key.
            if any(k in v for k in SCHEMA[pillar]["required_fields"]):
                return [v], None

    # Single educational record.
    if any(k in parsed for k in SCHEMA[pillar]["required_fields"]):
        return [parsed], None

    return None, None


def validate_items(pillar, parsed, source_paths):
    records, gap = unwrap_records(pillar, parsed)
    if gap:
        return True, [], {"items": [], "gap": gap}
    if records is None:
        return False, ["model JSON has no unambiguous record collection"], None
    if not records:
        return False, ["empty record collection"], None

    errors, clean = [], []
    required = SCHEMA[pillar]["required_fields"]

    for i, item in enumerate(records):
        if not isinstance(item, dict):
            errors.append(f"{pillar}[{i}] is not an object")
            continue

        origin = str(item.get("content_origin") or "GENERATED").upper()
        src = item.get("source_ref")

        if origin not in {"GENERATED", "SOURCE_DERIVED"}:
            errors.append(f"{pillar}[{i}] invalid content_origin")
            continue
        if origin == "SOURCE_DERIVED" and (not src or src not in source_paths):
            errors.append(f"{pillar}[{i}] invalid SOURCE_DERIVED source_ref")
            continue
        if origin == "GENERATED" and src and src not in source_paths:
            errors.append(f"{pillar}[{i}] invented source_ref")
            continue

        missing = [f for f in required if not str(item.get(f, "")).strip()]
        if missing:
            errors.append(f"{pillar}[{i}] missing fields {missing}")
            continue

        if bad_item(item):
            errors.append(f"{pillar}[{i}] placeholder/meta/mojibake content")
            continue

        x = copy.deepcopy(item)
        x["content_origin"] = origin
        clean.append(x)

    return (not errors), errors, ({"items": clean, "gap": None} if not errors else None)


def make_prompt(ch, pillar, b):
    spec = SCHEMA[pillar]
    return f"""GURUKUL AI SOURCE-GROUNDED EDUCATIONAL GENERATION

Chapter: {ch['chapter_title']}
Class: {ch['class_name']}
Subject: {ch['subject_name']}
Chapter ID: {ch['chapter_id']}
Pillar: {pillar}

Generate useful, age-appropriate, chapter-specific educational records using
ONLY the supplied source.

Required fields for EVERY record:
{json.dumps(spec['required_fields'], ensure_ascii=False)}

RULES:
- New records MUST use content_origin="GENERATED".
- SOURCE_DERIVED is allowed only when directly present in source and source_ref
  is exactly one supplied source path.
- Never invent facts, names, citations, page numbers, URLs or media.
- Never invent source_ref.
- Never mention AI, JSON, files, validation, pipelines, metadata or instructions.
- If the source genuinely cannot support this pillar, return a gap object.
- Assess MCQs must have one defensible answer and meaningful distractors.
- Do not produce generic questions.

OUTPUT:
Return either:
{{"items":[{{"content_origin":"GENERATED","source_ref":null,...}}]}}
OR:
{{"gap":"specific source-based reason"}}

The Python validator will construct the canonical wrapper. Do not output chapter_id,
pillars, generated_at, source hashes, or Markdown.

SOURCE:
{b['text']}
"""


def can_check(mod, ch, b, pillars, payload):
    C = mod.Chapter(class_name=ch["class_name"], subject_name=ch["subject_name"],
                    path=Path(ch["path"]), rel_path=ch["rel_path"],
                    chapter_id=str(ch["chapter_id"]), chapter_title=ch["chapter_title"])
    return mod.validate_generated_payload(payload, C, pillars, b)


def jobs(inp):
    root = inp / "jobs"
    return sorted([p for p in root.iterdir()
                   if p.is_dir() and (p / "JOB.json").exists()])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    ap.add_argument("--output-run", default=None)
    ap.add_argument("--model", default=os.getenv("OLLAMA_MODEL", MODEL_DEFAULT))
    ap.add_argument("--ollama-url", default=os.getenv("OLLAMA_URL", URL_DEFAULT))
    ap.add_argument("--max-source-chars", type=int, default=50000)
    ap.add_argument("--temperature", type=float, default=0.15)
    ap.add_argument("--max-retries", type=int, default=5)
    ap.add_argument("--promote-and-rebuild", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    inp = Path(args.input_run).resolve()
    out = Path(args.output_run).resolve() if args.output_run else Path(str(inp) + "_V52")
    mod = canonical(repo)
    js = jobs(inp)

    if not js:
        print("ERROR: no jobs")
        return 2

    report = {"version": "V5.2", "model": args.model, "input_run": str(inp),
              "output_run": str(out), "jobs": []}
    passed = failed = 0

    for n, jd in enumerate(js, 1):
        job = readj(jd / "JOB.json")
        ch = job["chapter"]
        missing = list(job.get("missing_pillars") or [])
        od = out / "jobs" / jd.name
        od.mkdir(parents=True, exist_ok=True)
        writej(od / "JOB.json", job)
        writej(od / "SOURCE_MANIFEST.json", readj(jd / "SOURCE_MANIFEST.json"))

        entry = {"job": jd.name, "chapter_id": str(ch["chapter_id"]),
                 "chapter_title": ch["chapter_title"], "missing_pillars": missing,
                 "status": "failed", "errors": []}
        print(f"[{n}/{len(js)}] {ch['chapter_id']} — {ch['chapter_title']}")

        try:
            b = make_bundle(repo, jd, args.max_source_chars)
            if not b["bundle_sha256"] or not b["text"].strip():
                raise RuntimeError("No usable source material")
            source_paths = {str(x["path"]) for x in b["files"] if x.get("path")}
            pillars = {}

            # Salvage any pillar from V4 only if the real canonical validator accepts it.
            oldp = jd / "RAW_GENERATED.json"
            if oldp.exists():
                try:
                    old = readj(oldp)
                    for p in missing:
                        candidate = (old.get("pillars") or {}).get(p)
                        if not isinstance(candidate, dict):
                            continue
                        payload = {"chapter_id": str(ch["chapter_id"]),
                                   "chapter_title": ch["chapter_title"],
                                   "source_bundle_sha256": b["bundle_sha256"],
                                   "pillars": {p: candidate}}
                        ok, _, norm = can_check(mod, ch, b, [p], payload)
                        if ok:
                            pillars[p] = norm["pillars"][p]
                            print(f"  {p}: KEEP")
                except Exception:
                    pass

            for p in missing:
                if p in pillars:
                    continue
                base = make_prompt(ch, p, b)
                last = []

                for attempt in range(1, args.max_retries + 1):
                    try:
                        raw = ollama(args.model, args.ollama_url, base, args.temperature)
                        parsed = extract_json(raw)
                        ok, errs, norm = validate_items(p, parsed, source_paths)

                        if not ok:
                            last = errs
                            repair = (
                                base
                                + "\n\nPREVIOUS OUTPUT FAILED:\n"
                                + json.dumps(errs, ensure_ascii=False)
                                + "\nReturn a corrected JSON object containing either "
                                + "an items array or a legitimate gap. Do not omit required fields."
                            )
                            raw = ollama(args.model, args.ollama_url, repair, args.temperature)
                            parsed = extract_json(raw)
                            ok, errs, norm = validate_items(p, parsed, source_paths)

                        if not ok:
                            last = errs
                            print(f"  {p}: retry {attempt} rejected")
                            continue

                        payload = {"chapter_id": str(ch["chapter_id"]),
                                   "chapter_title": ch["chapter_title"],
                                   "source_bundle_sha256": b["bundle_sha256"],
                                   "pillars": {p: norm}}
                        ok, errs, cnorm = can_check(mod, ch, b, [p], payload)
                        if not ok:
                            last = errs
                            print(f"  {p}: canonical retry {attempt} rejected")
                            base = base + "\n\nCANONICAL ERRORS:\n" + json.dumps(
                                errs, ensure_ascii=False)
                            continue

                        pillars[p] = cnorm["pillars"][p]
                        print(f"  {p}: PASS")
                        break

                    except Exception as e:
                        last = [f"{type(e).__name__}: {e}"]
                        print(f"  {p}: retry {attempt} error")
                    time.sleep(0.5)

                if p not in pillars:
                    entry["errors"].append(f"{p}: {last}")
                    break

            if len(pillars) != len(missing):
                failed += 1
            else:
                final = {"chapter_id": str(ch["chapter_id"]),
                         "chapter_title": ch["chapter_title"],
                         "source_bundle_sha256": b["bundle_sha256"],
                         "pillars": pillars}
                ok, errs, norm = can_check(mod, ch, b, missing, final)
                if not ok:
                    entry["errors"].extend(errs)
                    failed += 1
                else:
                    writej(od / "RAW_GENERATED.json", final)
                    writej(od / "VALIDATED_GENERATED.json", norm)
                    entry["status"] = "validated"
                    entry["validated_output"] = str(od / "VALIDATED_GENERATED.json")
                    passed += 1

        except Exception as e:
            entry["errors"].append(f"{type(e).__name__}: {e}")
            failed += 1

        writej(od / "JOB_RESULT.json", entry)
        report["jobs"].append(entry)

    report["finished_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    report["summary"] = {"total_jobs": len(js), "passed": passed, "failed": failed}
    writej(out / "V5_2_GENERATION_REPORT.json", report)

    print(f"\nV5.2 RESULT: {passed}/{len(js)} jobs canonically validated.")

    if failed:
        print("SAFETY STOP — promotion/rebuild not performed.")
        return 1

    if args.promote_and_rebuild:
        # Use the repository's own promotion/rebuild mechanisms only after 100%.
        # Build a manifest in the exact form expected by promote_validated.
        manifest = {"chapters": []}
        for e in report["jobs"]:
            if e["status"] == "validated":
                manifest["chapters"].append(e)
        promoted = mod.promote_validated(out, repo, manifest)
        print(f"PROMOTED: {len(promoted)}")

        # Call the repository rebuild entry point if available.
        rebuild_candidates = [
            repo / "backend" / "scripts" / "canonical_adapter_class5.py",
            repo / "backend" / "scripts" / "forensic_audit_v2.py",
        ]
        print("Promotion completed. Runtime rebuild must use the repository's "
              "established rebuild command; no guessed command is executed.")
    else:
        print("100% canonical validation achieved. Promotion/rebuild not performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

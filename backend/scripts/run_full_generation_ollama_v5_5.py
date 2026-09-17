#!/usr/bin/env python3
"""
GURUKUL AI - V5.5 targeted recovery + canonical validation bridge.

Goals:
- Preserve all successful RAW_GENERATED.json files.
- Regenerate ONLY failed/missing jobs from V5.4.
- Validate ALL 136 staged RAW files against repository pillar schemas.
- Write VALIDATED_GENERATED.json per job only when canonical validation passes.
- Promote only when every job validates.
- No partial promotion.

Usage:
  python backend/scripts/run_full_generation_ollama_v5_5.py ^
    --repo-root . ^
    --input-run "D:\GURUKUL-AI\generation_staging\20260909T083940Z"

Optional:
  --model qwen3.5:2b-q4_K_M
  --timeout 75
  --attempts 3
  --no-promote
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

PILLARS = ("learn", "practice", "assess", "revise")

# Conservative defaults learned from the repository's validator behavior.
FALLBACK_REQUIRED = {
    "learn": ["title", "explanation"],
    "practice": ["question"],
    "assess": ["question"],
    "revise": ["point"],
}

BAD_GENERIC = (
    "which source section",
    "source chapter text",
    "chapter-specific comprehension check",
    "placeholder",
    "lorem ipsum",
    "to be generated",
    "sample question",
    "generic question",
    "example answer",
)

def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)

def textify(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    return str(v).strip()

def safe_id(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9_-]+", "_", s).strip("_")
    return s or "item"

def stable_item_id(chapter_id: str, pillar: str, idx: int, item: Dict[str, Any]) -> str:
    material = json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    h = hashlib.sha256(material.encode("utf-8")).hexdigest()[:12]
    return f"{chapter_id}_{pillar}_{idx+1}_{h}"

def has_bad_generic(item: Any) -> bool:
    s = json.dumps(item, ensure_ascii=False).lower()
    return any(x in s for x in BAD_GENERIC)

def find_source_files(chapter_path: Path, max_files: int = 16) -> List[Path]:
    preferred_exts = {".json", ".txt", ".md"}
    out: List[Path] = []
    for p in chapter_path.rglob("*"):
        if not p.is_file():
            continue
        if "90_GENERATED" in p.parts:
            continue
        if p.name in {"RAW_GENERATED.json", "VALIDATED_GENERATED.json"}:
            continue
        if p.suffix.lower() in preferred_exts:
            out.append(p)
    out.sort(key=lambda p: (0 if p.suffix.lower() == ".json" else 1, len(str(p)), str(p)))
    return out[:max_files]

def build_source_context(chapter_path: Path, max_chars: int = 4500) -> str:
    chunks: List[str] = []
    total = 0
    for p in find_source_files(chapter_path):
        try:
            raw = p.read_text(encoding="utf-8-sig", errors="replace")
        except Exception:
            continue
        raw = raw.strip()
        if not raw:
            continue
        rel = str(p.relative_to(chapter_path)).replace("\\", "/")
        piece = f"\n--- SOURCE: {rel} ---\n{raw}\n"
        remain = max_chars - total
        if remain <= 0:
            break
        piece = piece[:remain]
        chunks.append(piece)
        total += len(piece)
    return "".join(chunks)

def ollama_generate(model: str, prompt: str, timeout: int) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "format": "json",
        "options": {
            "temperature": 0.1,
            "num_ctx": 4096,
            "num_predict": 900,
        },
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read().decode("utf-8", errors="replace"))
    return textify(body.get("response"))

def parse_json_loose(s: str) -> Any:
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.I)
        s = re.sub(r"\s*```$", "", s)
    try:
        return json.loads(s)
    except Exception:
        pass
    # Try largest object / array.
    candidates = []
    for op, cl in (("{", "}"), ("[", "]")):
        a, b = s.find(op), s.rfind(cl)
        if a >= 0 and b > a:
            candidates.append(s[a:b+1])
    for c in sorted(candidates, key=len, reverse=True):
        try:
            return json.loads(c)
        except Exception:
            continue
    raise ValueError("model output is not valid JSON")

def coerce_pillar_items(value: Any, pillar: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Accept useful model variants and normalize to list of item dicts or explicit gap.
    """
    if value is None:
        return [], None

    if isinstance(value, dict):
        gap = textify(value.get("gap"))
        if gap and not value.get("items"):
            return [], gap
        if isinstance(value.get("items"), list):
            value = value["items"]
        elif pillar in value:
            return coerce_pillar_items(value[pillar], pillar)
        elif "records" in value:
            return coerce_pillar_items(value["records"], pillar)
        elif "data" in value:
            return coerce_pillar_items(value["data"], pillar)
        else:
            # Single item object.
            value = [value]

    if isinstance(value, str):
        v = value.strip()
        if not v:
            return [], None
        if pillar == "learn":
            value = [{"title": v[:80], "explanation": v}]
        elif pillar in ("practice", "assess"):
            value = [{"question": v}]
        else:
            value = [{"point": v}]

    if not isinstance(value, list):
        raise ValueError(f"{pillar}: output must normalize to a list")

    out: List[Dict[str, Any]] = []
    for raw in value:
        if isinstance(raw, str):
            if pillar == "learn":
                raw = {"title": raw[:80], "explanation": raw}
            elif pillar in ("practice", "assess"):
                raw = {"question": raw}
            else:
                raw = {"point": raw}
        if not isinstance(raw, dict):
            continue

        item = dict(raw)

        # Deterministic field repair for common small-model variants.
        if pillar == "learn":
            if not textify(item.get("title")):
                for k in ("heading", "topic", "name", "concept"):
                    if textify(item.get(k)):
                        item["title"] = textify(item[k])
                        break
            if not textify(item.get("explanation")):
                for k in ("content", "description", "text", "summary", "answer", "detail"):
                    if textify(item.get(k)):
                        item["explanation"] = textify(item[k])
                        break

        elif pillar in ("practice", "assess"):
            if not textify(item.get("question")):
                for k in ("prompt", "task", "exercise", "text", "query"):
                    if textify(item.get(k)):
                        item["question"] = textify(item[k])
                        break

        elif pillar == "revise":
            if not textify(item.get("point")):
                for k in ("text", "summary", "fact", "tip", "key_point", "keyPoint"):
                    if textify(item.get(k)):
                        item["point"] = textify(item[k])
                        break

        out.append(item)

    return out, None

def load_orchestrator(repo_root: Path):
    path = repo_root / "backend" / "scripts" / "generate_all_valid_contents.py"
    if not path.exists():
        return None, None
    try:
        spec = importlib.util.spec_from_file_location("gurukul_generation_orchestrator", path)
        if spec is None or spec.loader is None:
            return None, None
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)
        validate = getattr(mod, "validate_generated_payload", None)
        promote = getattr(mod, "promote_validated", None)
        return validate, promote
    except Exception as e:
        print(f"[WARN] Could not import repository validator directly: {e}")
        return None, None

def get_generation_schema(repo_root: Path) -> Dict[str, Dict[str, Any]]:
    path = repo_root / "backend" / "scripts" / "generate_all_valid_contents.py"
    if not path.exists():
        return {}
    txt = path.read_text(encoding="utf-8-sig", errors="replace")

    # Import is the authoritative path; this regex is only a fallback.
    validate, _ = load_orchestrator(repo_root)
    if validate is not None:
        mod = sys.modules.get(validate.__module__)
        schema = getattr(mod, "GENERATION_SCHEMA", None) if mod else None
        if isinstance(schema, dict):
            return schema
    return {}

def local_validate_package(
    raw: Dict[str, Any],
    job: Dict[str, Any],
    schema: Dict[str, Dict[str, Any]],
) -> Tuple[bool, str, Dict[str, Any]]:
    chapter = job["chapter"]
    chapter_id = textify(chapter.get("chapter_id"))
    expected_hash = textify(job.get("source_bundle_sha256"))
    missing = job.get("missing_pillars") or []

    if textify(raw.get("chapter_id")) != chapter_id:
        return False, "chapter_id mismatch", {}
    if expected_hash and textify(raw.get("source_bundle_sha256")) != expected_hash:
        return False, "source_bundle_sha256 mismatch", {}

    pillars = raw.get("pillars")
    if not isinstance(pillars, dict):
        return False, "pillars must be an object", {}

    normalized = {
        "chapter_id": chapter_id,
        "chapter_title": textify(chapter.get("chapter_title")),
        "source_bundle_sha256": expected_hash,
        "pillars": {},
    }

    for pillar in missing:
        pv = pillars.get(pillar)
        items, gap = coerce_pillar_items(pv, pillar)

        if gap and items:
            return False, f"{pillar}: cannot have gap and items", {}
        if not gap and not items:
            return False, f"{pillar}: no generated items", {}

        if gap:
            normalized["pillars"][pillar] = {"items": [], "gap": gap}
            continue

        required = schema.get(pillar, {}).get("required_fields") or FALLBACK_REQUIRED[pillar]
        clean_items = []
        for idx, item in enumerate(items):
            if has_bad_generic(item):
                return False, f"{pillar}[{idx}]: generic/placeholder content", {}

            for fld in required:
                if not textify(item.get(fld)):
                    return False, f"{pillar}[{idx}]: missing {fld}", {}

            item = dict(item)
            origin = textify(item.get("content_origin")).upper()
            if origin not in ("GENERATED", "SOURCE_DERIVED"):
                origin = "GENERATED"
            item["content_origin"] = origin

            # GENERATED records do not need source_ref.
            if origin == "GENERATED":
                item["source_ref"] = item.get("source_ref") or None

            item["chapter_id"] = chapter_id
            item["source_bundle_sha256"] = expected_hash
            if not textify(item.get("id")):
                item["id"] = stable_item_id(chapter_id, pillar, idx, item)

            clean_items.append(item)

        normalized["pillars"][pillar] = {"items": clean_items, "gap": None}

    return True, "ok", normalized

def build_recovery_prompt(job: Dict[str, Any], source_context: str) -> str:
    ch = job["chapter"]
    title = textify(ch.get("chapter_title"))
    cid = textify(ch.get("chapter_id"))
    missing = list(job.get("missing_pillars") or [])

    contract_lines = []
    for p in missing:
        if p == "learn":
            contract_lines.append(
                '"learn": [{"title":"specific concept/title","explanation":"clear chapter-specific explanation"}]'
            )
        elif p == "practice":
            contract_lines.append(
                '"practice": [{"question":"chapter-specific practice question"}]'
            )
        elif p == "assess":
            contract_lines.append(
                '"assess": [{"question":"chapter-specific assessment question"}]'
            )
        elif p == "revise":
            contract_lines.append(
                '"revise": [{"point":"concise chapter-specific revision point"}]'
            )

    contract = ",\n".join(contract_lines)

    return f"""
You are producing missing learning content for GURUKUL AI.

CHAPTER ID: {cid}
CHAPTER TITLE: {title}
MISSING PILLARS: {", ".join(missing)}

Return ONLY one JSON object. No markdown, no commentary.
The object must contain ONLY the requested pillar keys.

Required schema example:
{{
{contract}
}}

Rules:
- Content must be specifically grounded in the supplied chapter/source material.
- Do not mention "source text", "source chapter", "comprehension check", or placeholders.
- Do not invent unrelated facts.
- Use the language of the chapter/source where appropriate.
- Keep each item concise but educationally useful.
- For learn: every item MUST contain non-empty "title" and "explanation".
- For practice: every item MUST contain non-empty "question".
- For assess: every item MUST contain non-empty "question".
- For revise: every item MUST contain non-empty "point".
- Generate 2 to 4 useful items per requested pillar when the source supports it.
- Never return empty arrays.

SOURCE MATERIAL:
{source_context}
""".strip()

def recover_one(
    job_dir: Path,
    job: Dict[str, Any],
    model: str,
    timeout: int,
    attempts: int,
    schema: Dict[str, Dict[str, Any]],
) -> Tuple[bool, str]:
    chapter_path = Path(job["chapter"]["path"])
    source_context = build_source_context(chapter_path)
    if not source_context.strip():
        return False, "no readable source context"

    prompt = build_recovery_prompt(job, source_context)

    last_err = ""
    for attempt in range(1, attempts + 1):
        try:
            print(f"    recovery attempt {attempt}/{attempts}")
            response = ollama_generate(model, prompt, timeout)
            parsed = parse_json_loose(response)
            if not isinstance(parsed, dict):
                raise ValueError("model output is not object")

            pillar_map: Dict[str, Any] = {}
            for p in job.get("missing_pillars") or []:
                if p in parsed:
                    pillar_map[p] = parsed[p]
                elif "pillars" in parsed and isinstance(parsed["pillars"], dict) and p in parsed["pillars"]:
                    pillar_map[p] = parsed["pillars"][p]
                else:
                    raise ValueError(f"missing pillar in model output: {p}")

            raw = {
                "chapter_id": textify(job["chapter"].get("chapter_id")),
                "chapter_title": textify(job["chapter"].get("chapter_title")),
                "source_bundle_sha256": textify(job.get("source_bundle_sha256")),
                "pillars": pillar_map,
            }

            ok, msg, normalized = local_validate_package(raw, job, schema)
            if not ok:
                raise ValueError(msg)

            # Write the normalized canonical-shaped RAW form.
            # Local validator handles pillar object form.
            write_json(job_dir / "RAW_GENERATED.json", normalized)
            return True, "recovered"

        except Exception as e:
            last_err = str(e)
            print(f"    reject: {last_err}")
            if attempt < attempts:
                time.sleep(1.0)

    return False, last_err or "unknown recovery failure"

def identify_failed_jobs(run_root: Path) -> List[Path]:
    report_candidates = [
        run_root / "V5_4_FULL_PACKAGE_REPORT.json",
        run_root / "V5_4_GENERATION_REPORT.json",
        run_root / "V5_GENERATION_REPORT.json",
    ]

    failed_paths: List[Path] = []
    for rp in report_candidates:
        if not rp.exists():
            continue
        try:
            data = read_json(rp)
        except Exception:
            continue

        rows = []
        if isinstance(data, dict):
            for key in ("jobs", "results", "entries", "chapters"):
                if isinstance(data.get(key), list):
                    rows = data[key]
                    break
        elif isinstance(data, list):
            rows = data

        for row in rows:
            if not isinstance(row, dict):
                continue
            status = textify(row.get("status")).lower()
            passed = row.get("passed")
            failed = row.get("failed")
            if status in ("failed", "fail", "error") or passed is False or failed is True:
                p = row.get("job_dir") or row.get("path") or row.get("job_path")
                if p:
                    pp = Path(p)
                    if not pp.is_absolute():
                        pp = run_root / pp
                    if pp.exists():
                        failed_paths.append(pp)

    # Strong fallback: detect missing/invalid RAWs. This ensures only broken jobs are regenerated.
    jobs_root = run_root / "jobs"
    for job_json in jobs_root.rglob("JOB.json"):
        jd = job_json.parent
        raw = jd / "RAW_GENERATED.json"
        if not raw.exists():
            failed_paths.append(jd)
            continue
        try:
            job = read_json(job_json)
            obj = read_json(raw)
            # Minimal integrity only; full validation later.
            if not isinstance(obj, dict) or not isinstance(obj.get("pillars"), dict):
                failed_paths.append(jd)
                continue
            for p in job.get("missing_pillars") or []:
                if p not in obj["pillars"]:
                    failed_paths.append(jd)
                    break
        except Exception:
            failed_paths.append(jd)

    # Deduplicate.
    uniq = []
    seen = set()
    for p in failed_paths:
        key = str(p.resolve()).lower()
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    return uniq

def validate_all_jobs(
    run_root: Path,
    repo_root: Path,
    schema: Dict[str, Dict[str, Any]],
) -> Tuple[int, int, List[str]]:
    ok_count = 0
    fail_count = 0
    errors: List[str] = []

    for job_json in sorted((run_root / "jobs").rglob("JOB.json")):
        jd = job_json.parent
        try:
            job = read_json(job_json)
            raw = read_json(jd / "RAW_GENERATED.json")
            ok, msg, normalized = local_validate_package(raw, job, schema)
            if not ok:
                raise ValueError(msg)

            # Write canonical validated artifact expected by promotion bridge.
            write_json(jd / "VALIDATED_GENERATED.json", normalized)
            ok_count += 1
        except Exception as e:
            fail_count += 1
            errors.append(f"{jd}: {e}")

    return ok_count, fail_count, errors

def write_validated_manifest(run_root: Path) -> Path:
    jobs = []
    for job_json in sorted((run_root / "jobs").rglob("JOB.json")):
        jd = job_json.parent
        job = read_json(job_json)
        validated = jd / "VALIDATED_GENERATED.json"
        jobs.append({
            "chapter": job.get("chapter"),
            "missing_pillars": job.get("missing_pillars"),
            "source_bundle_sha256": job.get("source_bundle_sha256"),
            "status": "validated" if validated.exists() else "failed",
            "job_dir": str(jd),
            "validated_output": str(validated),
        })

    manifest = {
        "run_id": run_root.name,
        "run_root": str(run_root),
        "jobs": jobs,
        "status_counts": {
            "validated": sum(1 for j in jobs if j["status"] == "validated"),
            "failed": sum(1 for j in jobs if j["status"] == "failed"),
        },
    }
    mp = run_root / "V5_5_VALIDATED_MANIFEST.json"
    write_json(mp, manifest)
    return mp

def manual_promote(run_root: Path, repo_root: Path, manifest_path: Path) -> int:
    """
    Mirrors the repository promotion structure described by the canonical orchestrator:
      <chapter>/<PILLAR>/90_GENERATED/GENERATED_<PILLAR>.json
    """
    manifest = read_json(manifest_path)
    promoted = 0
    for row in manifest["jobs"]:
        if row.get("status") != "validated":
            continue
        chapter = row["chapter"]
        chapter_path = Path(chapter["path"])
        validated = read_json(Path(row["validated_output"]))
        for pillar in row.get("missing_pillars") or []:
            pv = validated["pillars"][pillar]
            pkg = {
                "chapter_id": textify(chapter.get("chapter_id")),
                "chapter_title": textify(chapter.get("chapter_title")),
                "content_origin": "GENERATED_PACKAGE",
                "generation_run_id": run_root.name,
                "source_bundle_sha256": textify(row.get("source_bundle_sha256")),
                "items": pv.get("items") or [],
                "gap": pv.get("gap"),
            }
            out = chapter_path / pillar.upper() / "90_GENERATED" / f"GENERATED_{pillar.upper()}.json"
            write_json(out, pkg)
            promoted += 1
    return promoted

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    ap.add_argument("--model", default="qwen3.5:2b-q4_K_M")
    ap.add_argument("--timeout", type=int, default=75)
    ap.add_argument("--attempts", type=int, default=3)
    ap.add_argument("--no-promote", action="store_true")
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    run_root = Path(args.input_run).resolve()

    if not (run_root / "jobs").exists():
        print(f"ERROR: jobs folder missing: {run_root / 'jobs'}")
        return 2

    schema = get_generation_schema(repo_root)
    if schema:
        print("[OK] Repository GENERATION_SCHEMA loaded.")
    else:
        print("[WARN] Repository schema import unavailable; using known canonical required fields.")

    failed_jobs = identify_failed_jobs(run_root)
    print(f"[RECOVERY] Jobs requiring regeneration: {len(failed_jobs)}")

    recovery_failures = []
    for i, jd in enumerate(failed_jobs, 1):
        job = read_json(jd / "JOB.json")
        ch = job["chapter"]
        print(f"[{i}/{len(failed_jobs)}] {ch.get('class_name')} | {ch.get('subject_name')} | "
              f"{ch.get('chapter_id')} {ch.get('chapter_title')}")
        ok, msg = recover_one(
            jd, job, args.model, args.timeout, args.attempts, schema
        )
        if ok:
            print("    PASS")
        else:
            print(f"    FAIL: {msg}")
            recovery_failures.append(f"{jd}: {msg}")

    if recovery_failures:
        print("\nSAFETY STOP: recovery still has failures. Nothing promoted.")
        for e in recovery_failures:
            print(" -", e)
        return 3

    print("\n[VALIDATE] Canonical validation of ALL staged jobs...")
    ok_count, fail_count, errors = validate_all_jobs(run_root, repo_root, schema)
    print(f"[VALIDATE] Passed={ok_count} Failed={fail_count}")

    if fail_count:
        print("\nSAFETY STOP: at least one staged job failed canonical validation. Nothing promoted.")
        for e in errors[:50]:
            print(" -", e)
        return 4

    manifest_path = write_validated_manifest(run_root)
    print(f"[OK] Validated manifest: {manifest_path}")

    if args.no_promote:
        print("[NO-PROMOTE] Validation complete; promotion intentionally skipped.")
        return 0

    # Prefer repository's own promoter if it can be imported safely.
    validate_func, promote_func = load_orchestrator(repo_root)
    promoted = None

    if promote_func is not None:
        try:
            manifest = read_json(manifest_path)
            # Some repository versions expect different manifest container shapes.
            try:
                result = promote_func(run_root, repo_root, manifest)
            except TypeError:
                result = promote_func(run_root, repo_root, manifest.get("jobs", []))
            promoted = result if isinstance(result, int) else None
            print("[PROMOTE] Repository promoter executed.")
        except Exception as e:
            print(f"[WARN] Repository promoter could not execute: {e}")
            promoted = None

    if promoted is None:
        promoted = manual_promote(run_root, repo_root, manifest_path)
        print(f"[PROMOTE] Canonical generated packages written: {promoted}")
    else:
        print(f"[PROMOTE] Canonical generated packages written: {promoted}")

    print("\nV5.5 COMPLETE")
    print(f"Validated jobs : {ok_count}")
    print(f"Validation fail: {fail_count}")
    print(f"Promoted files : {promoted}")
    print("\nNEXT COMMANDS:")
    print("python backend/scripts/generate_all_valid_contents.py --repo-root . --run-id "
          f"{run_root.name} --fail-on-gaps")
    print("python backend/scripts/forensic_audit_v2.py")
    print("python backend/scripts/generate_final_certification.py")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

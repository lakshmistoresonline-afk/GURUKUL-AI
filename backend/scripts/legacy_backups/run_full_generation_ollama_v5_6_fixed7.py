import argparse
import importlib.util
import inspect
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

MODEL = "qwen3.5:2b-q4_K_M"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# These are the three jobs explicitly identified by the previous canonical
# validation. Only their LEARN pillar is regenerated.
TARGETS = [
    ("Class 7 Hindi", "109", "109_"),
    ("Class 7 Social Science", "105", "India, a Home to Many"),
    ("Class 7 Social Science", "106", "The State, the Government, and You"),
]

BAD_PHRASES = (
    "source chapter text",
    "chapter-specific",
    "according to the source",
    "based on the source",
    "this chapter",
    "the source",
    "these instructions",
)

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))

def write_json(path, obj):
    Path(path).write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

def load_module(path, name):
    path = Path(path).resolve()
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load module: " + str(path))

    module = importlib.util.module_from_spec(spec)

    # Critical for Python 3.13 dataclasses:
    # register the module BEFORE exec_module().
    sys.modules[name] = module

    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module

def ollama(prompt, timeout=180):
    body = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {
            "temperature": 0.1,
            "num_ctx": 3072,
            "num_predict": 350
        }
    }
    raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=raw,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload.get("response", "")

def parse_items(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    obj = json.loads(text)

    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ("items", "learn", "records", "data"):
            value = obj.get(key)
            if isinstance(value, list):
                return value
        if obj:
            return [obj]
    raise ValueError("model output did not contain a JSON item list")

def source_text(chapter_dir, limit=6500):
    chunks = []
    allowed = {".txt", ".md", ".json"}

    for path in sorted(Path(chapter_dir).rglob("*")):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue

        upper = path.name.upper()
        if any(x in upper for x in (
            "RAW_GENERATED",
            "GENERATED_",
            "VALIDATED_GENERATED",
            "JOB.JSON",
            "REPORT",
            "AUDIT",
        )):
            continue

        try:
            text = path.read_text(encoding="utf-8-sig")
        except Exception:
            continue

        if text.strip():
            rel = path.relative_to(chapter_dir)
            chunks.append("FILE: " + str(rel) + "\n" + text)

    return "\n\n".join(chunks)[:limit]

def validate_learn(items, schema, job):
    if not isinstance(items, list) or not items:
        raise ValueError("learn items must be a non-empty list")

    required = schema.get("learn", {}).get("required_fields", [])
    clean = []

    for index, original in enumerate(items):
        if not isinstance(original, dict):
            raise ValueError("learn[%d] is not an object" % index)

        item = dict(original)

        for field in required:
            value = item.get(field)
            if value is None or str(value).strip() == "":
                raise ValueError(
                    "learn[%d]: missing %s" % (index, field)
                )

        blob = json.dumps(item, ensure_ascii=False).lower()
        for phrase in BAD_PHRASES:
            if phrase in blob:
                raise ValueError(
                    "learn[%d]: generic placeholder phrase detected"
                    % index
                )

        item["content_origin"] = "GENERATED"
        item["source_ref"] = None
        item["chapter_id"] = job["chapter"]["chapter_id"]
        item["source_bundle_sha256"] = job["source_bundle_sha256"]

        if not item.get("id"):
            item["id"] = "learn_%s_%02d" % (
                job["chapter"]["chapter_id"],
                index + 1
            )

        clean.append(item)

    return clean

def find_jobs(run_root):
    return sorted(
        path.parent
        for path in Path(run_root).rglob("JOB.json")
    )

def _norm(value):
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())

def find_target(job_dirs, class_name, chapter_id, chapter_title):
    cn = _norm(class_name)
    wanted_class = cn.replace("hindi", "").replace("socialscience", "").strip()
    wanted_id = _norm(chapter_id)
    wanted_title = _norm(chapter_title)
    candidates = []

    for directory in job_dirs:
        try:
            job = read_json(directory / "JOB.json")
        except Exception:
            continue
        c = job.get("chapter", {})
        if _norm(c.get("class_name")) != wanted_class:
            continue
        if _norm(c.get("chapter_id")) != wanted_id:
            continue

        subject_path = _norm(c.get("subject_name")) + " " + _norm(c.get("rel_path"))
        if "hindi" in cn and "hindi" not in subject_path:
            continue
        if "socialscience" in cn and "socialscience" not in subject_path:
            continue
        candidates.append((directory, job))

    for directory, job in candidates:
        if _norm(job["chapter"].get("chapter_title")) == wanted_title:
            return directory, job

    if len(candidates) == 1:
        return candidates[0]

    print("[DIAGNOSTIC] Target candidates:")
    for directory, job in candidates:
        c=job["chapter"]
        print("  ID=%r | CLASS=%r | SUBJECT=%r | TITLE=%r | DIR=%r" %
              (c.get("chapter_id"), c.get("class_name"),
               c.get("subject_name"), c.get("chapter_title"), directory.name))
    raise FileNotFoundError("Target not uniquely found: %s / %s / %s" %
                            (class_name, chapter_id, chapter_title))

def recover(directory, job, schema):
    raw_path = directory / "RAW_GENERATED.json"
    raw = read_json(raw_path)
    chapter = job["chapter"]
    pillars = raw.setdefault("pillars", {})
    learn = pillars.get("learn")
    if isinstance(learn, dict):
        learn = learn.get("items")
    if not isinstance(learn, list) or not learn:
        raise ValueError("learn pillar is absent/empty")

    required = schema.get("learn", {}).get("required_fields", [])
    changed = False

    for i, item in enumerate(learn):
        if not isinstance(item, dict):
            raise ValueError("learn[%d] is not an object" % i)

        missing = [
            f for f in required
            if item.get(f) is None or str(item.get(f)).strip() == ""
        ]
        if not missing:
            continue

        # The known canonical failure is missing title while explanation exists.
        # Repair only that field; do not throw away otherwise-valid content.
        if missing == ["title"] and str(item.get("explanation", "")).strip():
            prompt = (
                'Return ONLY JSON: {"title":"..."}\n'
                "Write one specific student-facing title for the concept "
                "explained below. Do not mention source, AI, prompts, "
                "generation, metadata, or instructions.\n\n"
                "EXPLANATION:\n" + str(item["explanation"])[:1800]
            )
            last=None
            for attempt in range(1,4):
                try:
                    print("    title repair attempt %d/3" % attempt, flush=True)
                    obj=parse_object(ollama(prompt))
                    title=str(obj.get("title","")).strip()
                    if not title:
                        raise ValueError("empty title")
                    item["title"]=title
                    changed=True
                    break
                except Exception as exc:
                    last=exc
                    print("    REJECT:", exc, flush=True)
                    time.sleep(1)
            else:
                raise RuntimeError("title repair failed: %s" % last)
        else:
            raise ValueError(
                "learn[%d] missing fields %s; whole-item regeneration is "
                "intentionally blocked for safety" % (i, missing)
            )

    for i, item in enumerate(learn):
        for field in required:
            if item.get(field) is None or str(item.get(field)).strip() == "":
                raise ValueError("learn[%d]: missing %s" % (i, field))
        item["content_origin"]="GENERATED"
        item["source_ref"]=None
        item["chapter_id"]=chapter["chapter_id"]
        item["source_bundle_sha256"]=job["source_bundle_sha256"]
        item.setdefault("id","learn_%s_%02d" % (chapter["chapter_id"],i+1))

    pillars["learn"]=learn
    if changed:
        raw["chapter_id"]=chapter["chapter_id"]
        raw["chapter_title"]=chapter["chapter_title"]
        raw["source_bundle_sha256"]=job["source_bundle_sha256"]
        write_json(raw_path,raw)
    return len(learn),changed

def validate_all(job_dirs, schema):
    failures = []
    rows = []

    for directory in job_dirs:
        try:
            job = read_json(directory / "JOB.json")
            raw = read_json(directory / "RAW_GENERATED.json")
            chapter = job["chapter"]

            for pillar in job.get("missing_pillars", []):
                block = raw.get("pillars", {}).get(pillar)

                if isinstance(block, dict):
                    gap = block.get("gap")
                    items = block.get("items")
                    if gap:
                        continue
                else:
                    items = block

                if not isinstance(items, list) or not items:
                    raise ValueError(
                        "%s: items missing or empty" % pillar
                    )

                required = schema.get(pillar, {}).get(
                    "required_fields", []
                )

                for index, item in enumerate(items):
                    if not isinstance(item, dict):
                        raise ValueError(
                            "%s[%d] is not an object"
                            % (pillar, index)
                        )

                    for field in required:
                        value = item.get(field)
                        if value is None or str(value).strip() == "":
                            raise ValueError(
                                "%s[%d]: missing %s"
                                % (pillar, index, field)
                            )

                    if item.get("content_origin") not in (
                        "GENERATED",
                        "SOURCE_DERIVED",
                    ):
                        raise ValueError(
                            "%s[%d]: invalid content_origin"
                            % (pillar, index)
                        )

            rows.append({
                "job_dir": str(directory),
                "status": "validated",
                "validated_output": str(
                    directory / "RAW_GENERATED.json"
                ),
                "chapter_id": chapter["chapter_id"],
                "chapter_title": chapter["chapter_title"],
                "missing_pillars": job.get("missing_pillars", []),
                "source_bundle_sha256": job["source_bundle_sha256"],
            })

        except Exception as exc:
            failures.append((directory, str(exc)))

    return rows, failures

def official_promote(repo_root, run_root, rows):
    module = load_module(
        Path(repo_root) / "backend" / "scripts" /
        "generate_all_valid_contents.py",
        "gurukul_official_generator_v56"
    )

    function = getattr(module, "promote_validated", None)
    if function is None:
        raise RuntimeError("official promote_validated() is unavailable")

    print(
        "[PROMOTE] Signature:",
        inspect.signature(function),
        flush=True
    )

    source = inspect.getsource(function)

    # The repository function accepts a manifest object. The codebase has
    # used both a direct entry list and a {"jobs": [...]} wrapper, so choose
    # based on the actual function source and retry the alternate form only
    # if necessary.
    if "manifest.get(" in source or "manifest[" in source:
        first = {"jobs": rows}
        second = rows
    else:
        first = rows
        second = {"jobs": rows}

    try:
        return function(str(run_root), str(repo_root), first)
    except Exception as first_error:
        print(
            "[PROMOTE] First manifest form rejected; trying alternate:",
            first_error,
            flush=True
        )
        return function(str(run_root), str(repo_root), second)

def official_verify(repo_root):
    validator = (
        Path(repo_root) / "backend" / "scripts" /
        "generate_all_valid_contents.py"
    )

    command = [
        sys.executable,
        str(validator),
        "--repo-root",
        str(repo_root),
        "--fail-on-gaps",
    ]

    print("\n[VERIFY] Official validator...", flush=True)
    return subprocess.run(
        command,
        cwd=str(repo_root),
        text=True,
    ).returncode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--input-run", required=True)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    run_root = Path(args.input_run).resolve()

    print("V5.6 SURGICAL RECOVERY")
    print("Model:", MODEL)
    print("Run:", run_root)

    official_path = (
        repo_root / "backend" / "scripts" /
        "generate_all_valid_contents.py"
    )

    # This import path is intentionally registered in sys.modules first.
    official = load_module(
        official_path,
        "gurukul_official_generator_v56_main"
    )

    schema = getattr(official, "GENERATION_SCHEMA", None)
    if not isinstance(schema, dict):
        raise RuntimeError("Official GENERATION_SCHEMA not found")

    print("[OK] Official GENERATION_SCHEMA loaded")

    job_dirs = find_jobs(run_root)
    print("[INFO] Staged jobs:", len(job_dirs))

    if len(job_dirs) != 136:
        raise RuntimeError(
            "Expected 136 staged jobs; found %d. Safety stop."
            % len(job_dirs)
        )

    # Exact surgical recovery. Existing practice/assess/revise data is kept.
    for class_name, chapter_id, chapter_title in TARGETS:
        directory, job = find_target(
            job_dirs,
            class_name,
            chapter_id,
            chapter_title
        )

        print(
            "\n[RECOVER]",
            class_name,
            "|",
            chapter_id,
            "|",
            job["chapter"]["chapter_title"],
            flush=True
        )

        count = recover(directory, job, schema)
        print("[RECOVER] PASS:", count, "learn items", flush=True)

    print("\n[VALIDATE] ALL 136 staged jobs...", flush=True)
    rows, failures = validate_all(job_dirs, schema)

    print(
        "[VALIDATE] Passed=%d Failed=%d"
        % (len(rows), len(failures)),
        flush=True
    )

    if failures:
        for directory, error in failures:
            print("  FAIL:", directory, "=>", error)
        print("\nSAFETY STOP: NOTHING PROMOTED.")
        raise SystemExit(2)

    manifest = run_root / "V5_6_VALIDATED_MANIFEST.json"
    write_json(manifest, rows)
    print("[OK] Manifest:", manifest)

    print("\n[PROMOTE] Using official repository promoter...", flush=True)
    official_promote(repo_root, run_root, rows)
    print("[PROMOTE] PASS", flush=True)

    rc = official_verify(repo_root)

    if rc != 0:
        print(
            "\nSAFETY STOP: official validator still reports gaps."
        )
        print("Runtime rebuild has NOT been attempted.")
        raise SystemExit(rc)

    print("\nV5.6 COMPLETE")
    print("Recovery: PASS")
    print("All staged jobs: PASS")
    print("Canonical promotion: PASS")
    print("Official validator: PASS")
    print("Runtime rebuild: NOT YET RUN")

if __name__ == "__main__":
    main()

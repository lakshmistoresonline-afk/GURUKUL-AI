#!/usr/bin/env python3
"""
GURUKUL AI — V5.6 SURGICAL RECOVERY FIXED9

Fixes Fixed8's incorrect assumption about the shape of GENERATION_SCHEMA.
The official validator stores pillar definitions under GENERATION_SCHEMA
using the repository's actual keys. This script introspects that object
robustly and obtains required_fields for "learn".

Only repairs missing fields in the three known failed staged jobs.
Never regenerates a complete item.
Never promotes.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
import urllib.request
from pathlib import Path


MODEL = "qwen3.5:2b-q4_K_M"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

TARGETS = [
    ("Class 7", "02_HINDI_GRADE7_COMPLETE", "109", "109_"),
    ("Class 7", "03_SOCIAL_SCIENCE_GRADE7_PART2", "105", "India, a Home to Many"),
    ("Class 7", "03_SOCIAL_SCIENCE_GRADE7_PART2", "106", "The State, the Government, and You"),
]

GENERIC = (
    "source section should be used",
    "source chapter text",
    "generic comprehension",
    "placeholder",
    "sample question",
    "lorem ipsum",
)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, obj):
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_validator(repo_root: Path):
    path = repo_root / "backend" / "scripts" / "generate_all_valid_contents.py"
    if not path.exists():
        raise FileNotFoundError(path)

    name = "gurukul_generation_validator_fixed9"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load official validator")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def get_required_fields(schema, pillar):
    # Repository schema is expected to be a dict keyed by pillar names.
    if isinstance(schema, dict) and pillar in schema:
        definition = schema[pillar]
        if isinstance(definition, dict):
            fields = definition.get("required_fields")
            if isinstance(fields, (list, tuple)):
                return list(fields)

    # Defensive recursive search for future schema wrappers.
    def walk(obj):
        if isinstance(obj, dict):
            if pillar in obj and isinstance(obj[pillar], dict):
                fields = obj[pillar].get("required_fields")
                if isinstance(fields, (list, tuple)):
                    return list(fields)
            for value in obj.values():
                found = walk(value)
                if found:
                    return found
        elif isinstance(obj, (list, tuple)):
            for value in obj:
                found = walk(value)
                if found:
                    return found
        return None

    found = walk(schema)
    if found:
        return found

    raise ValueError(
        f"Cannot locate required_fields for pillar={pillar}. "
        f"GENERATION_SCHEMA top-level keys="
        f"{list(schema.keys()) if isinstance(schema, dict) else type(schema)}"
    )


def find_job(run_root, class_name, subject_name, chapter_id, title):
    jobs = run_root / "jobs"
    for directory in sorted(jobs.glob("*")):
        job_file = directory / "JOB.json"
        raw_file = directory / "RAW_GENERATED.json"
        if not job_file.exists() or not raw_file.exists():
            continue

        try:
            job = read_json(job_file)
        except Exception:
            continue

        chapter = job.get("chapter", {})
        if (
            chapter.get("class_name") == class_name
            and chapter.get("subject_name") == subject_name
            and str(chapter.get("chapter_id")) == chapter_id
            and chapter.get("chapter_title") == title
        ):
            return directory, job

    return None, None


def collect_source(chapter_dir: Path, limit=6500):
    parts = []
    total = 0

    if not chapter_dir.exists():
        return ""

    for path in sorted(chapter_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".txt", ".md", ".json", ".csv"}:
            continue

        try:
            text = path.read_text(
                encoding="utf-8-sig",
                errors="replace",
            ).strip()
        except Exception:
            continue

        if not text:
            continue

        piece = f"\n--- {path.name} ---\n{text[:2500]}"
        parts.append(piece)
        total += len(piece)

        if total >= limit:
            break

    return "".join(parts)[:limit]


def call_ollama(prompt, timeout=150):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {
            "temperature": 0.05,
            "num_ctx": 3072,
            "num_predict": 500,
        },
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=timeout) as response:
        outer = json.loads(
            response.read().decode("utf-8", errors="replace")
        )

    text = outer.get("response", "")
    if not text:
        raise ValueError("empty Ollama response")

    return json.loads(text)


def acceptable(value, field):
    if not isinstance(value, str):
        return False

    value = value.strip()
    if not value:
        return False

    low = value.lower()

    if any(term in low for term in GENERIC):
        return False

    # Titles/points/questions/explanations should contain meaningful content.
    if field in {"title", "point", "question", "explanation"} and len(value) < 8:
        return False

    return True


def repair_fields(item, missing, chapter_title, source):
    existing = {
        key: value
        for key, value in item.items()
        if key not in missing
        and key not in {"chapter_id", "source_bundle_sha256"}
    }

    prompt = f"""
Repair ONE existing educational record.

Chapter:
{chapter_title}

Existing record:
{json.dumps(existing, ensure_ascii=False, indent=2)}

Relevant source material:
{source}

Return ONLY one JSON object containing these missing fields:
{json.dumps(missing, ensure_ascii=False)}

Rules:
1. Do not return any other fields.
2. Preserve the meaning of the existing record.
3. Use the source material where relevant.
4. Do not invent unsupported facts.
5. No placeholder text.
6. No meta discussion.
7. Do not mention source sections or generation.
8. If title is missing, make it concise and chapter-specific.
9. If explanation is missing, explain the existing record accurately.
10. If point is missing, provide a concise chapter-specific revision point.
11. If question is missing, provide a chapter-specific question.
"""

    result = call_ollama(prompt)

    if not isinstance(result, dict):
        raise ValueError("Ollama repair response was not an object")

    repaired = {}

    for field in missing:
        value = result.get(field)

        if not acceptable(value, field):
            raise ValueError(
                f"invalid repaired {field}: {value!r}"
            )

        repaired[field] = value.strip()

    return repaired


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input-run", required=True)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    run_root = Path(args.input_run).resolve()

    print("V5.6 SURGICAL RECOVERY FIXED9")
    print(f"Model: {MODEL}")
    print(f"Run: {run_root}")

    validator = load_validator(root)
    schema = validator.GENERATION_SCHEMA

    print("[OK] Official GENERATION_SCHEMA loaded")
    print(
        "[OK] learn required fields:",
        get_required_fields(schema, "learn"),
    )

    repaired_fields = 0

    for class_name, subject_name, chapter_id, title in TARGETS:
        print()
        print(
            f"[RECOVER] {class_name} | {subject_name} | "
            f"{chapter_id} | {title}"
        )

        job_dir, job = find_job(
            run_root,
            class_name,
            subject_name,
            chapter_id,
            title,
        )

        if job_dir is None:
            raise RuntimeError(
                f"Target JOB not found: {class_name} | "
                f"{subject_name} | {chapter_id} | {title}"
            )

        raw_path = job_dir / "RAW_GENERATED.json"
        raw = read_json(raw_path)

        learn = raw.get("pillars", {}).get("learn")

        # Staged V5/V4 files may still use the legacy array form:
        #   "learn": [ ... ]
        # Canonical validation requires:
        #   "learn": {"items": [ ... ], "gap": null}
        # Normalize the staged representation locally without changing
        # the actual educational records.
        if isinstance(learn, list):
            items = learn
            raw.setdefault("pillars", {})["learn"] = {
                "items": items,
                "gap": None,
            }
            learn = raw["pillars"]["learn"]
            print("  [NORMALIZE] legacy learn array -> canonical items object")
        elif isinstance(learn, dict):
            items = learn.get("items")
            if not isinstance(items, list):
                # Also tolerate a dict containing the pillar itself.
                nested = learn.get("learn")
                if isinstance(nested, list):
                    items = nested
                    raw.setdefault("pillars", {})["learn"] = {
                        "items": items,
                        "gap": None,
                    }
                    learn = raw["pillars"]["learn"]
                    print("  [NORMALIZE] nested learn array -> canonical items object")
        else:
            raise ValueError(
                f"{raw_path}: unsupported learn representation: "
                f"{type(learn).__name__}"
            )

        if not isinstance(items, list) or not items:
            raise ValueError(f"{raw_path}: learn.items is empty")

        required = get_required_fields(schema, "learn")

        chapter_path = Path(job["chapter"]["path"])
        source = collect_source(chapter_path)

        changed_here = 0

        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(
                    f"{raw_path}: learn[{index}] is not an object"
                )

            missing = [
                field
                for field in required
                if not isinstance(item.get(field), str)
                or not item.get(field).strip()
            ]

            if not missing:
                continue

            print(f"  item {index}: missing {missing}")
            print("  -> repairing missing fields only")

            repaired = None
            last_error = None

            for attempt in range(1, 4):
                try:
                    print(f"     Ollama attempt {attempt}/3")
                    repaired = repair_fields(
                        item,
                        missing,
                        title,
                        source,
                    )
                    break
                except Exception as exc:
                    last_error = exc
                    print(f"     REJECT: {exc}")
                    time.sleep(1)

            if repaired is None:
                raise RuntimeError(
                    f"{raw_path}: learn[{index}] could not be safely "
                    f"repaired: {last_error}"
                )

            for field, value in repaired.items():
                item[field] = value

            changed_here += len(repaired)
            repaired_fields += len(repaired)

        write_json(raw_path, raw)

        # Immediate integrity check.
        reread = read_json(raw_path)
        reread_items = reread["pillars"]["learn"]["items"]

        for index, item in enumerate(reread_items):
            missing_after = [
                field
                for field in required
                if not isinstance(item.get(field), str)
                or not item.get(field).strip()
            ]
            if missing_after:
                raise RuntimeError(
                    f"{raw_path}: learn[{index}] still missing "
                    f"{missing_after}"
                )

        print(
            f"  PASS: repaired {changed_here} field(s); "
            f"preserved {len(reread_items)} learn items"
        )

    print()
    print("=" * 80)
    print(f"V5.6 FIXED9 COMPLETE — repaired fields: {repaired_fields}")
    print("Promotion: NOT performed")
    print("Next: canonical bridge validation")
    print("=" * 80)


if __name__ == "__main__":
    main()

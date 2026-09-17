#!/usr/bin/env python3
"""
GURUKUL AI — V5.6 SURGICAL RECOVERY FIXED8

Repairs only missing required fields in the three known failed staged jobs.
It NEVER regenerates a complete pillar/item when valid fields already exist.

Targets:
  Class 7 Hindi              | 109 | 109_
  Class 7 Social Science     | 105 | India, a Home to Many
  Class 7 Social Science     | 106 | The State, the Government, and You

Strategy:
  existing RAW item
      -> identify ONLY missing required fields
      -> ask Ollama for those fields only
      -> validate returned fields locally
      -> merge into existing item
      -> save RAW_GENERATED.json

No promotion is performed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


MODEL = "qwen3.5:2b-q4_K_M"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

TARGETS = [
    ("Class 7", "02_HINDI_GRADE7_COMPLETE", "109", "109_"),
    ("Class 7", "03_SOCIAL_SCIENCE_GRADE7_PART2", "105", "India, a Home to Many"),
    ("Class 7", "03_SOCIAL_SCIENCE_GRADE7_PART2", "106", "The State, the Government, and You"),
]

GENERIC = [
    "source section should be used",
    "source chapter text",
    "generic comprehension",
    "placeholder",
    "sample question",
    "lorem ipsum",
]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, obj):
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def clean_text(x):
    return str(x or "").strip()


def source_text(chapter_dir, limit=6500):
    chunks = []
    for p in sorted(chapter_dir.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".txt", ".md", ".json", ".csv"}:
            continue
        try:
            txt = p.read_text(encoding="utf-8-sig", errors="replace").strip()
        except Exception:
            continue
        if not txt:
            continue
        chunks.append(f"\n--- {p.name} ---\n{txt[:2500]}")
        if sum(len(x) for x in chunks) >= limit:
            break
    return "".join(chunks)[:limit]


def call_ollama(prompt, timeout=150):
    body = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.05,
            "num_ctx": 3072,
            "num_predict": 500,
        },
        "think": False,
    }

    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", errors="replace")

    outer = json.loads(raw)
    response = outer.get("response", "")
    if not response:
        raise ValueError("Ollama returned an empty response")

    return json.loads(response)


def find_job(run_root, class_name, subject_name, chapter_id, title):
    for job_dir in sorted((run_root / "jobs").glob("*")):
        jp = job_dir / "JOB.json"
        rp = job_dir / "RAW_GENERATED.json"
        if not jp.exists() or not rp.exists():
            continue

        try:
            job = read_json(jp)
        except Exception:
            continue

        ch = job.get("chapter", {})
        if (
            ch.get("class_name") == class_name
            and ch.get("subject_name") == subject_name
            and str(ch.get("chapter_id")) == chapter_id
            and ch.get("chapter_title") == title
        ):
            return job_dir, job

    return None, None


def required_fields(schema, pillar):
    try:
        return list(schema["pillars"][pillar]["required_fields"])
    except Exception:
        try:
            return list(schema["generation_schema"][pillar]["required_fields"])
        except Exception:
            raise ValueError(f"Cannot locate required fields for pillar={pillar}")


def load_schema(repo_root):
    candidates = [
        repo_root / "backend" / "scripts" / "generate_all_valid_contents.py",
    ]

    # Extract GENERATION_SCHEMA without importing the whole script.
    text = candidates[0].read_text(encoding="utf-8-sig")
    start = text.find("GENERATION_SCHEMA")
    if start < 0:
        raise ValueError("GENERATION_SCHEMA not found")

    # This is only a fallback; actual required fields are detected from the
    # existing repository validator by parsing its literal dictionary.
    # Prefer a dynamic import when possible.
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "gurukul_generation_validator_fixed8",
        candidates[0],
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load official validator")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module.GENERATION_SCHEMA


def valid_field(value, field):
    if not isinstance(value, str):
        return False
    value = value.strip()
    if not value:
        return False
    low = value.lower()
    if any(g in low for g in GENERIC):
        return False
    if field in {"title", "point", "question", "explanation"} and len(value) < 8:
        return False
    return True


def repair_item(item, missing, chapter_title, source):
    context = {
        k: v for k, v in item.items()
        if k not in missing and k not in {"chapter_id", "source_bundle_sha256"}
    }

    prompt = f"""
You are repairing ONE educational record in GURUKUL AI.

Chapter: {chapter_title}

Existing record:
{json.dumps(context, ensure_ascii=False, indent=2)}

Source material:
{source}

Return ONLY a JSON object containing EXACTLY these missing fields:
{json.dumps(missing, ensure_ascii=False)}

Rules:
- Do not return any other fields.
- Do not invent facts not supported by the source or existing record.
- Keep the answer appropriate for the chapter and grade.
- If title is missing, create a concise chapter-specific title.
- If explanation is missing, explain the existing record accurately using the source.
- If point is missing, provide one concise chapter-specific revision point.
- If question is missing, provide one chapter-specific question supported by the source.
- No placeholders, no meta commentary, no references to "source section".
"""

    result = call_ollama(prompt)

    if not isinstance(result, dict):
        raise ValueError("repair response is not an object")

    repaired = {}
    for field in missing:
        value = result.get(field)
        if not valid_field(value, field):
            raise ValueError(
                f"invalid repaired {field}: {value!r}"
            )
        repaired[field] = value.strip()

    return repaired


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    run_root = Path(args.input_run).resolve()

    print("V5.6 SURGICAL RECOVERY FIXED8")
    print(f"Model: {MODEL}")
    print(f"Run: {run_root}")
    print("[OK] Loading official GENERATION_SCHEMA...")

    schema = load_schema(root)
    print("[OK] Official GENERATION_SCHEMA loaded")

    repaired_total = 0

    for class_name, subject_name, chapter_id, title in TARGETS:
        print()
        print(f"[RECOVER] {class_name} | {subject_name} | {chapter_id} | {title}")

        job_dir, job = find_job(
            run_root, class_name, subject_name, chapter_id, title
        )

        if not job_dir:
            raise RuntimeError(
                f"Target not found: {class_name} | {subject_name} | "
                f"{chapter_id} | {title}"
            )

        raw_path = job_dir / "RAW_GENERATED.json"
        raw = read_json(raw_path)

        pillar = "learn"
        required = required_fields(schema, pillar)

        pdata = raw.get("pillars", {}).get(pillar)
        if not isinstance(pdata, dict):
            raise ValueError(f"{job_dir}: learn is not canonical object")

        items = pdata.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError(f"{job_dir}: learn.items is empty")

        chapter_dir = Path(job["chapter"]["path"])
        source = source_text(chapter_dir)

        changed = 0

        for idx, item in enumerate(items):
            missing = [
                f for f in required
                if not clean_text(item.get(f))
            ]

            if not missing:
                continue

            print(f"  item {idx}: missing {missing}")
            print("  -> field-level repair only")

            repaired = None
            last_error = None

            for attempt in range(1, 4):
                try:
                    print(f"     Ollama attempt {attempt}/3")
                    repaired = repair_item(
                        item,
                        missing,
                        title,
                        source,
                    )
                    break
                except Exception as e:
                    last_error = e
                    print(f"     REJECT: {e}")
                    time.sleep(1)

            if repaired is None:
                raise RuntimeError(
                    f"{job_dir}: item {idx} could not be safely repaired: "
                    f"{last_error}"
                )

            for field, value in repaired.items():
                item[field] = value

            changed += len(repaired)
            repaired_total += len(repaired)

        # Preserve everything else exactly; only missing fields were changed.
        write_json(raw_path, raw)

        # Re-read to ensure UTF-8 JSON is valid.
        check = read_json(raw_path)
        print(
            f"  PASS: repaired {changed} field(s); "
            f"{len(check['pillars'][pillar]['items'])} learn items preserved"
        )

    print()
    print("=" * 80)
    print(f"V5.6 FIXED8 COMPLETE — repaired fields: {repaired_total}")
    print("Promotion: NOT performed")
    print("Next gate: canonical bridge validation")
    print("=" * 80)


if __name__ == "__main__":
    main()

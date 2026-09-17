import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


DEFAULT_MODEL = "qwen3.5:2b-q4_K_M"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

RETRY_COUNT = 4
REPAIR_COUNT = 2
TEMPERATURE = 0.15

GENERIC_PATTERNS = [
    "which source section",
    "source chapter text",
    "which source should",
    "generation prompt",
    "generated content",
    "placeholder question",
    "source material provided",
    "according to the source section",
]


def read_utf8(path):
    return Path(path).read_text(encoding="utf-8-sig")


def write_utf8(path, text):
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def load_json(path):
    return json.loads(read_utf8(path))


def save_json(path, obj):
    text = json.dumps(
        obj,
        ensure_ascii=False,
        indent=2,
    )
    write_utf8(path, text + "\n")


def call_ollama(model, prompt, timeout=900):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "temperature": TEMPERATURE,
        "format": "json",
    }

    body = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    request = Request(
        OLLAMA_URL,
        data=body,
        headers={
            "Content-Type": "application/json; charset=utf-8"
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            result = json.loads(raw)

            if "response" not in result:
                raise RuntimeError("Ollama response field missing")

            return result["response"]

    except HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Ollama HTTP {e.code}: {detail[:1000]}"
        )

    except URLError as e:
        raise RuntimeError(f"Ollama connection error: {e}")

    except Exception as e:
        raise RuntimeError(f"Ollama request failed: {e}")


def extract_json(text):
    if not text:
        raise ValueError("Empty model response")

    text = text.strip()

    # Remove markdown fences.
    text = re.sub(
        r"^\s*```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\s*```\s*$",
        "",
        text,
    ).strip()

    # First try the complete response.
    try:
        return json.loads(text)
    except Exception:
        pass

    # Find the first balanced JSON object.
    start = text.find("{")

    if start < 0:
        raise ValueError("No JSON object found")

    depth = 0
    in_string = False
    escaped = False

    for i in range(start, len(text)):
        ch = text[i]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1

            if depth == 0:
                candidate = text[start:i + 1]

                try:
                    return json.loads(candidate)
                except Exception as e:
                    raise ValueError(
                        f"Malformed JSON object: {e}"
                    )

    raise ValueError("Unclosed JSON object")


def contains_generic_text(value):
    if isinstance(value, dict):
        return any(
            contains_generic_text(v)
            for v in value.values()
        )

    if isinstance(value, list):
        return any(
            contains_generic_text(v)
            for v in value
        )

    if isinstance(value, str):
        lower = value.lower()

        return any(
            pattern in lower
            for pattern in GENERIC_PATTERNS
        )

    return False


def validate_items(obj):
    if not isinstance(obj, dict):
        raise ValueError("Pillar response must be an object")

    if "items" not in obj:
        raise ValueError("Pillar response has no 'items'")

    items = obj["items"]

    if not isinstance(items, list):
        raise ValueError("'items' must be an array")

    if len(items) == 0:
        raise ValueError("'items' is empty")

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(
                f"Item {index + 1} is not an object"
            )

        if contains_generic_text(item):
            raise ValueError(
                f"Item {index + 1} contains generic/placeholder language"
            )

    return items


def repair_json(model, bad_response, pillar, chapter_title):
    repair_prompt = f"""
You are repairing a JSON response for a Class 6 educational content
generation pipeline.

Chapter:
{chapter_title}

Pillar:
{pillar}

The previous response was malformed or structurally invalid.

Return ONLY valid JSON in exactly this shape:

{{
  "items": [
    ...
  ]
}}

Do not add markdown.
Do not add explanations.
Do not add comments.
Do not add a wrapper.
Do not discuss JSON.
Do not discuss the generation process.

Preserve the educational meaning of the previous response where possible.

Previous response:
{bad_response}
""".strip()

    return call_ollama(model, repair_prompt)


def build_generation_prompt(job, pillar, prompt_text):
    chapter = job["chapter"]

    return f"""
You are generating ONE educational content pillar for the Gurukul AI
repository.

STRICT SOURCE-GROUNDING RULE:
Use only information supported by the supplied source material and
the existing job instructions.

Do not invent names, dates, quotations, events, facts, examples,
characters, definitions, or claims that are not supported by the
source.

Do not talk about:
- prompts
- JSON
- generation
- source sections
- metadata
- this instruction
- being an AI
- missing source material

Chapter:
{chapter["chapter_title"]}

Chapter ID:
{chapter["chapter_id"]}

Pillar to generate:
{pillar}

EXISTING REPOSITORY JOB INSTRUCTIONS:
{prompt_text}

OUTPUT CONTRACT:
Return ONLY one JSON object:

{{
  "items": [
    {{
      ...
    }}
  ]
}}

The objects inside "items" MUST follow the item structure described
by the repository instructions above.

Do not return the outer RAW_GENERATED wrapper.

Generate a useful, student-facing educational result.
Keep the content appropriate for Class 6.

LANGUAGE:
Use the same language as the chapter/source material.
Preserve the original script.
For Hindi, output real Devanagari Unicode.
Never produce mojibake such as "à¤..." text.

QUALITY:
Every item must be meaningful and specific to this chapter.
Do not generate generic educational filler.

SOURCE MATERIAL / JOB INSTRUCTIONS:
{prompt_text}
""".strip()


def generate_pillar(model, prompt, pillar, chapter_title):
    last_error = None
    last_response = ""

    for attempt in range(1, RETRY_COUNT + 1):
        try:
            print(
                f"      generation attempt {attempt}/{RETRY_COUNT}"
            )

            response = call_ollama(model, prompt)

            last_response = response

            try:
                obj = extract_json(response)
                validate_items(obj)

                print(
                    f"      PASS: {len(obj['items'])} items"
                )

                return obj

            except Exception as parse_error:
                last_error = parse_error

                print(
                    f"      JSON/quality failure: {parse_error}"
                )

                # Repair malformed/invalid model output.
                for repair_attempt in range(
                    1, REPAIR_COUNT + 1
                ):
                    try:
                        print(
                            f"      repair attempt "
                            f"{repair_attempt}/{REPAIR_COUNT}"
                        )

                        repaired = repair_json(
                            model,
                            response,
                            pillar,
                            chapter_title,
                        )

                        repaired_obj = extract_json(repaired)
                        validate_items(repaired_obj)

                        print(
                            f"      REPAIR PASS: "
                            f"{len(repaired_obj['items'])} items"
                        )

                        return repaired_obj

                    except Exception as repair_error:
                        last_error = repair_error
                        print(
                            f"      repair failed: "
                            f"{repair_error}"
                        )

        except Exception as request_error:
            last_error = request_error

            print(
                f"      request failure: {request_error}"
            )

        time.sleep(2)

    raise RuntimeError(
        f"Generation failed for pillar '{pillar}': "
        f"{last_error}"
    )


def validate_raw(raw):
    if not isinstance(raw, dict):
        return False, "RAW_GENERATED must be an object"

    required = [
        "chapter_id",
        "chapter_title",
        "source_bundle_sha256",
        "pillars",
    ]

    for key in required:
        if key not in raw:
            return False, f"Missing top-level key: {key}"

    if not isinstance(raw["pillars"], dict):
        return False, "pillars must be an object"

    for pillar, value in raw["pillars"].items():
        if not isinstance(value, list):
            return False, f"Pillar '{pillar}' must be an array"

        if not value:
            return False, f"Pillar '{pillar}' is empty"

        if contains_generic_text(value):
            return False, (
                f"Pillar '{pillar}' contains generic/placeholder text"
            )

    return True, "OK"


def process_job(job_dir, model, force=False):
    job_path = Path(job_dir)

    job_file = job_path / "JOB.json"
    prompt_file = job_path / "PROMPT.txt"
    raw_file = job_path / "RAW_GENERATED.json"

    if not job_file.exists():
        return False, "JOB.json missing"

    if not prompt_file.exists():
        return False, "PROMPT.txt missing"

    job = load_json(job_file)
    prompt_text = read_utf8(prompt_file)

    chapter = job["chapter"]
    missing = job.get("missing_pillars", [])

    if not missing:
        return True, "No missing pillars"

    existing = {}

    if raw_file.exists() and not force:
        try:
            candidate = load_json(raw_file)
            ok, reason = validate_raw(candidate)

            if ok:
                existing = candidate.get("pillars", {})
            else:
                print(
                    f"      existing RAW invalid: {reason}"
                )
        except Exception as e:
            print(
                f"      existing RAW unreadable: {e}"
            )

    # Only retain pillars that are explicitly requested/valid.
    generated_pillars = dict(existing)

    remaining = []

    for pillar in missing:
        if pillar in generated_pillars:
            try:
                if generated_pillars[pillar]:
                    print(
                        f"      KEEP existing pillar: {pillar}"
                    )
                    continue
            except Exception:
                pass

        remaining.append(pillar)

    if not remaining:
        raw = {
            "chapter_id": chapter["chapter_id"],
            "chapter_title": chapter["chapter_title"],
            "source_bundle_sha256": job["source_bundle_sha256"],
            "pillars": generated_pillars,
        }

        ok, reason = validate_raw(raw)

        if not ok:
            return False, reason

        save_json(raw_file, raw)
        return True, "Existing staged output satisfies job"

    for pillar in remaining:
        print(
            f"      GENERATE pillar: {pillar}"
        )

        prompt = build_generation_prompt(
            job,
            pillar,
            prompt_text,
        )

        result = generate_pillar(
            model,
            prompt,
            pillar,
            chapter["chapter_title"],
        )

        generated_pillars[pillar] = result["items"]

    raw = {
        "chapter_id": chapter["chapter_id"],
        "chapter_title": chapter["chapter_title"],
        "source_bundle_sha256": job["source_bundle_sha256"],
        "pillars": generated_pillars,
    }

    ok, reason = validate_raw(raw)

    if not ok:
        return False, reason

    save_json(raw_file, raw)

    # Re-read from disk to verify UTF-8 JSON survives the write.
    reread = load_json(raw_file)

    ok, reason = validate_raw(reread)

    if not ok:
        return False, (
            f"Post-write validation failed: {reason}"
        )

    return True, (
        f"Generated {len(remaining)} pillar(s)"
    )


def discover_jobs(run_dir):
    jobs_dir = Path(run_dir) / "jobs"

    if not jobs_dir.exists():
        raise RuntimeError(
            f"Jobs directory does not exist: {jobs_dir}"
        )

    return sorted(
        [
            p
            for p in jobs_dir.iterdir()
            if p.is_dir()
            and (p / "JOB.json").exists()
        ],
        key=lambda p: p.name.lower(),
    )


def write_report(run_dir, results):
    report = {
        "run_id": Path(run_dir).name,
        "total_jobs": len(results),
        "passed": sum(
            1 for r in results if r["status"] == "PASS"
        ),
        "failed": sum(
            1 for r in results if r["status"] == "FAIL"
        ),
        "results": results,
    }

    report_file = Path(run_dir) / "V4_GENERATION_REPORT.json"
    save_json(report_file, report)

    return report_file


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--repo-root",
        required=True,
    )

    parser.add_argument(
        "--run-id",
        required=True,
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Regenerate even existing valid staged outputs",
    )

    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    run_dir = (
        repo_root
        / "generation_staging"
        / args.run_id
    )

    if not run_dir.exists():
        print(
            f"ERROR: staging run not found: {run_dir}"
        )
        return 2

    print("=" * 72)
    print("GURUKUL AI — V4 SOURCE-GROUNDED GENERATOR")
    print("=" * 72)
    print(f"Repository : {repo_root}")
    print(f"Run        : {args.run_id}")
    print(f"Model      : {args.model}")
    print("=" * 72)

    jobs = discover_jobs(run_dir)

    print(f"Jobs discovered: {len(jobs)}")

    results = []

    for index, job_dir in enumerate(jobs, 1):
        print()
        print("-" * 72)
        print(
            f"[{index}/{len(jobs)}] "
            f"{job_dir.name}"
        )
        print("-" * 72)

        started = time.time()

        try:
            ok, message = process_job(
                job_dir,
                args.model,
                args.force,
            )

            status = "PASS" if ok else "FAIL"

        except Exception as e:
            status = "FAIL"
            message = str(e)

        elapsed = round(time.time() - started, 1)

        print(
            f"[{status}] {message} "
            f"({elapsed}s)"
        )

        results.append(
            {
                "job": job_dir.name,
                "status": status,
                "message": message,
                "seconds": elapsed,
            }
        )

    report_file = write_report(
        run_dir,
        results,
    )

    passed = sum(
        1 for r in results if r["status"] == "PASS"
    )
    failed = len(results) - passed

    print()
    print("=" * 72)
    print("V4 GENERATION COMPLETE")
    print("=" * 72)
    print(f"Total : {len(results)}")
    print(f"Pass  : {passed}")
    print(f"Fail  : {failed}")
    print(f"Report: {report_file}")
    print("=" * 72)

    if failed:
        print(
            "PROMOTION BLOCKED: generation failures remain."
        )
        return 1

    print(
        "ALL JOBS PASSED LOCAL V4 VALIDATION."
    )
    print(
        "Promotion/rebuild has NOT been performed."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO = Path(r"D:\GURUKUL-AI")
RUN = REPO / "generation_staging" / "20260909T083940Z"

sys.path.insert(0, str(REPO / "backend" / "scripts"))
import generate_all_valid_contents as gavc


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def make_chapter(job):
    c = job["chapter"]
    return gavc.Chapter(
        class_name=c["class_name"],
        subject_name=c["subject_name"],
        path=Path(c["path"]),
        rel_path=c["rel_path"],
        chapter_id=str(c["chapter_id"]),
        chapter_title=c["chapter_title"],
    )


jobs = sorted(
    RUN.glob("jobs/*/JOB.json"),
    key=lambda p: str(p)
)

print("=" * 80)
print("GURUKUL AI - V4 -> CANONICAL VALIDATION BRIDGE")
print("=" * 80)
print(f"Run: {RUN}")
print(f"Jobs discovered: {len(jobs)}")
print()

if len(jobs) != 136:
    raise SystemExit(
        f"SAFETY STOP: expected 136 jobs, found {len(jobs)}"
    )

manifest = {
    "run_id": RUN.name,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "source": "V4_GENERATION",
    "bridge": "V4_RAW_TO_CANONICAL_VALIDATED",
    "chapters": [],
}

passed = 0
failed = 0
promotable = []

for n, job_path in enumerate(jobs, 1):
    job = read_json(job_path)
    chapter = make_chapter(job)
    missing = job.get("missing_pillars", [])

    raw_path = job_path.parent / "RAW_GENERATED.json"
    valid_path = job_path.parent / "VALIDATED_GENERATED.json"

    print(
        f"[{n:03d}/136] "
        f"{chapter.class_name} | "
        f"{chapter.subject_name} | "
        f"{chapter.chapter_id} | "
        f"{chapter.chapter_title}"
    )

    if not raw_path.exists():
        print("    FAIL: RAW_GENERATED.json missing")
        failed += 1
        manifest["chapters"].append({
            "chapter": job["chapter"],
            "missing_pillars": missing,
            "status": "missing_raw",
            "validation_errors": ["RAW_GENERATED.json missing"],
        })
        continue

    try:
        raw = read_json(raw_path)

        # V4 format:
        # "pillars": {"learn": [ ... ]}
        #
        # Canonical orchestrator format:
        # "pillars": {
        #   "learn": {
        #       "items": [ ... ],
        #       "gap": null
        #   }
        # }
        #
        # Convert ONLY the wrapper. Never alter source content.
        if not isinstance(raw, dict):
            raise ValueError("RAW payload is not an object")

        canonical_input = dict(raw)
        canonical_input["chapter_id"] = str(
            canonical_input.get("chapter_id", chapter.chapter_id)
        )
        canonical_input["chapter_title"] = canonical_input.get(
            "chapter_title", chapter.chapter_title
        )

        canonical_pillars = {}

        for pillar in missing:
            value = raw.get("pillars", {}).get(pillar)

            if isinstance(value, list):
                canonical_pillars[pillar] = {
                    "items": value,
                    "gap": None,
                }
            elif isinstance(value, dict):
                # Already canonical; retain it.
                canonical_pillars[pillar] = value
            else:
                canonical_pillars[pillar] = {
                    "items": [],
                    "gap": "V4 output missing pillar payload",
                }

        canonical_input["pillars"] = canonical_pillars

        bundle = gavc.source_bundle(
            chapter,
            120_000
        )

        ok, errors, normalized = gavc.validate_generated_payload(
            canonical_input,
            chapter,
            missing,
            bundle
        )

        if not ok:
            print("    FAIL")
            for error in errors:
                print(f"      - {error}")

            failed += 1

            manifest["chapters"].append({
                "chapter": job["chapter"],
                "missing_pillars": missing,
                "status": "invalid_generated_output",
                "validation_errors": errors,
                "raw_output": str(raw_path),
            })
            continue

        write_json(valid_path, normalized)

        print(
            f"    PASS: canonical validation "
            f"({len(normalized.get('pillars', {}))} pillars)"
        )

        passed += 1

        entry = {
            "chapter": job["chapter"],
            "missing_pillars": missing,
            "status": "validated",
            "validated_output": str(valid_path),
            "validation_errors": [],
        }

        manifest["chapters"].append(entry)
        promotable.append(entry)

    except Exception as exc:
        print(f"    FAIL: {type(exc).__name__}: {exc}")
        failed += 1

        manifest["chapters"].append({
            "chapter": job["chapter"],
            "missing_pillars": missing,
            "status": "bridge_error",
            "validation_errors": [str(exc)],
        })


manifest["summary"] = {
    "jobs": len(jobs),
    "validated": passed,
    "failed": failed,
    "promotable": len(promotable),
}

write_json(RUN / "V4_CANONICAL_BRIDGE_MANIFEST.json", manifest)

print()
print("=" * 80)
print("CANONICAL VALIDATION RESULT")
print("=" * 80)
print(f"Jobs      : {len(jobs)}")
print(f"Validated : {passed}")
print(f"Failed    : {failed}")
print(f"Promotable: {len(promotable)}")
print()

if failed:
    print("SAFETY STOP - NOTHING WILL BE PROMOTED.")
    print(f"Manifest: {RUN / 'V4_CANONICAL_BRIDGE_MANIFEST.json'}")
    raise SystemExit(2)

if passed != 136:
    raise SystemExit(
        f"SAFETY STOP: expected 136 validated jobs, got {passed}"
    )

print("ALL 136 JOBS PASSED THE REPOSITORY'S ACTUAL VALIDATOR.")
print()
print("Starting canonical promotion...")

promotion_manifest = {
    "run_id": RUN.name,
    "chapters": promotable,
}

promoted = gavc.promote_validated(
    RUN,
    REPO,
    promotion_manifest
)

print()
print("=" * 80)
print("PROMOTION RESULT")
print("=" * 80)
print(f"Validated jobs : {passed}")
print(f"Promoted files : {len(promoted)}")

if len(promoted) != sum(
    len(x["missing_pillars"])
    for x in promotable
):
    print("WARNING: promoted-file count differs from pillar count.")

write_json(
    RUN / "V4_PROMOTION_RESULT.json",
    {
        "run_id": RUN.name,
        "validated_jobs": passed,
        "failed_jobs": failed,
        "promoted_files": promoted,
        "promoted_count": len(promoted),
    }
)

print()
print("PROMOTION COMPLETE.")

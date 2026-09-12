#!/usr/bin/env python3
"""
GURUKUL AI — Full API Fidelity QA
=================================

Independent HTTP-vs-runtime integrity test for the actual FastAPI student API.

Read-only: this script never modifies runtime educational JSON.

It:
  * reads the runtime chapter JSON as the independent expected baseline;
  * calls the real /api/v1/student/* routes over HTTP;
  * traverses the API catalog -> classes -> subjects -> chapters;
  * compares chapter summary/full/layer responses with runtime files;
  * checks IDs, titles, class/subject mappings and pillar counts;
  * checks all catalog-visible chapters;
  * checks invalid layer and invalid chapter behavior;
  * reports the certified 183-job inventory vs 94 runtime-file population;
  * tests search and dashboard summary;
  * writes JSON and Markdown reports.

Usage:
  python backend/scripts/gurukul_api_fidelity_qa.py
  python backend/scripts/gurukul_api_fidelity_qa.py --api-base http://127.0.0.1:8000
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_PATH = "/api/v1/student"
LAYERS = ("learn", "practice", "assess", "revise", "resources", "traceability")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip()).casefold()


def get_id(obj: Any) -> str | None:
    if not isinstance(obj, dict):
        return None
    for key in ("id", "student_id", "record_id", "content_id", "uid"):
        value = obj.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def request_json(base: str, route: str, timeout: float) -> dict[str, Any]:
    url = base.rstrip("/") + route
    started = time.perf_counter()
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "GURUKUL-AI-API-Fidelity-QA/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read()
            elapsed = time.perf_counter() - started
            text = raw.decode("utf-8", errors="replace")
            try:
                data = json.loads(text)
                return {
                    "ok": 200 <= response.status < 300,
                    "status": response.status,
                    "data": data,
                    "elapsed_ms": round(elapsed * 1000, 2),
                    "error": None,
                    "url": url,
                }
            except Exception as exc:
                return {
                    "ok": False,
                    "status": response.status,
                    "data": None,
                    "elapsed_ms": round(elapsed * 1000, 2),
                    "error": f"invalid_json: {exc}",
                    "url": url,
                }
    except urllib.error.HTTPError as exc:
        elapsed = time.perf_counter() - started
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        try:
            data = json.loads(body)
        except Exception:
            data = body[:1000]
        return {
            "ok": False,
            "status": exc.code,
            "data": data,
            "elapsed_ms": round(elapsed * 1000, 2),
            "error": str(exc),
            "url": url,
        }
    except Exception as exc:
        elapsed = time.perf_counter() - started
        return {
            "ok": False,
            "status": 0,
            "data": None,
            "elapsed_ms": round(elapsed * 1000, 2),
            "error": str(exc),
            "url": url,
        }


def runtime_inventory(repo: Path) -> dict[str, Any]:
    root = repo / "runtime-data" / "chapters"
    files = sorted(root.rglob("*.json")) if root.is_dir() else []

    by_identity: dict[tuple[str, str, str], list[Path]] = defaultdict(list)
    records = []

    for path in files:
        try:
            data = load_json(path)
        except Exception as exc:
            records.append({
                "file": str(path.relative_to(repo)).replace("\\", "/"),
                "error": f"invalid_json: {exc}",
            })
            continue

        trace = data.get("traceability")
        info = trace.get("chapter_info") if isinstance(trace, dict) else {}
        if not isinstance(info, dict):
            info = {}

        class_id = str(data.get("classId", info.get("class_id", "")))
        subject_id = str(data.get("subjectId", info.get("subject_id", "")))
        chapter_id = str(data.get("chapter_id", info.get("chapter_id", path.stem)))
        title = str(data.get("title", info.get("chapter_title", data.get("chapter_title", ""))))

        # Catalog route uses chapter ID from catalog and load_chapter() uses
        # the class/subject names plus chapter_id to find this JSON.
        key = (norm(class_id), norm(subject_id), norm(chapter_id))
        by_identity[key].append(path)

        records.append({
            "file": str(path.relative_to(repo)).replace("\\", "/"),
            "class_id": class_id,
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "title": title,
            "data": data,
            "sha256": sha256(path),
        })

    duplicates = {
        "|".join(k): [str(p) for p in paths]
        for k, paths in by_identity.items()
        if len(paths) > 1
    }

    return {
        "root": str(root),
        "file_count": len(files),
        "records": records,
        "by_identity": by_identity,
        "duplicate_identities": duplicates,
    }


def compare_scalar(result: dict[str, Any], field: str, expected: Any, actual: Any):
    if norm(expected) != norm(actual):
        result["failures"].append({
            "type": "field_mismatch",
            "field": field,
            "expected": expected,
            "actual": actual,
        })


def compare_records(expected: list[Any], actual: Any, path: str, result: dict[str, Any]):
    if not isinstance(actual, list):
        result["failures"].append({
            "type": "layer_not_list",
            "path": path,
            "actual_type": type(actual).__name__,
        })
        return

    if len(expected) != len(actual):
        result["failures"].append({
            "type": "count_mismatch",
            "path": path,
            "expected": len(expected),
            "actual": len(actual),
        })

    n = min(len(expected), len(actual))
    for i in range(n):
        e, a = expected[i], actual[i]
        if isinstance(e, dict) and isinstance(a, dict):
            eid = get_id(e)
            aid = get_id(a)
            if eid and aid and eid != aid:
                result["failures"].append({
                    "type": "record_id_mismatch",
                    "path": f"{path}[{i}]",
                    "expected": eid,
                    "actual": aid,
                })
            elif eid and not aid:
                result["failures"].append({
                    "type": "missing_api_record_id",
                    "path": f"{path}[{i}]",
                    "expected": eid,
                })


def find_runtime_record(inv: dict[str, Any], class_id: str, subject_id: str, chapter_id: str):
    key = (norm(class_id), norm(subject_id), norm(chapter_id))
    paths = inv["by_identity"].get(key, [])
    if len(paths) == 1:
        p = paths[0]
        # Compare by checking if record file ends with the relative path from runtime root
        target_suffix = str(p.relative_to(Path(inv["root"]).parent.parent)).replace("\\", "/")
        for r in inv["records"]:
            if r.get("file") == target_suffix:
                return r
    return None


def api_catalog_walk(base: str, inv: dict[str, Any], timeout: float) -> dict[str, Any]:
    failures = []
    warnings = []
    timings = []
    chapter_results = []
    seen_catalog_chapters = set()

    catalog_r = request_json(base, f"{BASE_PATH}/catalog", timeout)
    timings.append({"route": f"{BASE_PATH}/catalog", "ms": catalog_r["elapsed_ms"], "status": catalog_r["status"]})

    if not catalog_r["ok"] or not isinstance(catalog_r["data"], dict):
        failures.append({"type": "catalog_unavailable", "response": catalog_r})
        return {
            "status": "FAIL",
            "catalog": catalog_r,
            "chapter_results": [],
            "failures": failures,
            "warnings": warnings,
            "timings": timings,
        }

    catalog = catalog_r["data"]
    classes = catalog.get("classes")
    if not isinstance(classes, list):
        failures.append({"type": "catalog_classes_not_list"})
        return {
            "status": "FAIL",
            "catalog": catalog_r,
            "chapter_results": [],
            "failures": failures,
            "warnings": warnings,
            "timings": timings,
        }

    # Check classes endpoint against catalog.
    classes_r = request_json(base, f"{BASE_PATH}/classes", timeout)
    timings.append({"route": f"{BASE_PATH}/classes", "ms": classes_r["elapsed_ms"], "status": classes_r["status"]})
    if not classes_r["ok"] or not isinstance(classes_r["data"], list):
        failures.append({"type": "classes_endpoint_failed", "response": classes_r})
    elif len(classes_r["data"]) != len(classes):
        failures.append({
            "type": "classes_count_mismatch",
            "catalog": len(classes),
            "api": len(classes_r["data"]),
        })

    for cls in classes:
        if not isinstance(cls, dict):
            failures.append({"type": "class_not_object"})
            continue

        class_id = str(cls.get("id", ""))
        subjects = cls.get("subjects", [])
        class_r = request_json(base, f"{BASE_PATH}/classes/{class_id}", timeout)
        timings.append({"route": f"{BASE_PATH}/classes/{class_id}", "ms": class_r["elapsed_ms"], "status": class_r["status"]})
        if not class_r["ok"]:
            failures.append({"type": "class_endpoint_failed", "class_id": class_id, "response": class_r})
        elif isinstance(class_r["data"], dict):
            compare_scalar({"failures": failures}, "class.id", class_id, class_r["data"].get("id"))
        else:
            failures.append({"type": "class_response_not_object", "class_id": class_id})

        subject_route = f"{BASE_PATH}/classes/{class_id}/subjects"
        subject_r = request_json(base, subject_route, timeout)
        timings.append({"route": subject_route, "ms": subject_r["elapsed_ms"], "status": subject_r["status"]})
        if not subject_r["ok"] or not isinstance(subject_r["data"], list):
            failures.append({"type": "class_subjects_endpoint_failed", "class_id": class_id, "response": subject_r})
        elif len(subject_r["data"]) != len(subjects):
            failures.append({
                "type": "class_subject_count_mismatch",
                "class_id": class_id,
                "catalog": len(subjects),
                "api": len(subject_r["data"]),
            })

        for subj in subjects:
            if not isinstance(subj, dict):
                failures.append({"type": "subject_not_object", "class_id": class_id})
                continue

            subject_id = str(subj.get("id", ""))
            chapters = subj.get("chapters", [])

            subj_r = request_json(base, f"{BASE_PATH}/subjects/{subject_id}", timeout)
            timings.append({"route": f"{BASE_PATH}/subjects/{subject_id}", "ms": subj_r["elapsed_ms"], "status": subj_r["status"]})
            if not subj_r["ok"]:
                failures.append({"type": "subject_endpoint_failed", "subject_id": subject_id, "response": subj_r})

            subj_ch_r = request_json(base, f"{BASE_PATH}/subjects/{subject_id}/chapters", timeout)
            timings.append({"route": f"{BASE_PATH}/subjects/{subject_id}/chapters", "ms": subj_ch_r["elapsed_ms"], "status": subj_ch_r["status"]})
            if not subj_ch_r["ok"] or not isinstance(subj_ch_r["data"], list):
                failures.append({"type": "subject_chapters_endpoint_failed", "subject_id": subject_id, "response": subj_ch_r})
            elif len(subj_ch_r["data"]) != len(chapters):
                failures.append({
                    "type": "subject_chapter_count_mismatch",
                    "subject_id": subject_id,
                    "catalog": len(chapters),
                    "api": len(subj_ch_r["data"]),
                })

            for ch in chapters:
                if not isinstance(ch, dict):
                    failures.append({"type": "chapter_catalog_entry_not_object", "subject_id": subject_id})
                    continue

                uid = str(ch.get("id", ""))
                chapter_id = str(ch.get("chapter_id", ""))
                title = str(ch.get("title", ""))
                seen_catalog_chapters.add(uid)

                cr = {
                    "chapter_uid": uid,
                    "class_id": class_id,
                    "subject_id": subject_id,
                    "chapter_id": chapter_id,
                    "title": title,
                    "status": "PASS",
                    "failures": [],
                    "layers": {},
                }

                summary = request_json(base, f"{BASE_PATH}/chapters/{uid}", timeout)
                timings.append({"route": f"{BASE_PATH}/chapters/{uid}", "ms": summary["elapsed_ms"], "status": summary["status"]})
                if not summary["ok"] or not isinstance(summary["data"], dict):
                    cr["failures"].append({"type": "summary_failed", "response": summary})
                else:
                    compare_scalar(cr, "summary.id", uid, summary["data"].get("id"))
                    compare_scalar(cr, "summary.title", title, summary["data"].get("title"))
                    compare_scalar(cr, "summary.classId", class_id, summary["data"].get("classId"))
                    compare_scalar(cr, "summary.subjectId", subject_id, summary["data"].get("subjectId"))

                full = request_json(base, f"{BASE_PATH}/chapters/{uid}/full", timeout)
                timings.append({"route": f"{BASE_PATH}/chapters/{uid}/full", "ms": full["elapsed_ms"], "status": full["status"]})

                runtime = find_runtime_record(inv, class_id, subject_id, chapter_id)
                if runtime is None:
                    cr["failures"].append({
                        "type": "runtime_baseline_not_found",
                        "class_id": class_id,
                        "subject_id": subject_id,
                        "chapter_id": chapter_id,
                    })
                elif not full["ok"] or not isinstance(full["data"], dict):
                    cr["failures"].append({"type": "full_endpoint_failed", "response": full})
                else:
                    expected = runtime["data"]
                    actual = full["data"]
                    for field in ("id", "title", "classId", "subjectId"):
                        compare_scalar(cr, f"full.{field}", expected.get(field), actual.get(field))

                    for layer in LAYERS:
                        expected_layer = expected.get(layer, [])
                        actual_layer = actual.get(layer, [])
                        layer_result = {"expected": len(expected_layer) if isinstance(expected_layer, list) else 1 if isinstance(expected_layer, dict) else 0,
                                        "actual": len(actual_layer) if isinstance(actual_layer, list) else 1 if isinstance(actual_layer, dict) else 0}

                        if layer == "traceability":
                            # Special case for traceability dict
                            layer_result["pass"] = isinstance(actual_layer, dict)
                            if not layer_result["pass"]:
                                cr["failures"].append({"type": "full_traceability_not_dict", "layer": layer})
                            continue

                        if isinstance(expected_layer, list):
                            before = len(cr["failures"])
                            compare_records(expected_layer, actual_layer, f"full.{layer}", cr)
                            layer_result["pass"] = len(cr["failures"]) == before
                        else:
                            layer_result["pass"] = False
                            cr["failures"].append({"type": "runtime_layer_not_list", "layer": layer})
                        cr["layers"][layer] = layer_result

                    # Individual layer endpoint must match the full response layer.
                    for layer in LAYERS:
                        lr = request_json(base, f"{BASE_PATH}/chapters/{uid}/{layer}", timeout)
                        timings.append({"route": f"{BASE_PATH}/chapters/{uid}/{layer}", "ms": lr["elapsed_ms"], "status": lr["status"]})
                        if not lr["ok"] or not isinstance(lr["data"], dict):
                            cr["failures"].append({"type": "layer_endpoint_failed", "layer": layer, "response": lr})
                            continue
                        items = lr["data"].get("items")
                        meta = lr["data"].get("metadata", {})
                        expected_layer = expected.get(layer, [])

                        if layer == "traceability":
                            if not isinstance(items, dict):
                                cr["failures"].append({"type": "layer_traceability_not_dict", "layer": layer})
                            compare_scalar(cr, f"{layer}.metadata.id", expected.get("id"), meta.get("id"))
                            continue

                        if not isinstance(items, list):
                            cr["failures"].append({"type": "layer_items_not_list", "layer": layer})
                        else:
                            if len(items) != len(expected_layer):
                                cr["failures"].append({
                                    "type": "layer_count_mismatch",
                                    "layer": layer,
                                    "expected": len(expected_layer),
                                    "actual": len(items),
                                })
                            else:
                                compare_records(expected_layer, items, f"api.{layer}", cr)
                        compare_scalar(cr, f"{layer}.metadata.id", expected.get("id"), meta.get("id"))
                        compare_scalar(cr, f"{layer}.metadata.title", expected.get("title"), meta.get("title"))

                if cr["failures"]:
                    cr["status"] = "FAIL"
                    failures.extend([{"chapter_uid": uid, **x} for x in cr["failures"]])
                chapter_results.append(cr)

    # Negative route tests.
    bad_chapter = request_json(base, f"{BASE_PATH}/chapters/__gurukul_invalid_chapter__", timeout)
    timings.append({"route": f"{BASE_PATH}/chapters/__gurukul_invalid_chapter__", "ms": bad_chapter["elapsed_ms"], "status": bad_chapter["status"]})
    if bad_chapter["status"] != 404:
        failures.append({"type": "invalid_chapter_should_404", "status": bad_chapter["status"]})

    bad_layer = request_json(base, f"{BASE_PATH}/chapters/__gurukul_invalid_chapter__/invalid_layer", timeout)
    timings.append({"route": f"{BASE_PATH}/chapters/__gurukul_invalid_chapter__/invalid_layer", "ms": bad_layer["elapsed_ms"], "status": bad_layer["status"]})
    # Route lookup occurs before layer validation, so 404 is acceptable here.
    if bad_layer["status"] not in (400, 404):
        failures.append({"type": "invalid_layer_unexpected_status", "status": bad_layer["status"]})

    return {
        "status": "PASS" if not failures else "FAIL",
        "catalog": {
            "classes": len(classes),
            "catalog_chapters": len(seen_catalog_chapters),
        },
        "chapter_results": chapter_results,
        "failures": failures,
        "warnings": warnings,
        "timings": timings,
    }


def search_and_dashboard(base: str, timeout: float) -> dict[str, Any]:
    results = []
    search = request_json(base, f"{BASE_PATH}/search?q=India", timeout)
    results.append({
        "test": "search?q=India",
        "status": search["status"],
        "ok": search["ok"] and isinstance(search["data"], list),
        "result_count": len(search["data"]) if isinstance(search["data"], list) else None,
    })

    dashboard = request_json(base, f"{BASE_PATH}/dashboard/summary", timeout)
    results.append({
        "test": "dashboard/summary",
        "status": dashboard["status"],
        "ok": dashboard["ok"] and isinstance(dashboard["data"], dict),
        "data": dashboard["data"] if isinstance(dashboard["data"], dict) else None,
    })

    return {
        "status": "PASS" if all(x["ok"] for x in results) else "FAIL",
        "tests": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="GURUKUL AI full API fidelity QA")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--api-base", default="http://127.0.0.1:8000")
    parser.add_argument("--timeout", type=float, default=15.0)
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    inv = runtime_inventory(repo)

    api = api_catalog_walk(args.api_base, inv, args.timeout)
    misc = search_and_dashboard(args.api_base, args.timeout)

    # Locate canonical job evidence without trusting it for API expected values.
    evidence = repo / "CANONICAL_VALIDATION_PROMOTION_EVIDENCE.txt"
    evidence_status = {
        "exists": evidence.exists(),
        "jobs_136": False,
        "validated_136": False,
        "failed_0": False,
        "promotable_136": False,
        "promoted_440": False,
        "promotion_complete": False,
    }
    if evidence.exists():
        try:
            text = evidence.read_text(encoding="utf-16", errors="replace")
            evidence_status.update({
                "jobs_136": bool(re.search(r"Jobs\s*:\s*136\b", text, re.I)),
                "validated_136": bool(re.search(r"Validated\s*:\s*136\b", text, re.I)),
                "failed_0": bool(re.search(r"Failed\s*:\s*0\b", text, re.I)),
                "promotable_136": bool(re.search(r"Promotable\s*:\s*136\b", text, re.I)),
                "promoted_440": bool(re.search(r"Promoted\s+files\s*:\s*440\b", text, re.I)),
                "promotion_complete": bool(re.search(r"PROMOTION\s+COMPLETE", text, re.I)),
            })
        except Exception as exc:
            evidence_status["error"] = str(exc)

    overall = (
        inv["file_count"] > 0
        and not inv["duplicate_identities"]
        and api["status"] == "PASS"
        and misc["status"] == "PASS"
    )

    report = {
        "overall_status": "API_FIDELITY_PASS" if overall else "API_FIDELITY_FAIL",
        "generated_at": now_iso(),
        "api_base": args.api_base,
        "runtime_baseline": {
            "chapter_files": inv["file_count"],
            "duplicate_identities": inv["duplicate_identities"],
        },
        "catalog_vs_runtime": {
            "certified_generation_jobs": 136 if all(evidence_status.values()) else None,
            "runtime_chapter_files": inv["file_count"],
            "api_catalog_chapters": api.get("catalog", {}).get("catalog_chapters"),
            "note": "Generation-job count, runtime-file count, and API-catalog chapter count are separate populations and are reported without silently reconciling them.",
        },
        "canonical_promotion_evidence": evidence_status,
        "api_fidelity": api,
        "search_dashboard": misc,
    }

    jp = repo / "GURUKUL_API_FIDELITY_REPORT.json"
    mp = repo / "GURUKUL_API_FIDELITY_REPORT.md"
    jp.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    failed_chapters = [x for x in api["chapter_results"] if x["status"] == "FAIL"]
    md = [
        "# GURUKUL AI — Full API Fidelity QA",
        "",
        f"**Overall status:** `{report['overall_status']}`",
        f"**Generated:** `{report['generated_at']}`",
        "",
        "## Coverage",
        f"- Certified generation jobs: **{report['catalog_vs_runtime']['certified_generation_jobs']}**",
        f"- Runtime chapter files: **{inv['file_count']}**",
        f"- API catalog chapters: **{api.get('catalog', {}).get('catalog_chapters')}**",
        f"- API chapter tests completed: **{len(api['chapter_results'])}**",
        f"- Failed chapters: **{len(failed_chapters)}**",
        "",
        "## API Gates",
        f"- Catalog/classes/subjects/chapters traversal: **{api['status']}**",
        f"- Search: **{misc['tests'][0]['status']}**",
        f"- Dashboard summary: **{misc['tests'][1]['status']}**",
        "",
        "## Canonical Evidence",
        f"- 136/136 validation: **{report['canonical_promotion_evidence']['validated_136']}**",
        f"- 440 promoted files: **{report['canonical_promotion_evidence']['promoted_440']}**",
        "",
        "## Release Gate",
        f"**`{report['overall_status']}`**",
        "",
        "Expected values are independently read from runtime JSON; API responses are obtained over HTTP.",
    ]
    if api["failures"]:
        md += ["", "## First Failures"]
        for f in api["failures"][:50]:
            md.append(f"- `{json.dumps(f, ensure_ascii=False)}`")

    mp.write_text("\n".join(md) + "\n", encoding="utf-8")

    print("=" * 72)
    print("GURUKUL AI — FULL API FIDELITY QA")
    print("=" * 72)
    print("Overall status          :", report["overall_status"])
    print("Runtime chapter files   :", inv["file_count"])
    print("API catalog chapters    :", api.get("catalog", {}).get("catalog_chapters"))
    print("API chapter tests       :", len(api["chapter_results"]))
    print("Failed chapters         :", len(failed_chapters))
    print("API traversal           :", api["status"])
    print("Search                  :", misc["tests"][0]["status"])
    print("Dashboard summary       :", misc["tests"][1]["status"])
    print("Canonical 136/136       :", evidence_status["validated_136"])
    print("Canonical 440 promoted  :", evidence_status["promoted_440"])
    print()
    print("JSON:", jp)
    print("MD  :", mp)
    if api["failures"]:
        print("\nFIRST FAILURES:")
        for failure in api["failures"][:30]:
            print(json.dumps(failure, ensure_ascii=False))
    print("=" * 72)

    return 0 if overall else 2


if __name__ == "__main__":
    raise SystemExit(main())

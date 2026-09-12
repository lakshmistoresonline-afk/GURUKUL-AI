#!/usr/bin/env python3
"""
GURUKUL AI — COMPLETE API FIDELITY CERTIFICATION

Purpose
-------
Proves that the live Student API serves the same certified data that exists
in runtime-data.

This is a DATA FIDELITY test, not merely an HTTP availability test.

Coverage
--------
* Runtime discovery
* Catalog
* Classes
* Class -> subjects
* Subject
* Subject -> chapters
* Chapter summary
* Chapter full payload
* Learn
* Practice
* Assess
* Revise
* Resources
* Traceability
* Search
* Class-filtered search
* Dashboard

Failure policy
--------------
ANY unexpected HTTP status, missing endpoint, malformed JSON, missing chapter,
unexpected chapter, ID mismatch, count mismatch, or payload mismatch causes
exit code 1.

Outputs
-------
GURUKUL_API_FIDELITY_CERTIFICATION.json
GURUKUL_API_FIDELITY_CERTIFICATION.md
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ============================================================================
# CONFIGURATION
# ============================================================================

REPO_ROOT = Path(__file__).resolve().parents[2]

RUNTIME_ROOT = REPO_ROOT / "runtime-data"
CATALOG_PATH = RUNTIME_ROOT / "catalog.json"
SEARCH_INDEX_PATH = RUNTIME_ROOT / "search" / "index.json"

REPORT_JSON = REPO_ROOT / "GURUKUL_API_FIDELITY_CERTIFICATION.json"
REPORT_MD = REPO_ROOT / "GURUKUL_API_FIDELITY_CERTIFICATION.md"

API_BASE = os.environ.get(
    "GURUKUL_API_BASE",
    "http://127.0.0.1:8000/api/v1/student"
).rstrip("/")

HTTP_TIMEOUT = float(os.environ.get("GURUKUL_API_TIMEOUT", "15"))
HTTP_RETRIES = int(os.environ.get("GURUKUL_API_RETRIES", "3"))
RETRY_DELAY = float(os.environ.get("GURUKUL_API_RETRY_DELAY", "0.5"))

LAYERS = [
    "learn",
    "practice",
    "assess",
    "revise",
    "resources",
]

# Traceability is tested as an additional integrity layer because the current
# API explicitly exposes it.
ALL_LAYERS = LAYERS + ["traceability"]

MAX_MISMATCHES_STORED = 100
SEARCH_TEST_COUNT = 25


# ============================================================================
# RESULT MODEL
# ============================================================================

@dataclass
class TestResult:
    name: str
    passed: bool
    expected: Any = None
    actual: Any = None
    detail: str = ""
    path: str = ""


RESULTS: List[TestResult] = []


def record(
    name: str,
    passed: bool,
    expected: Any = None,
    actual: Any = None,
    detail: str = "",
    path: str = "",
) -> None:
    RESULTS.append(
        TestResult(
            name=name,
            passed=passed,
            expected=expected,
            actual=actual,
            detail=detail,
            path=path,
        )
    )


# ============================================================================
# GENERAL HELPERS
# ============================================================================

def utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_json(value: Any) -> str:
    return hashlib.sha256(
        canonical_json(value).encode("utf-8")
    ).hexdigest()


def normalize(value: Any) -> Any:
    """
    Normalize JSON without changing semantics.

    Lists remain ordered because API ordering is part of the contract.
    Dict key ordering is irrelevant.
    """
    if isinstance(value, dict):
        return {
            str(k): normalize(v)
            for k, v in value.items()
        }

    if isinstance(value, list):
        return [normalize(v) for v in value]

    return value


def first_difference(
    expected: Any,
    actual: Any,
    path: str = "$",
) -> Optional[Tuple[str, Any, Any]]:
    """
    Return the first semantic JSON difference.
    """
    if type(expected) is not type(actual):
        return path, expected, actual

    if isinstance(expected, dict):
        ek = set(expected.keys())
        ak = set(actual.keys())

        missing = sorted(ek - ak)
        if missing:
            key = missing[0]
            return f"{path}.{key}", expected[key], "<MISSING>"

        unexpected = sorted(ak - ek)
        if unexpected:
            key = unexpected[0]
            return f"{path}.{key}", "<ABSENT>", actual[key]

        for key in sorted(ek):
            diff = first_difference(
                expected[key],
                actual[key],
                f"{path}.{key}",
            )
            if diff:
                return diff

        return None

    if isinstance(expected, list):
        if len(expected) != len(actual):
            return (
                f"{path}.length",
                len(expected),
                len(actual),
            )

        for i, (e, a) in enumerate(zip(expected, actual)):
            diff = first_difference(
                e,
                a,
                f"{path}[{i}]",
            )
            if diff:
                return diff

        return None

    if expected != actual:
        return path, expected, actual

    return None


def payload_summary(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            "type": "object",
            "keys": list(value.keys()),
            "sha256": sha256_json(value),
        }

    if isinstance(value, list):
        return {
            "type": "array",
            "length": len(value),
            "sha256": sha256_json(value),
        }

    return {
        "type": type(value).__name__,
        "value": value,
    }


# ============================================================================
# HTTP CLIENT
# ============================================================================

class APIError(Exception):
    pass


def http_get(path: str) -> Tuple[int, Any, float]:
    url = API_BASE + "/" + path.lstrip("/")

    last_error = None

    for attempt in range(1, HTTP_RETRIES + 1):
        started = time.perf_counter()

        try:
            request = urllib.request.Request(
                url,
                method="GET",
                headers={
                    "Accept": "application/json",
                    "User-Agent": "GURUKUL-AI-API-Fidelity/1.0",
                },
            )

            with urllib.request.urlopen(
                request,
                timeout=HTTP_TIMEOUT,
            ) as response:
                raw = response.read()
                elapsed = time.perf_counter() - started

                try:
                    payload = json.loads(raw.decode("utf-8"))
                except Exception as exc:
                    raise APIError(
                        f"Invalid JSON response from {url}: {exc}"
                    )

                return response.status, payload, elapsed

        except urllib.error.HTTPError as exc:
            elapsed = time.perf_counter() - started

            try:
                raw = exc.read().decode("utf-8", errors="replace")
                payload = json.loads(raw)
            except Exception:
                payload = raw if "raw" in locals() else str(exc)

            last_error = APIError(
                f"HTTP {exc.code} from {url}: {payload}"
            )

            if attempt < HTTP_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
                continue

            return exc.code, payload, elapsed

        except Exception as exc:
            elapsed = time.perf_counter() - started
            last_error = exc

            if attempt < HTTP_RETRIES:
                time.sleep(RETRY_DELAY * attempt)
                continue

            raise APIError(
                f"Request failed after {HTTP_RETRIES} attempts: {url}: {exc}"
            )

    raise APIError(str(last_error))


def assert_get(
    name: str,
    path: str,
    expected_status: int = 200,
) -> Optional[Any]:
    try:
        status, payload, elapsed = http_get(path)

        passed = status == expected_status

        record(
            name=name,
            passed=passed,
            expected=expected_status,
            actual=status,
            detail=f"{path} ({elapsed:.3f}s)",
            path=path,
        )

        if not passed:
            return None

        return payload

    except Exception as exc:
        record(
            name=name,
            passed=False,
            expected=expected_status,
            actual="REQUEST_ERROR",
            detail=str(exc),
            path=path,
        )
        return None


# ============================================================================
# RUNTIME DISCOVERY
# ============================================================================

@dataclass
class ChapterRef:
    class_id: str
    class_name: str
    subject_id: str
    subject_name: str
    chapter_id: str
    chapter_uid: str
    runtime_path: str


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def discover_runtime() -> Tuple[Dict[str, Any], List[ChapterRef], Dict[str, Any]]:
    if not CATALOG_PATH.exists():
        raise RuntimeError(f"Missing catalog: {CATALOG_PATH}")

    if not SEARCH_INDEX_PATH.exists():
        raise RuntimeError(f"Missing search index: {SEARCH_INDEX_PATH}")

    catalog = load_json(CATALOG_PATH)
    search_data = load_json(SEARCH_INDEX_PATH)

    if not isinstance(catalog, dict):
        raise RuntimeError("catalog.json is not an object")

    if not isinstance(search_data, (dict, list)):
        raise RuntimeError("search/index.json has invalid root type")

    if isinstance(search_data, dict):
        search_records = search_data.get("records", [])
    else:
        search_records = search_data

    if not isinstance(search_records, list):
        raise RuntimeError("search index records is not an array")

    chapters: List[ChapterRef] = []

    for cls in catalog.get("classes", []):
        class_id = str(cls["id"])
        class_name = str(cls["name"])

        for subj in cls.get("subjects", []):
            subject_id = str(subj["id"])
            subject_name = str(subj["name"])

            for ch in subj.get("chapters", []):
                chapter_id = str(ch["chapter_id"])
                chapter_uid = str(ch["id"])

                # Canonical runtime filesystem namespace.
                # IMPORTANT: class_id is the filesystem namespace;
                # class_name is display-only metadata.
                runtime_class_namespace = class_id

                runtime_path = (
                    RUNTIME_ROOT
                    / "chapters"
                    / runtime_class_namespace
                    / subject_name
                    / f"{chapter_id}.json"
                )

                chapters.append(
                    ChapterRef(
                        class_id=class_id,
                        class_name=class_name,
                        subject_id=subject_id,
                        subject_name=subject_name,
                        chapter_id=chapter_id,
                        chapter_uid=chapter_uid,
                        runtime_path=str(runtime_path),
                    )
                )

    return catalog, chapters, {
        "records": search_records,
        "raw": search_data,
    }


# ============================================================================
# RUNTIME PAYLOAD VALIDATION
# ============================================================================

def load_runtime_chapter(ref: ChapterRef) -> Optional[Dict[str, Any]]:
    path = Path(ref.runtime_path)

    if not path.exists():
        record(
            name=f"RUNTIME_FILE::{ref.chapter_uid}",
            passed=False,
            expected="existing runtime chapter",
            actual="missing",
            detail=str(path),
            path=str(path),
        )
        return None

    try:
        payload = load_json(path)
    except Exception as exc:
        record(
            name=f"RUNTIME_JSON::{ref.chapter_uid}",
            passed=False,
            expected="valid JSON",
            actual="invalid",
            detail=str(exc),
            path=str(path),
        )
        return None

    if not isinstance(payload, dict):
        record(
            name=f"RUNTIME_OBJECT::{ref.chapter_uid}",
            passed=False,
            expected="JSON object",
            actual=type(payload).__name__,
            path=str(path),
        )
        return None

    return payload


# ============================================================================
# CATALOG TESTS
# ============================================================================

def test_catalog(catalog: Dict[str, Any], chapters: List[ChapterRef]) -> None:
    api_catalog = assert_get(
        "CATALOG_HTTP",
        "/catalog",
    )

    if api_catalog is not None:
        diff = first_difference(
            normalize(catalog),
            normalize(api_catalog),
        )

        record(
            "CATALOG_FIDELITY",
            diff is None,
            expected=payload_summary(catalog),
            actual=payload_summary(api_catalog),
            detail="Exact catalog comparison"
            if diff is None
            else f"Mismatch at {diff[0]}",
            path=diff[0] if diff else "",
        )

    api_classes = assert_get(
        "CLASSES_HTTP",
        "/classes",
    )

    expected_classes = catalog.get("classes", [])

    if api_classes is not None:
        diff = first_difference(
            normalize(expected_classes),
            normalize(api_classes),
        )

        record(
            "CLASSES_FIDELITY",
            diff is None,
            expected=len(expected_classes),
            actual=len(api_classes) if isinstance(api_classes, list) else None,
            detail="Exact class list"
            if diff is None
            else f"Mismatch at {diff[0]}",
            path=diff[0] if diff else "",
        )

    record(
        "RUNTIME_CHAPTER_COUNT",
        len(chapters) == 183,
        expected=183,
        actual=len(chapters),
        detail="Certified runtime chapter count",
    )


# ============================================================================
# CLASS / SUBJECT / CHAPTER TRAVERSAL
# ============================================================================

def test_traversal(catalog: Dict[str, Any]) -> None:
    for cls in catalog.get("classes", []):
        class_id = str(cls["id"])
        expected_subjects = cls.get("subjects", [])

        api_class = assert_get(
            f"CLASS::{class_id}",
            f"/classes/{urllib.parse.quote(class_id, safe='')}",
        )

        if api_class is not None:
            diff = first_difference(
                normalize(cls),
                normalize(api_class),
            )

            record(
                f"CLASS_FIDELITY::{class_id}",
                diff is None,
                expected=payload_summary(cls),
                actual=payload_summary(api_class),
                detail="Exact class object"
                if diff is None
                else f"Mismatch at {diff[0]}",
                path=diff[0] if diff else "",
            )

        api_subjects = assert_get(
            f"CLASS_SUBJECTS::{class_id}",
            f"/classes/{urllib.parse.quote(class_id, safe='')}/subjects",
        )

        if api_subjects is not None:
            diff = first_difference(
                normalize(expected_subjects),
                normalize(api_subjects),
            )

            record(
                f"CLASS_SUBJECTS_FIDELITY::{class_id}",
                diff is None,
                expected=len(expected_subjects),
                actual=len(api_subjects)
                if isinstance(api_subjects, list)
                else None,
                detail="Exact subject traversal"
                if diff is None
                else f"Mismatch at {diff[0]}",
                path=diff[0] if diff else "",
            )

        for subj in expected_subjects:
            subject_id = str(subj["id"])
            expected_chapters = subj.get("chapters", [])

            api_subject = assert_get(
                f"SUBJECT::{subject_id}",
                f"/subjects/{urllib.parse.quote(subject_id, safe='')}",
            )

            if api_subject is not None:
                diff = first_difference(
                    normalize(subj),
                    normalize(api_subject),
                )

                record(
                    f"SUBJECT_FIDELITY::{subject_id}",
                    diff is None,
                    expected=payload_summary(subj),
                    actual=payload_summary(api_subject),
                    detail="Exact subject object"
                    if diff is None
                    else f"Mismatch at {diff[0]}",
                    path=diff[0] if diff else "",
                )

            api_chapters = assert_get(
                f"SUBJECT_CHAPTERS::{subject_id}",
                f"/subjects/{urllib.parse.quote(subject_id, safe='')}/chapters",
            )

            if api_chapters is not None:
                diff = first_difference(
                    normalize(expected_chapters),
                    normalize(api_chapters),
                )

                record(
                    f"SUBJECT_CHAPTERS_FIDELITY::{subject_id}",
                    diff is None,
                    expected=len(expected_chapters),
                    actual=len(api_chapters)
                    if isinstance(api_chapters, list)
                    else None,
                    detail="Exact chapter traversal"
                    if diff is None
                    else f"Mismatch at {diff[0]}",
                    path=diff[0] if diff else "",
                )

            for ch in expected_chapters:
                uid = str(ch["id"])

                api_summary = assert_get(
                    f"CHAPTER_SUMMARY::{uid}",
                    f"/chapters/{urllib.parse.quote(uid, safe='')}",
                )

                if api_summary is not None:
                    diff = first_difference(
                        normalize(ch),
                        normalize(api_summary),
                    )

                    record(
                        f"CHAPTER_SUMMARY_FIDELITY::{uid}",
                        diff is None,
                        expected=payload_summary(ch),
                        actual=payload_summary(api_summary),
                        detail="Exact chapter summary"
                        if diff is None
                        else f"Mismatch at {diff[0]}",
                        path=diff[0] if diff else "",
                    )


# ============================================================================
# CHAPTER PAYLOAD FIDELITY
# ============================================================================

def test_chapter_fidelity(chapters: List[ChapterRef]) -> None:
    for index, ref in enumerate(chapters, start=1):
        runtime = load_runtime_chapter(ref)

        if runtime is None:
            continue

        print(
            f"[{index:03d}/{len(chapters):03d}] "
            f"{ref.class_name} / {ref.subject_name} / "
            f"{ref.chapter_id} — {ref.chapter_uid}",
            flush=True,
        )

        api_full = assert_get(
            f"FULL_HTTP::{ref.chapter_uid}",
            f"/chapters/{urllib.parse.quote(ref.chapter_uid, safe='')}/full",
        )

        if api_full is not None:
            diff = first_difference(
                normalize(runtime),
                normalize(api_full),
            )

            record(
                f"FULL_FIDELITY::{ref.chapter_uid}",
                diff is None,
                expected=payload_summary(runtime),
                actual=payload_summary(api_full),
                detail="Exact runtime chapter payload"
                if diff is None
                else f"Mismatch at {diff[0]}",
                path=diff[0] if diff else "",
            )

        for layer in ALL_LAYERS:
            api_layer = assert_get(
                f"LAYER_HTTP::{ref.chapter_uid}::{layer}",
                f"/chapters/"
                f"{urllib.parse.quote(ref.chapter_uid, safe='')}/"
                f"{layer}",
            )

            if api_layer is None:
                continue

            expected_items = runtime.get(layer, [])

            if not isinstance(api_layer, dict):
                record(
                    f"LAYER_STRUCTURE::{ref.chapter_uid}::{layer}",
                    False,
                    expected="object with metadata + items",
                    actual=type(api_layer).__name__,
                )
                continue

            expected_metadata = {
                "id": runtime.get("id"),
                "title": runtime.get("title"),
                "classId": runtime.get("classId"),
                "subjectId": runtime.get("subjectId"),
            }

            actual_metadata = api_layer.get("metadata")
            actual_items = api_layer.get("items")

            metadata_diff = first_difference(
                normalize(expected_metadata),
                normalize(actual_metadata),
            )

            items_diff = first_difference(
                normalize(expected_items),
                normalize(actual_items),
            )

            if metadata_diff:
                record(
                    f"LAYER_METADATA_FIDELITY::{ref.chapter_uid}::{layer}",
                    False,
                    expected=payload_summary(expected_metadata),
                    actual=payload_summary(actual_metadata),
                    detail=f"Metadata mismatch at {metadata_diff[0]}",
                    path=metadata_diff[0],
                )
            else:
                record(
                    f"LAYER_METADATA_FIDELITY::{ref.chapter_uid}::{layer}",
                    True,
                    expected=payload_summary(expected_metadata),
                    actual=payload_summary(actual_metadata),
                    detail="Metadata exact",
                )

            if items_diff:
                record(
                    f"LAYER_ITEMS_FIDELITY::{ref.chapter_uid}::{layer}",
                    False,
                    expected=payload_summary(expected_items),
                    actual=payload_summary(actual_items),
                    detail=f"Items mismatch at {items_diff[0]}",
                    path=items_diff[0],
                )
            else:
                record(
                    f"LAYER_ITEMS_FIDELITY::{ref.chapter_uid}::{layer}",
                    True,
                    expected=payload_summary(expected_items),
                    actual=payload_summary(actual_items),
                    detail=f"{layer} items exact",
                )


# ============================================================================
# SEARCH FIDELITY
# ============================================================================

def choose_search_terms(records: List[Any]) -> List[Tuple[str, Optional[str]]]:
    """
    Build deterministic search probes from actual indexed content.

    Each tuple is (query, optional classId).
    """
    candidates: List[Tuple[str, Optional[str]]] = []

    stopwords = {
        "the", "and", "for", "with", "that", "this",
        "from", "what", "when", "where", "your", "have",
        "will", "into", "their", "there", "about", "which",
        "could", "would", "should", "chapter", "lesson",
    }

    seen = set()

    for item in records:
        if not isinstance(item, dict):
            continue

        class_id = item.get("class_id")
        title = str(
            item.get("chapter_title", item.get("title", ""))
        )
        text = str(item.get("text", ""))

        source = f"{title} {text}"

        words = []
        for token in source.lower().replace("/", " ").replace("-", " ").split():
            cleaned = "".join(ch for ch in token if ch.isalnum())

            if (
                len(cleaned) >= 5
                and cleaned not in stopwords
                and cleaned not in seen
            ):
                words.append(cleaned)

        for word in words[:3]:
            key = (word, class_id)

            if key not in seen:
                seen.add(key)
                candidates.append(key)

            if len(candidates) >= SEARCH_TEST_COUNT:
                return candidates

    return candidates


def expected_search(
    records: List[Any],
    query: str,
    class_id: Optional[str],
) -> List[Any]:
    q = query.lower()
    results = []

    for item in records:
        if not isinstance(item, dict):
            continue

        if class_id:
            item_class_id = str(
                item.get("class_id", "")
            ).strip().lower()

            if item_class_id != str(class_id).strip().lower():
                continue

        if (
            q in str(item.get("chapter_title", item.get("title", ""))).lower()
            or q in str(item.get("text", "")).lower()
        ):
            results.append(item)

    return results[:50]


def test_search(search_data: Dict[str, Any]) -> None:
    records = search_data["records"]

    probes = choose_search_terms(records)

    record(
        "SEARCH_PROBES_AVAILABLE",
        len(probes) > 0,
        expected=f">=1 probes",
        actual=len(probes),
        detail="Deterministic probes derived from runtime search index",
    )

    for query, class_id in probes:
        params = {
            "q": query,
        }

        if class_id:
            params["classId"] = str(class_id).lower().replace(" ", "_")

        query_string = urllib.parse.urlencode(params)

        api_results = assert_get(
            f"SEARCH_HTTP::{query}::{class_id or 'ALL'}",
            f"/search?{query_string}",
        )

        if api_results is None:
            continue

        expected = expected_search(
            records,
            query,
            params.get("classId"),
        )

        diff = first_difference(
            normalize(expected),
            normalize(api_results),
        )

        record(
            f"SEARCH_FIDELITY::{query}::{class_id or 'ALL'}",
            diff is None,
            expected=len(expected),
            actual=len(api_results)
            if isinstance(api_results, list)
            else None,
            detail="Exact search result set/order"
            if diff is None
            else f"Mismatch at {diff[0]}",
            path=diff[0] if diff else "",
        )


# ============================================================================
# DASHBOARD
# ============================================================================

def test_dashboard(catalog: Dict[str, Any]) -> None:
    api_dashboard = assert_get(
        "DASHBOARD_HTTP",
        "/dashboard/summary",
    )

    if api_dashboard is None:
        return

    expected = {
        "status": "Gurukul AI Unified API v5.0",
        "classes": {
            cls["name"]: len(cls.get("subjects", []))
            for cls in catalog.get("classes", [])
        },
        "total_classes": len(catalog.get("classes", [])),
    }

    diff = first_difference(
        normalize(expected),
        normalize(api_dashboard),
    )

    record(
        "DASHBOARD_FIDELITY",
        diff is None,
        expected=expected,
        actual=api_dashboard,
        detail="Exact dashboard payload"
        if diff is None
        else f"Mismatch at {diff[0]}",
        path=diff[0] if diff else "",
    )


# ============================================================================
# GLOBAL CONSISTENCY CHECKS
# ============================================================================

def test_catalog_runtime_consistency(
    catalog: Dict[str, Any],
    chapters: List[ChapterRef],
) -> None:
    catalog_uids = []

    for cls in catalog.get("classes", []):
        for subj in cls.get("subjects", []):
            for ch in subj.get("chapters", []):
                catalog_uids.append(str(ch["id"]))

    runtime_uids = [c.chapter_uid for c in chapters]

    catalog_set = set(catalog_uids)
    runtime_set = set(runtime_uids)

    missing_runtime = sorted(catalog_set - runtime_set)
    unexpected_runtime = sorted(runtime_set - catalog_set)

    record(
        "CATALOG_RUNTIME_UID_RECONCILIATION",
        not missing_runtime and not unexpected_runtime,
        expected=len(catalog_set),
        actual=len(runtime_set),
        detail=(
            "Catalog and runtime chapter IDs reconcile"
            if not missing_runtime and not unexpected_runtime
            else (
                f"missing_runtime={missing_runtime[:20]}, "
                f"unexpected_runtime={unexpected_runtime[:20]}"
            )
        ),
    )

    record(
        "CATALOG_UID_UNIQUENESS",
        len(catalog_uids) == len(set(catalog_uids)),
        expected="unique",
        actual=len(catalog_uids) - len(set(catalog_uids)),
        detail="Duplicate catalog chapter IDs",
    )

    record(
        "RUNTIME_UID_UNIQUENESS",
        len(runtime_uids) == len(set(runtime_uids)),
        expected="unique",
        actual=len(runtime_uids) - len(set(runtime_uids)),
        detail="Duplicate runtime chapter IDs",
    )


# ============================================================================
# REPORTING
# ============================================================================

def build_report(
    catalog: Dict[str, Any],
    chapters: List[ChapterRef],
    search_data: Dict[str, Any],
    started: float,
) -> Dict[str, Any]:

    passed = sum(1 for r in RESULTS if r.passed)
    failed = sum(1 for r in RESULTS if not r.passed)

    failures = []

    for result in RESULTS:
        if not result.passed:
            item = asdict(result)

            if len(failures) < MAX_MISMATCHES_STORED:
                failures.append(item)

    class_counts = {}
    subject_counts = {}

    for ref in chapters:
        class_counts[ref.class_name] = (
            class_counts.get(ref.class_name, 0) + 1
        )

        key = f"{ref.class_name}/{ref.subject_name}"
        subject_counts[key] = (
            subject_counts.get(key, 0) + 1
        )

    layer_counts = {
        layer: 0
        for layer in ALL_LAYERS
    }

    for ref in chapters:
        runtime = load_runtime_chapter(ref)

        if not runtime:
            continue

        for layer in ALL_LAYERS:
            value = runtime.get(layer, [])

            if isinstance(value, list):
                layer_counts[layer] += len(value)
            elif value:
                layer_counts[layer] += 1

    report = {
        "certification": {
            "name": "GURUKUL AI — COMPLETE API FIDELITY CERTIFICATION",
            "status": "API_FIDELITY_PASS" if failed == 0 else "API_FIDELITY_FAIL",
            "started_utc": START_TIME,
            "completed_utc": utc_now(),
            "duration_seconds": round(
                time.perf_counter() - started,
                3,
            ),
        },
        "api": {
            "base": API_BASE,
            "timeout_seconds": HTTP_TIMEOUT,
            "retries": HTTP_RETRIES,
        },
        "runtime": {
            "chapter_files": len(chapters),
            "classes": class_counts,
            "subjects": subject_counts,
            "search_records": len(search_data["records"]),
            "layer_record_counts": layer_counts,
        },
        "tests": {
            "total": len(RESULTS),
            "passed": passed,
            "failed": failed,
        },
        "failures": failures,
    }

    return report


def write_reports(report: Dict[str, Any]) -> None:
    with REPORT_JSON.open("w", encoding="utf-8") as f:
        json.dump(
            report,
            f,
            ensure_ascii=False,
            indent=2,
        )

    failures = report["tests"]["failed"]
    status = report["certification"]["status"]

    lines = [
        "# GURUKUL AI — COMPLETE API FIDELITY CERTIFICATION",
        "",
        f"**Status:** `{status}`",
        "",
        "## Runtime",
        "",
        f"- Runtime chapters: **{report['runtime']['chapter_files']}**",
        f"- Search records: **{report['runtime']['search_records']}**",
        "",
        "### Chapters by class",
        "",
    ]

    for name, count in report["runtime"]["classes"].items():
        lines.append(f"- {name}: **{count}**")

    lines.extend(
        [
            "",
            "### Runtime layer counts",
            "",
        ]
    )

    for layer, count in report["runtime"]["layer_record_counts"].items():
        lines.append(f"- {layer}: **{count}**")

    lines.extend(
        [
            "",
            "## Test Results",
            "",
            f"- Total tests: **{report['tests']['total']}**",
            f"- Passed: **{report['tests']['passed']}**",
            f"- Failed: **{report['tests']['failed']}**",
            "",
        ]
    )

    if failures:
        lines.extend(
            [
                "## FAILURES",
                "",
            ]
        )

        for failure in report["failures"]:
            lines.append(
                f"### `{failure['name']}`"
            )
            lines.append("")
            lines.append(
                f"- Detail: {failure.get('detail', '')}"
            )
            if failure.get("path"):
                lines.append(
                    f"- Path: `{failure['path']}`"
                )
            lines.append(
                f"- Expected: `{json.dumps(failure.get('expected'), ensure_ascii=False)}`"
            )
            lines.append(
                f"- Actual: `{json.dumps(failure.get('actual'), ensure_ascii=False)}`"
            )
            lines.append("")

    else:
        lines.extend(
            [
                "## Certification",
                "",
                "All API fidelity tests passed.",
                "",
                "The live Student API matches the certified runtime data "
                "for the tested catalog, traversal, chapter, layer, search, "
                "and dashboard contracts.",
                "",
            ]
        )

    lines.extend(
        [
            "---",
            "",
            f"API base: `{API_BASE}`",
            "",
            f"Completed: `{report['certification']['completed_utc']}`",
        ]
    )

    REPORT_MD.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


# ============================================================================
# MAIN
# ============================================================================

START_TIME = utc_now()


def main() -> int:
    started = time.perf_counter()

    print("=" * 72)
    print("GURUKUL AI — COMPLETE API FIDELITY CERTIFICATION")
    print("=" * 72)
    print()
    print(f"Repository : {REPO_ROOT}")
    print(f"Runtime    : {RUNTIME_ROOT}")
    print(f"API        : {API_BASE}")
    print()

    try:
        catalog, chapters, search_data = discover_runtime()

        print(f"Runtime chapters discovered : {len(chapters)}")
        print(f"Search records              : {len(search_data['records'])}")
        print()

        # ------------------------------------------------------------------
        # Runtime expected count.
        # ------------------------------------------------------------------
        record(
            "CERTIFIED_CHAPTER_COUNT",
            len(chapters) == 183,
            expected=183,
            actual=len(chapters),
            detail="Expected certified chapter count",
        )

        # ------------------------------------------------------------------
        # Runtime/catalog reconciliation.
        # ------------------------------------------------------------------
        print("===== CATALOG / RUNTIME CONSISTENCY =====")
        test_catalog_runtime_consistency(
            catalog,
            chapters,
        )

        # ------------------------------------------------------------------
        # Catalog and traversal.
        # ------------------------------------------------------------------
        print()
        print("===== CATALOG / CLASS / SUBJECT / CHAPTER TRAVERSAL =====")
        test_catalog(
            catalog,
            chapters,
        )

        test_traversal(
            catalog,
        )

        # ------------------------------------------------------------------
        # Every chapter, every layer.
        # ------------------------------------------------------------------
        print()
        print("===== 183-CHAPTER COMPLETE PAYLOAD FIDELITY =====")
        test_chapter_fidelity(
            chapters,
        )

        # ------------------------------------------------------------------
        # Search.
        # ------------------------------------------------------------------
        print()
        print("===== SEARCH FIDELITY =====")
        test_search(
            search_data,
        )

        # ------------------------------------------------------------------
        # Dashboard.
        # ------------------------------------------------------------------
        print()
        print("===== DASHBOARD FIDELITY =====")
        test_dashboard(
            catalog,
        )

    except Exception as exc:
        record(
            "CERTIFICATION_EXECUTION",
            False,
            expected="successful certification execution",
            actual="exception",
            detail=(
                f"{exc}\n\n"
                f"{traceback.format_exc()}"
            ),
        )

    report = build_report(
        catalog if "catalog" in locals() else {},
        chapters if "chapters" in locals() else [],
        search_data if "search_data" in locals()
        else {"records": []},
        started,
    )

    write_reports(report)

    total = report["tests"]["total"]
    passed = report["tests"]["passed"]
    failed = report["tests"]["failed"]

    print()
    print("=" * 72)
    print("FINAL API FIDELITY RESULT")
    print("=" * 72)
    print(f"Tests executed : {total}")
    print(f"Tests passed   : {passed}")
    print(f"Tests failed   : {failed}")
    print()

    if failed == 0:
        print("API_FIDELITY_PASS")
        print()
        print("All tested API responses match the certified runtime.")
    else:
        print("API_FIDELITY_FAIL")
        print()
        print("FAILURES DETECTED:")
        print()

        for failure in report["failures"][:20]:
            print(f" - {failure['name']}")
            if failure.get("detail"):
                print(f"   {failure['detail']}")
            if failure.get("path"):
                print(f"   path: {failure['path']}")

    print()
    print(f"JSON: {REPORT_JSON}")
    print(f"MD  : {REPORT_MD}")
    print("=" * 72)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

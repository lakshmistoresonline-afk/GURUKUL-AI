#!/usr/bin/env python3
"""
GURUKUL AI — CONTENTS HARDENING / NORMALIZATION ENGINE
=======================================================

AUTHORITATIVE INPUT:
    D:/GURUKUL-AI/Contents

WHAT THIS DOES
--------------
1. Reads ONLY the Contents tree.
2. Detects Class 5/6/7, subject and chapter identity from both
   paths and JSON metadata.
3. Normalizes class/subject/chapter metadata aliases.
4. Normalizes resource schemas:
      url/resource_url/resourceUrl/video_url/youtube_url
      status/verification_status
      id/resource_id/resourceId
5. Classifies resources:
      official_ncert
      official_diksha
      youtube_direct
      youtube_search
      external
      local
      invalid
      missing
6. Detects duplicate resources without deleting source records.
7. Detects placeholder/pending resource records.
8. Detects cross-class / cross-subject / cross-chapter references.
9. Detects malformed URLs.
10. Preserves provenance and source-relative paths.
11. Writes a normalized copy and detailed reports.
12. NEVER fabricates a YouTube video, ID, title, channel or URL.
13. NEVER modifies the original Contents tree unless --apply is used.
14. --apply creates a full backup before changing JSON files.

IMPORTANT:
The current audit showed:
    3309 files
    2147 JSON files
    876 resource records
    0 direct YouTube videos
    366 YouTube search URLs
    0 official NCERT/DIKSHA resource URLs
    144 invalid URLs

Therefore this script treats "PASS" for JSON syntax as NOT equivalent
to curriculum/resource quality certification.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


PROJECT_ROOT = Path(r"D:\GURUKUL-AI")
SOURCE_ROOT = PROJECT_ROOT / "Contents"
DEFAULT_OUTPUT = PROJECT_ROOT / "Contents_HARDENED"

# Generated/discovery material is not authoritative NCERT source content and
# must never be ingested into the canonical Contents normalization pass.
EXCLUDED_SOURCE_DIRS = {
    "GURUKUL_AI_CHAPTER_RESOURCE_PACK_V1",
    "Contents_HARDENED",
}
DEFAULT_REPORT = PROJECT_ROOT / "CONTENTS_HARDENING_REPORT.json"
DEFAULT_AUDIT = PROJECT_ROOT / "CONTENTS_HARDENING_AUDIT.md"

CLASS_MAP = {
    "class5": "class_5",
    "class_5": "class_5",
    "class-5": "class_5",
    "class 5": "class_5",
    "class05": "class_5",
    "class_05": "class_5",
    "class6": "class_6",
    "class_6": "class_6",
    "class-6": "class_6",
    "class 6": "class_6",
    "class06": "class_6",
    "class_06": "class_6",
    "class7": "class_7",
    "class_7": "class_7",
    "class-7": "class_7",
    "class 7": "class_7",
    "class07": "class_7",
    "class_07": "class_7",
}

RESOURCE_KEYS = {
    "resource",
    "resources",
    "resource_list",
    "resource_items",
    "resource_index",
    "multimedia",
    "videos",
    "youtube",
    "youtube_videos",
    "discovery_queries",
    "recommended_resources",
    "recommended_portals",
}

URL_KEYS = {
    "url",
    "resource_url",
    "resourceUrl",
    "video_url",
    "videoUrl",
    "youtube_url",
    "youtubeUrl",
    "link",
    "href",
    "search_url",
}

PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|PENDING|PLACEHOLDER|TO_BE_GENERATED|"
    r"TO_BE_RENDERED|MISSING_CONTENT|DERIVED_CONTENT_PENDING)\b",
    re.I,
)

YOUTUBE_WATCH_RE = re.compile(
    r"^https?://(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})(?:[&#?].*)?$",
    re.I,
)

YOUTUBE_SHORT_RE = re.compile(
    r"^https?://youtu\.be/([A-Za-z0-9_-]{11})(?:[?&#].*)?$",
    re.I,
)

YOUTUBE_SEARCH_RE = re.compile(
    r"^https?://(?:www\.)?youtube\.com/results\?search_query=",
    re.I,
)


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical_text(value):
    if not isinstance(value, str):
        return ""
    value = value.replace("\ufeff", "").replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip().lower()


def clean_string(value):
    if not isinstance(value, str):
        return value

    value = value.replace("\ufeff", "")
    value = value.replace("\u00a0", " ")
    value = re.sub(r"\bChapter\s+\d+\s*\.\s*indd\s*\d*\b", "", value, flags=re.I)
    value = re.sub(r"\bReprint\s+\d{4}(?:-\d{2})?\b", "", value, flags=re.I)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def class_from_path(path: Path):
    for part in path.parts:
        p = part.lower().strip()
        if p in CLASS_MAP:
            return CLASS_MAP[p]
        m = re.fullmatch(r"class[_ -]?0*([567])", p)
        if m:
            return f"class_{m.group(1)}"
    return None


def first_string(obj, keys):
    if not isinstance(obj, dict):
        return None
    for key in keys:
        value = obj.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def recursive_find_first(obj, keys):
    if isinstance(obj, dict):
        for key in keys:
            if key in obj and isinstance(obj[key], (str, int)):
                return obj[key]
        for value in obj.values():
            found = recursive_find_first(value, keys)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = recursive_find_first(value, keys)
            if found is not None:
                return found
    return None


def subject_from_path(path: Path):
    for part in path.parts:
        if re.match(r"^\d{2}[_-]", part):
            return part
    return None


def subject_from_data(data):
    value = recursive_find_first(
        data,
        {
            "subject_id",
            "subjectId",
            "subject_uid",
            "subjectUid",
        },
    )
    return str(value) if value is not None else None


def chapter_from_path(path: Path):
    for part in reversed(path.parts):
        m = re.search(
            r"(?:chapter[_-]?)?(\d{3,5})(?:[_-]|$)",
            part,
            re.I,
        )
        if m:
            return m.group(1)
    return None


def chapter_from_data(data):
    value = recursive_find_first(
        data,
        {
            "chapter_id",
            "chapterId",
            "chapter_uid",
            "chapterUid",
            "chapterID",
        },
    )
    if value is None:
        return None

    s = str(value)
    m = re.search(r"(?:chapter[_-]?)?(\d{3,5})(?:$|[_-])", s, re.I)
    return m.group(1) if m else None


def title_from_path(path: Path):
    for part in reversed(path.parts):
        m = re.match(r"(?:chapter[_-]?\d{3,5}[_-])(.+)", part, re.I)
        if m:
            return clean_string(m.group(1).replace("_", " "))
    return None


def title_from_data(data):
    value = recursive_find_first(
        data,
        {
            "chapter_title",
            "chapterTitle",
            "chapter_name",
            "chapterName",
            "title",
        },
    )
    return clean_string(str(value)) if value is not None else None


def identity(path: Path, data):
    cls = class_from_path(path) or recursive_find_first(
        data, {"class_id", "classId", "class_uid", "classUid"}
    )
    subject = subject_from_path(path) or subject_from_data(data)
    chapter = chapter_from_path(path) or chapter_from_data(data)
    title = title_from_data(data) or title_from_path(path)

    return {
        "class_id": str(cls).lower() if cls else None,
        "subject_id": str(subject).lower() if subject else None,
        "chapter_id": str(chapter) if chapter else None,
        "chapter_title": title,
    }


def is_url(value):
    if not isinstance(value, str):
        return False
    try:
        p = urlparse(value.strip())
    except Exception:
        return False
    return p.scheme in {"http", "https"} and bool(p.netloc)


def youtube_info(url):
    if not isinstance(url, str):
        return None, None

    url = url.strip()

    m = YOUTUBE_WATCH_RE.match(url)
    if m:
        return "youtube_direct", m.group(1)

    m = YOUTUBE_SHORT_RE.match(url)
    if m:
        return "youtube_direct", m.group(1)

    if YOUTUBE_SEARCH_RE.match(url):
        return "youtube_search", None

    return None, None


def classify_url(url):
    if not isinstance(url, str) or not url.strip():
        return "missing"

    url = url.strip()

    yt_type, yt_id = youtube_info(url)
    if yt_type:
        return yt_type

    if not is_url(url):
        return "invalid"

    host = urlparse(url).netloc.lower()

    if "ncert.nic.in" in host:
        return "official_ncert"

    if "diksha.gov.in" in host:
        return "official_diksha"

    return "external"


def likely_placeholder(value):
    if isinstance(value, str):
        return bool(PLACEHOLDER_RE.search(value))
    if isinstance(value, (dict, list)):
        return bool(PLACEHOLDER_RE.search(
            json.dumps(value, ensure_ascii=False)
        ))
    return False


def looks_like_resource_dict(obj):
    if not isinstance(obj, dict):
        return False

    keys = {k.lower() for k in obj.keys()}

    return bool(
        keys.intersection(
            {
                "url",
                "resource_url",
                "resourceurl",
                "video_url",
                "youtube_url",
                "title",
                "resource_id",
                "resourceid",
                "verification_status",
                "status",
                "search_url",
            }
        )
    )


def collect_resource_objects(obj, path=""):
    found = []

    if isinstance(obj, dict):
        for key, value in obj.items():
            lk = key.lower()

            if lk in RESOURCE_KEYS:
                if isinstance(value, list):
                    for i, item in enumerate(value):
                        if isinstance(item, dict):
                            found.append((item, f"{path}.{key}[{i}]"))
                        elif isinstance(item, str):
                            found.append(
                                ({"url": item}, f"{path}.{key}[{i}]")
                            )
                elif isinstance(value, dict):
                    if looks_like_resource_dict(value):
                        found.append((value, f"{path}.{key}"))

            elif looks_like_resource_dict(value):
                found.append((value, f"{path}.{key}"))

            found.extend(
                collect_resource_objects(value, f"{path}.{key}")
            )

    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            found.extend(
                collect_resource_objects(item, f"{path}[{i}]")
            )

    return found


def normalize_resource(resource, chapter_identity, source_rel):
    original = copy.deepcopy(resource)

    url = first_string(
        resource,
        [
            "url",
            "resource_url",
            "resourceUrl",
            "video_url",
            "videoUrl",
            "youtube_url",
            "youtubeUrl",
            "link",
            "href",
            "search_url",
        ],
    )

    title = first_string(
        resource,
        ["title", "name", "label", "resource_title"],
    )

    rid = first_string(
        resource,
        ["resource_id", "resourceId", "id", "uid"],
    )

    status = first_string(
        resource,
        [
            "verification_status",
            "verificationStatus",
            "status",
        ],
    )

    rtype = first_string(
        resource,
        ["type", "resource_type", "resourceType", "content_type"],
    )

    url_type = classify_url(url)
    yt_type, yt_id = youtube_info(url)

    normalized = {
        "resource_id": rid,
        "title": clean_string(title) if title else None,
        "url": url.strip() if isinstance(url, str) else url,
        "resource_type": rtype,
        "verification_status": status,
        "url_type": url_type,
        "youtube_video_id": yt_id,
        "is_direct_youtube": yt_type == "youtube_direct",
        "is_youtube_search": yt_type == "youtube_search",
        "is_official": url_type in {
            "official_ncert",
            "official_diksha",
        },
        "is_placeholder": likely_placeholder(original),
        "source_relative_file": source_rel,
        "class_id": chapter_identity["class_id"],
        "subject_id": chapter_identity["subject_id"],
        "chapter_id": chapter_identity["chapter_id"],
        "original": original,
    }

    return normalized


def walk_clean(value):
    if isinstance(value, str):
        return clean_string(value)
    if isinstance(value, list):
        return [walk_clean(v) for v in value]
    if isinstance(value, dict):
        return {k: walk_clean(v) for k, v in value.items()}
    return value


def inject_canonical_metadata(data, ident, source_rel):
    if not isinstance(data, dict):
        return data

    data = walk_clean(data)

    if ident["class_id"]:
        data["class_id"] = data.get("class_id") or ident["class_id"]
        data["classId"] = data.get("classId") or data["class_id"]

    if ident["subject_id"]:
        data["subject_id"] = data.get("subject_id") or ident["subject_id"]
        data["subjectId"] = data.get("subjectId") or data["subject_id"]

    if ident["chapter_id"]:
        data["chapter_id"] = data.get("chapter_id") or ident["chapter_id"]
        data["chapterId"] = data.get("chapterId") or data["chapter_id"]

    if ident["chapter_title"]:
        data["chapter_title"] = (
            data.get("chapter_title") or ident["chapter_title"]
        )

    gurukul = data.get("_gurukul")
    if not isinstance(gurukul, dict):
        gurukul = {}

    gurukul.update(
        {
            "schema_version": "GURUKUL_CONTENT_HARDENED_1.0",
            "source_relative_file": source_rel,
            "class_id": ident["class_id"],
            "subject_id": ident["subject_id"],
            "chapter_id": ident["chapter_id"],
            "chapter_title": ident["chapter_title"],
        }
    )

    data["_gurukul"] = gurukul

    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=str(SOURCE_ROOT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--audit", default=str(DEFAULT_AUDIT))
    parser.add_argument(
        "--apply",
        action="store_true",
        help="After successful validation, replace JSON files in Contents."
    )
    parser.add_argument(
        "--no-copy-media",
        action="store_true",
        help="Do not copy non-JSON files into the hardened output."
    )
    args = parser.parse_args()

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()

    if source != SOURCE_ROOT.resolve():
        raise SystemExit(
            "SAFETY STOP: This hardening script is intentionally locked "
            "to D:\\GURUKUL-AI\\Contents unless --source is explicitly changed."
        )

    if not source.is_dir():
        raise SystemExit(f"Missing source: {source}")

    if output == source:
        raise SystemExit("SAFETY STOP: output cannot equal Contents.")

    output.mkdir(parents=True, exist_ok=True)

    files = [
        p for p in source.rglob("*")
        if p.is_file()
        and not any(part in EXCLUDED_SOURCE_DIRS for part in p.relative_to(source).parts)
    ]

    json_files = sorted(
        p for p in files
        if p.suffix.lower() == ".json"
    )

    report = {
        "schema_version": "GURUKUL_CONTENTS_HARDENING_REPORT_1.0",
        "started_at": now(),
        "source_root": str(source),
        "output_root": str(output),
        "source_modified": False,
        "files": len(files),
        "json_files": len(json_files),
        "invalid_json": [],
        "identity": {
            "missing_class": [],
            "missing_subject": [],
            "missing_chapter": [],
            "missing_title": [],
        },
        "resources": {
            "total": 0,
            "official_ncert": 0,
            "official_diksha": 0,
            "direct_youtube": 0,
            "youtube_search": 0,
            "external": 0,
            "local": 0,
            "invalid": 0,
            "missing": 0,
            "placeholders": 0,
            "duplicates": 0,
        },
        "cross_identity": [],
        "duplicate_resource_records": [],
        "invalid_urls": [],
        "placeholder_records": [],
        "chapter_matrix": [],
        "classes": Counter(),
        "subjects": Counter(),
        "chapters": Counter(),
    }

    if not args.no_copy_media:
        for file in files:
            if file.suffix.lower() == ".json":
                continue
            rel = file.relative_to(source)
            dest = output / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)

    chapter_resources = defaultdict(list)

    for i, path in enumerate(json_files, 1):
        rel = path.relative_to(source)
        print(f"[{i}/{len(json_files)}] {rel}")

        try:
            data = json.loads(
                path.read_text(encoding="utf-8-sig")
            )
        except Exception as exc:
            report["invalid_json"].append(
                {"file": str(rel), "error": str(exc)}
            )
            continue

        ident = identity(path, data)

        if ident["class_id"]:
            report["classes"][ident["class_id"]] += 1
        else:
            report["identity"]["missing_class"].append(str(rel))

        if ident["subject_id"]:
            report["subjects"][ident["subject_id"]] += 1
        else:
            report["identity"]["missing_subject"].append(str(rel))

        if ident["chapter_id"]:
            report["chapters"][
                f"{ident['class_id']}:{ident['subject_id']}"
            ] += 1
        else:
            report["identity"]["missing_chapter"].append(str(rel))

        if not ident["chapter_title"]:
            report["identity"]["missing_title"].append(str(rel))

        normalized = inject_canonical_metadata(
            data,
            ident,
            str(rel),
        )

        raw_resources = collect_resource_objects(normalized)

        seen = {}

        for resource, resource_path in raw_resources:
            nr = normalize_resource(
                resource,
                ident,
                str(rel),
            )

            report["resources"]["total"] += 1

            kind = nr["url_type"]
            if kind in report["resources"]:
                report["resources"][kind] += 1

            if nr["is_placeholder"]:
                report["resources"]["placeholders"] += 1
                report["placeholder_records"].append(
                    {
                        "file": str(rel),
                        "path": resource_path,
                        "title": nr["title"],
                    }
                )

            if kind == "invalid":
                report["resources"]["invalid"] += 1
                report["invalid_urls"].append(
                    {
                        "file": str(rel),
                        "path": resource_path,
                        "url": nr["url"],
                    }
                )

            identity_key = (
                nr["url"]
                or nr["resource_id"]
                or canonical_text(nr["title"])
            )

            if identity_key:
                if identity_key in seen:
                    report["resources"]["duplicates"] += 1
                    report["duplicate_resource_records"].append(
                        {
                            "file": str(rel),
                            "first_path": seen[identity_key],
                            "duplicate_path": resource_path,
                            "identity": identity_key,
                        }
                    )
                else:
                    seen[identity_key] = resource_path

            # Resource identity must match the containing chapter.
            mismatches = []

            if nr["class_id"] and ident["class_id"]:
                if nr["class_id"].lower() != ident["class_id"].lower():
                    mismatches.append("class_id")

            if nr["subject_id"] and ident["subject_id"]:
                if nr["subject_id"].lower() != ident["subject_id"].lower():
                    mismatches.append("subject_id")

            if nr["chapter_id"] and ident["chapter_id"]:
                if str(nr["chapter_id"]) != str(ident["chapter_id"]):
                    mismatches.append("chapter_id")

            if mismatches:
                report["cross_identity"].append(
                    {
                        "file": str(rel),
                        "resource_path": resource_path,
                        "mismatches": mismatches,
                        "resource": nr,
                    }
                )

            if ident["chapter_id"]:
                key = (
                    ident["class_id"],
                    ident["subject_id"],
                    ident["chapter_id"],
                )
                chapter_resources[key].append(nr)

        # Write normalized JSON.
        dest = output / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            json.dumps(
                normalized,
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )

    # --------------------------------------------------------
    # Chapter matrix
    # --------------------------------------------------------

    for key in sorted(chapter_resources, key=lambda k: tuple("" if v is None else str(v) for v in k)):
        cls, subject, chapter = key
        rs = chapter_resources[key]

        unique_urls = {
            r["url"]
            for r in rs
            if r["url"]
        }

        report["chapter_matrix"].append(
            {
                "class_id": cls,
                "subject_id": subject,
                "chapter_id": chapter,
                "resource_count": len(rs),
                "unique_url_count": len(unique_urls),
                "official_ncert": sum(
                    r["url_type"] == "official_ncert"
                    for r in rs
                ),
                "official_diksha": sum(
                    r["url_type"] == "official_diksha"
                    for r in rs
                ),
                "direct_youtube": sum(
                    r["url_type"] == "youtube_direct"
                    for r in rs
                ),
                "youtube_search": sum(
                    r["url_type"] == "youtube_search"
                    for r in rs
                ),
                "external": sum(
                    r["url_type"] == "external"
                    for r in rs
                ),
                "invalid": sum(
                    r["url_type"] == "invalid"
                    for r in rs
                ),
                "placeholders": sum(
                    r["is_placeholder"]
                    for r in rs
                ),
            }
        )

    report["classes"] = dict(report["classes"])
    report["subjects"] = dict(report["subjects"])
    report["chapters"] = dict(report["chapters"])

    # --------------------------------------------------------
    # Hard gates
    # --------------------------------------------------------

    total_chapters = len(report["chapter_matrix"])

    class_chapter_counts = Counter(
        x["class_id"]
        for x in report["chapter_matrix"]
    )

    expected = {
        "class_5": 47,
        "class_6": 64,
        "class_7": 72,
    }

    gates = {
        "source_protection": True,
        "json_validity": len(report["invalid_json"]) == 0,
        "class_coverage": all(
            class_chapter_counts.get(k, 0) == v
            for k, v in expected.items()
        ),
        "cross_identity": len(report["cross_identity"]) == 0,
        "placeholder_resources": (
            report["resources"]["placeholders"] == 0
        ),
    }

    # Resource quality is intentionally NOT allowed to pass merely
    # because JSON is syntactically valid.
    gates["resource_quality"] = (
        report["resources"]["invalid"] == 0
        and report["resources"]["duplicates"] == 0
        and report["resources"]["placeholders"] == 0
    )

    report["gates"] = gates
    report["chapter_count"] = total_chapters
    report["class_chapter_counts"] = dict(class_chapter_counts)

    report["status"] = (
        "READY_FOR_REVIEW"
        if all(gates.values())
        else "HARDENING_REQUIRED"
    )

    report["finished_at"] = now()

    Path(args.report).write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Human-readable audit
    # --------------------------------------------------------

    lines = [
        "# GURUKUL AI Contents Hardening Audit",
        "",
        f"Generated: {now()}",
        "",
        "## Authoritative source",
        "",
        f"`{source}`",
        "",
        "## Safety",
        "",
        f"- Source modified during analysis: **{report['source_modified']}**",
        f"- Normalized output: `{output}`",
        "",
        "## Inventory",
        "",
        f"- Files: **{len(files)}**",
        f"- JSON files: **{len(json_files)}**",
        f"- Chapters discovered: **{total_chapters}**",
        "",
        "## Class coverage",
        "",
    ]

    for cls in ("class_5", "class_6", "class_7"):
        lines.append(
            f"- {cls}: {class_chapter_counts.get(cls, 0)} "
            f"/ {expected[cls]}"
        )

    lines.extend(
        [
            "",
            "## Resources",
            "",
            f"- Total resource records: **{report['resources']['total']}**",
            f"- Direct YouTube: **{report['resources']['direct_youtube']}**",
            f"- YouTube search URLs: **{report['resources']['youtube_search']}**",
            f"- NCERT: **{report['resources']['official_ncert']}**",
            f"- DIKSHA: **{report['resources']['official_diksha']}**",
            f"- External: **{report['resources']['external']}**",
            f"- Invalid URLs: **{report['resources']['invalid']}**",
            f"- Placeholders: **{report['resources']['placeholders']}**",
            f"- Duplicate records: **{report['resources']['duplicates']}**",
            "",
            "## Hard gates",
            "",
        ]
    )

    for gate, passed in gates.items():
        lines.append(
            f"- {gate}: **{'PASS' if passed else 'FAIL'}**"
        )

    lines.extend(
        [
            "",
            "## Overall",
            "",
            f"**{report['status']}**",
            "",
            "No YouTube IDs, video URLs or external learning resources "
            "were fabricated by this script.",
            "",
        ]
    )

    Path(args.audit).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # Optional apply
    # --------------------------------------------------------

    if args.apply:
        if report["status"] != "READY_FOR_REVIEW":
            raise SystemExit(
                "APPLY ABORTED: hard gates did not pass. "
                "Review the report first."
            )

        backup = PROJECT_ROOT / (
            "Contents_BACKUP_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
        )

        backup.mkdir(parents=True, exist_ok=False)

        for path in json_files:
            rel = path.relative_to(source)
            dest = backup / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)

        for path in json_files:
            rel = path.relative_to(source)
            normalized = output / rel
            shutil.copy2(normalized, path)

        report["source_modified"] = True
        report["backup"] = str(backup)
        report["status"] = "APPLIED"

        Path(args.report).write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print("")
    print("=" * 70)
    print("GURUKUL AI CONTENTS HARDENING")
    print("=" * 70)
    print(f"Source       : {source}")
    print(f"Output       : {output}")
    print(f"Files        : {len(files)}")
    print(f"JSON         : {len(json_files)}")
    print(f"Chapters     : {total_chapters}")
    print(f"Direct YT    : {report['resources']['direct_youtube']}")
    print(f"YT searches  : {report['resources']['youtube_search']}")
    print(f"NCERT        : {report['resources']['official_ncert']}")
    print(f"DIKSHA       : {report['resources']['official_diksha']}")
    print(f"Invalid URLs : {report['resources']['invalid']}")
    print(f"Cross ID     : {len(report['cross_identity'])}")
    print(f"Status       : {report['status']}")
    print("=" * 70)


if __name__ == "__main__":
    main()

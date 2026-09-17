from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


# ============================================================
# GURUKUL AI
# CONTENTS NORMALIZATION + RESOURCE HARDENING ENGINE
#
# AUTHORITATIVE INPUT:
#     D:\GURUKUL-AI\Contents
#
# IMPORTANT:
#     Original Contents is NEVER modified by default.
#
# OUTPUT:
#     D:\GURUKUL-AI\Contents_NORMALIZED
#
# VALIDATION:
#     D:\GURUKUL-AI\Contents_NORMALIZATION_REPORT.json
#
# ============================================================


SOURCE_ROOT = Path(r"D:\GURUKUL-AI\Contents")
PROJECT_ROOT = SOURCE_ROOT.parent
OUTPUT_ROOT = PROJECT_ROOT / "Contents_NORMALIZED"
REPORT_PATH = PROJECT_ROOT / "Contents_NORMALIZATION_REPORT.json"
AUDIT_PATH = PROJECT_ROOT / "Contents_NORMALIZATION_AUDIT.md"


SUPPORTED_CLASSES = {
    "class_5": "class_5",
    "class_05": "class_5",
    "class5": "class_5",
    "class-5": "class_5",
    "class 5": "class_5",

    "class_6": "class_6",
    "class_06": "class_6",
    "class6": "class_6",
    "class-6": "class_6",
    "class 6": "class_6",

    "class_7": "class_7",
    "class_07": "class_7",
    "class7": "class_7",
    "class-7": "class_7",
    "class 7": "class_7",
}


TEXT_EXTENSIONS = {
    ".json",
    ".jsonl",
    ".txt",
    ".md",
    ".csv",
    ".yaml",
    ".yml",
    ".xml",
    ".html",
    ".htm",
}


MEDIA_EXTENSIONS = {
    ".mp4",
    ".webm",
    ".mov",
    ".mkv",
    ".avi",
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".pdf",
}


PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bPENDING\b",
    r"\bPLACEHOLDER\b",
    r"\bTO_BE_GENERATED\b",
    r"\bTO_BE_RENDERED\b",
    r"\bMISSING_CONTENT\b",
    r"\bDERIVED_CONTENT_PENDING\b",
]


YOUTUBE_DIRECT_PATTERNS = [
    r"https?://(?:www\.)?youtube\.com/watch\?v=[A-Za-z0-9_-]{11}",
    r"https?://youtu\.be/[A-Za-z0-9_-]{11}",
]


YOUTUBE_SEARCH_PATTERN = (
    r"https?://(?:www\.)?youtube\.com/results\?search_query="
)


# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()

    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return h.hexdigest()


def clean_text(value):
    if not isinstance(value, str):
        return value

    value = value.replace("\ufeff", "")
    value = value.replace("\u00a0", " ")

    # Remove obvious InDesign artifacts.
    value = re.sub(
        r"\bChapter\s+\d+\s*\.\s*indd\s*\d*\b",
        "",
        value,
        flags=re.I,
    )

    # Remove common reprint markers.
    value = re.sub(
        r"\bReprint\s+\d{4}(?:-\d{2})?\b",
        "",
        value,
        flags=re.I,
    )

    # Normalize whitespace without destroying paragraph breaks.
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)

    return value.strip()


def canonical_key(value) -> str:
    if not isinstance(value, str):
        return ""

    value = clean_text(value).lower()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^\w\s]", "", value)

    return value.strip()


def classify_url(url: str) -> str:
    if not isinstance(url, str):
        return "invalid"

    url = url.strip()

    if not url:
        return "missing"

    try:
        parsed = urlparse(url)
    except Exception:
        return "invalid"

    if parsed.scheme not in {"http", "https"}:
        return "invalid"

    host = (parsed.netloc or "").lower()

    if "youtube.com" in host or "youtu.be" in host:
        if re.search(YOUTUBE_DIRECT_PATTERNS[0], url, re.I):
            return "youtube_direct"

        if re.search(YOUTUBE_DIRECT_PATTERNS[1], url, re.I):
            return "youtube_direct"

        if re.search(YOUTUBE_SEARCH_PATTERN, url, re.I):
            return "youtube_search"

        return "youtube_other"

    if "diksha.gov.in" in host:
        return "official_diksha"

    if "ncert.nic.in" in host:
        return "official_ncert"

    return "external"


def looks_like_placeholder(value) -> bool:
    if not isinstance(value, str):
        return False

    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, value, re.I):
            return True

    return False


def find_class(path: Path) -> str | None:

    for part in path.parts:

        normalized = part.lower().strip()

        if normalized in SUPPORTED_CLASSES:
            return SUPPORTED_CLASSES[normalized]

        m = re.match(r"class[_ -]?0*([567])$", normalized)

        if m:
            return f"class_{m.group(1)}"

    return None


def find_chapter_id(path: Path, obj=None) -> str | None:

    if isinstance(obj, dict):

        for key in (
            "chapter_id",
            "chapterId",
            "chapter_uid",
            "chapterUid",
            "chapterID",
            "id",
        ):

            value = obj.get(key)

            if isinstance(value, str):

                m = re.search(
                    r"(?:chapter[_-]?)?(\d{3,5})",
                    value,
                    re.I,
                )

                if m:
                    return m.group(1)

    for part in reversed(path.parts):

        m = re.search(
            r"(?:chapter[_-]?)?(\d{3,5})(?:[_-]|$)",
            part,
            re.I,
        )

        if m:
            return m.group(1)

    return None


def find_subject(path: Path) -> str | None:

    for part in path.parts:

        if re.match(r"^\d{2}[_-]", part):

            return part

    return None


def find_chapter_title(path: Path, obj=None) -> str | None:

    if isinstance(obj, dict):

        for key in (
            "chapter_title",
            "chapterTitle",
            "title",
            "name",
            "chapter_name",
        ):

            value = obj.get(key)

            if isinstance(value, str) and value.strip():
                return clean_text(value)

    # Extract from directory names.
    for part in reversed(path.parts):

        m = re.match(
            r"(?:chapter[_-]?\d{3,5}[_-])(.+)",
            part,
            re.I,
        )

        if m:
            return clean_text(
                m.group(1).replace("_", " ")
            )

    return None


# ------------------------------------------------------------
# Resource extraction
# ------------------------------------------------------------

def resource_like(obj) -> bool:

    if not isinstance(obj, dict):
        return False

    keys = {
        "url",
        "resource_url",
        "resourceUrl",
        "video_url",
        "youtube_url",
        "title",
        "resource_id",
        "resourceId",
        "verification_status",
        "status",
    }

    return bool(keys.intersection(obj.keys()))


def extract_resources(obj, path=""):

    resources = []

    if isinstance(obj, dict):

        for key, value in obj.items():

            lower = key.lower()

            if lower in {
                "resources",
                "resource",
                "resource_list",
                "resource_items",
                "resource_index",
                "multimedia",
                "videos",
                "youtube",
                "youtube_videos",
            }:

                if isinstance(value, list):

                    for item in value:

                        if isinstance(item, dict):
                            resources.append(copy.deepcopy(item))

                        elif isinstance(item, str):
                            resources.append({
                                "url": item
                            })

                elif isinstance(value, dict):

                    if resource_like(value):
                        resources.append(copy.deepcopy(value))

            elif resource_like(value):

                resources.append(copy.deepcopy(value))

            resources.extend(
                extract_resources(
                    value,
                    f"{path}.{key}",
                )
            )

    elif isinstance(obj, list):

        for index, item in enumerate(obj):

            resources.extend(
                extract_resources(
                    item,
                    f"{path}[{index}]",
                )
            )

    return resources


def normalize_resource(resource):

    if not isinstance(resource, dict):
        resource = {"value": resource}

    result = copy.deepcopy(resource)

    title = (
        result.get("title")
        or result.get("name")
        or result.get("label")
        or result.get("description")
    )

    url = (
        result.get("url")
        or result.get("resource_url")
        or result.get("resourceUrl")
        or result.get("video_url")
        or result.get("youtube_url")
    )

    status = (
        result.get("verification_status")
        or result.get("verificationStatus")
        or result.get("status")
    )

    resource_id = (
        result.get("resource_id")
        or result.get("resourceId")
        or result.get("id")
    )

    normalized = {
        "resource_id": resource_id,
        "title": clean_text(title) if title else None,
        "url": url,
        "verification_status": status,
        "resource_type": result.get(
            "type",
            result.get("resource_type")
        ),
        "purpose": result.get("purpose"),
        "description": clean_text(
            result.get("description")
        ) if result.get("description") else None,
        "source": result.get("source"),
        "original": result,
    }

    url_type = classify_url(url)

    normalized["url_type"] = url_type

    normalized["is_direct_youtube"] = (
        url_type == "youtube_direct"
    )

    normalized["is_youtube_search"] = (
        url_type == "youtube_search"
    )

    normalized["is_official"] = (
        url_type in {
            "official_ncert",
            "official_diksha",
        }
    )

    normalized["is_placeholder"] = (
        looks_like_placeholder(
            json.dumps(result, ensure_ascii=False)
        )
    )

    return normalized


# ------------------------------------------------------------
# JSON normalization
# ------------------------------------------------------------

def normalize_json_object(
    data,
    relative_path: str,
    source_path: Path,
):

    class_id = find_class(source_path)
    subject_id = find_subject(source_path)
    chapter_id = find_chapter_id(
        source_path,
        data,
    )
    chapter_title = find_chapter_title(
        source_path,
        data,
    )

    if isinstance(data, dict):

        normalized = copy.deepcopy(data)

        # Canonical metadata aliases.
        if class_id:
            normalized["class_id"] = (
                normalized.get("class_id")
                or class_id
            )

            normalized["classId"] = (
                normalized.get("classId")
                or normalized["class_id"]
            )

        if subject_id:
            normalized["subject_id"] = (
                normalized.get("subject_id")
                or subject_id
            )

            normalized["subjectId"] = (
                normalized.get("subjectId")
                or normalized["subject_id"]
            )

        if chapter_id:
            normalized["chapter_id"] = (
                normalized.get("chapter_id")
                or chapter_id
            )

            normalized["chapterId"] = (
                normalized.get("chapterId")
                or normalized["chapter_id"]
            )

        if chapter_title:
            normalized["chapter_title"] = (
                normalized.get("chapter_title")
                or chapter_title
            )

        # Preserve recursively cleaned strings.
        def clean_recursive(value):

            if isinstance(value, str):
                return clean_text(value)

            if isinstance(value, list):
                return [
                    clean_recursive(x)
                    for x in value
                ]

            if isinstance(value, dict):
                return {
                    k: clean_recursive(v)
                    for k, v in value.items()
                }

            return value

        normalized = clean_recursive(normalized)

        resources = extract_resources(normalized)

        normalized_resources = []

        seen = set()

        for resource in resources:

            nr = normalize_resource(resource)

            dedupe_basis = (
                nr.get("url")
                or nr.get("resource_id")
                or canonical_key(
                    nr.get("title")
                )
            )

            if not dedupe_basis:
                dedupe_basis = hashlib.sha1(
                    json.dumps(
                        nr,
                        sort_keys=True,
                        ensure_ascii=False,
                    ).encode("utf-8")
                ).hexdigest()

            if dedupe_basis in seen:
                continue

            seen.add(dedupe_basis)

            normalized_resources.append(nr)

        normalized["_gurukul"] = {
            "normalization_version": "1.0",
            "normalized_at": now_iso(),
            "source_relative_path": relative_path,
            "class_id": class_id,
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "chapter_title": chapter_title,
            "resource_count": len(
                normalized_resources
            ),
            "direct_youtube_count": sum(
                1 for r in normalized_resources
                if r["is_direct_youtube"]
            ),
            "youtube_search_count": sum(
                1 for r in normalized_resources
                if r["is_youtube_search"]
            ),
            "official_resource_count": sum(
                1 for r in normalized_resources
                if r["is_official"]
            ),
            "placeholder_count": sum(
                1 for r in normalized_resources
                if r["is_placeholder"]
            ),
        }

        if normalized_resources:
            normalized["_gurukul"][
                "normalized_resources"
            ] = normalized_resources

        return normalized

    return data


# ------------------------------------------------------------
# Main processing
# ------------------------------------------------------------

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        default=str(SOURCE_ROOT),
    )

    parser.add_argument(
        "--output",
        default=str(OUTPUT_ROOT),
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Replace JSON files in Contents after "
            "successful validation. "
            "A backup is created first."
        ),
    )

    parser.add_argument(
        "--no-copy-media",
        action="store_true",
        help=(
            "Do not copy non-JSON files into "
            "Contents_NORMALIZED."
        ),
    )

    args = parser.parse_args()

    source = Path(args.source).resolve()
    output = Path(args.output).resolve()

    if not source.exists():
        raise SystemExit(
            f"SOURCE DOES NOT EXIST: {source}"
        )

    # --------------------------------------------------------
    # HARD SAFETY CHECK
    # --------------------------------------------------------

    if source.name.lower() != "contents":
        raise SystemExit(
            "SAFETY STOP: source must be the Contents folder."
        )

    if source == output:
        raise SystemExit(
            "SAFETY STOP: output cannot equal source."
        )

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_files = sorted(
        source.rglob("*.json")
    )

    all_files = sorted(
        p for p in source.rglob("*")
        if p.is_file()
    )

    report = {
        "status": "RUNNING",
        "started_at": now_iso(),
        "source_root": str(source),
        "output_root": str(output),
        "source_modified": False,
        "files": len(all_files),
        "json_files": len(json_files),
        "classes": Counter(),
        "subjects": Counter(),
        "chapters": Counter(),
        "resources": 0,
        "direct_youtube": 0,
        "youtube_search": 0,
        "official_resources": 0,
        "placeholder_resources": 0,
        "invalid_urls": 0,
        "duplicate_resources_removed": 0,
        "invalid_json": [],
        "errors": [],
        "files_changed": [],
    }

    chapter_manifest = defaultdict(
        lambda: {
            "class_id": None,
            "subject_id": None,
            "chapter_id": None,
            "chapter_title": None,
            "files": [],
            "resources": [],
        }
    )

    # --------------------------------------------------------
    # COPY NON-JSON FILES
    # --------------------------------------------------------

    if not args.no_copy_media:

        for file in all_files:

            if file.suffix.lower() == ".json":
                continue

            relative = file.relative_to(source)
            destination = output / relative

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                file,
                destination,
            )

    # --------------------------------------------------------
    # PROCESS JSON
    # --------------------------------------------------------

    for index, json_file in enumerate(json_files, 1):

        relative = json_file.relative_to(source)

        print(
            f"[{index}/{len(json_files)}] "
            f"{relative}"
        )

        class_id = find_class(json_file)
        subject_id = find_subject(json_file)

        if class_id:
            report["classes"][class_id] += 1

        if subject_id:
            report["subjects"][subject_id] += 1

        try:

            raw = json_file.read_text(
                encoding="utf-8-sig"
            )

            data = json.loads(raw)

        except Exception as exc:

            report["invalid_json"].append({
                "file": str(relative),
                "error": str(exc),
            })

            continue

        normalized = normalize_json_object(
            data,
            str(relative),
            json_file,
        )

        chapter_id = find_chapter_id(
            json_file,
            normalized,
        )

        chapter_title = find_chapter_title(
            json_file,
            normalized,
        )

        if chapter_id:
            report["chapters"][
                f"{class_id}:{subject_id}"
            ] += 1

        resources = extract_resources(
            normalized
        )

        normalized_resources = [
            normalize_resource(r)
            for r in resources
        ]

        report["resources"] += len(
            normalized_resources
        )

        report["direct_youtube"] += sum(
            1
            for r in normalized_resources
            if r["is_direct_youtube"]
        )

        report["youtube_search"] += sum(
            1
            for r in normalized_resources
            if r["is_youtube_search"]
        )

        report["official_resources"] += sum(
            1
            for r in normalized_resources
            if r["is_official"]
        )

        report["placeholder_resources"] += sum(
            1
            for r in normalized_resources
            if r["is_placeholder"]
        )

        for resource in normalized_resources:

            if resource["url_type"] == "invalid":
                report["invalid_urls"] += 1

        if chapter_id:

            key = (
                class_id,
                subject_id,
                chapter_id,
            )

            chapter = chapter_manifest[key]

            chapter["class_id"] = class_id
            chapter["subject_id"] = subject_id
            chapter["chapter_id"] = chapter_id
            chapter["chapter_title"] = chapter_title

            chapter["files"].append(
                str(relative)
            )

            chapter["resources"].extend(
                normalized_resources
            )

        # Write normalized JSON.
        destination = output / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_text(
            json.dumps(
                normalized,
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )

    # --------------------------------------------------------
    # CHAPTER MANIFEST
    # --------------------------------------------------------

    chapters_output = []

    for key, chapter in sorted(
        chapter_manifest.items(),
        key=lambda x: str(x[0]),
    ):

        unique_resources = []

        seen = set()

        for resource in chapter["resources"]:

            identity = (
                resource.get("url")
                or resource.get("resource_id")
                or canonical_key(
                    resource.get("title")
                )
            )

            if identity in seen:
                continue

            seen.add(identity)

            unique_resources.append(resource)

        chapter["resources"] = unique_resources

        chapter["resource_summary"] = {
            "total": len(unique_resources),
            "official": sum(
                r["is_official"]
                for r in unique_resources
            ),
            "direct_youtube": sum(
                r["is_direct_youtube"]
                for r in unique_resources
            ),
            "youtube_search": sum(
                r["is_youtube_search"]
                for r in unique_resources
            ),
            "invalid": sum(
                r["url_type"] == "invalid"
                for r in unique_resources
            ),
            "placeholders": sum(
                r["is_placeholder"]
                for r in unique_resources
            ),
        }

        chapters_output.append(chapter)

    manifest = {
        "schema_version": "GURUKUL_RESOURCE_MANIFEST_1.0",
        "generated_at": now_iso(),
        "source": str(source),
        "chapters": chapters_output,
    }

    (output / "GURUKUL_CHAPTER_RESOURCE_MANIFEST.json").write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # CLASS/SUBJECT INDEX
    # --------------------------------------------------------

    index = defaultdict(
        lambda: defaultdict(list)
    )

    for chapter in chapters_output:

        index[
            chapter["class_id"]
        ][
            chapter["subject_id"]
        ].append({
            "chapter_id": chapter["chapter_id"],
            "chapter_title": chapter["chapter_title"],
            "resource_count":
                chapter["resource_summary"]["total"],
            "direct_youtube":
                chapter["resource_summary"]["direct_youtube"],
            "official":
                chapter["resource_summary"]["official"],
        })

    (output / "GURUKUL_CLASS_SUBJECT_INDEX.json").write_text(
        json.dumps(
            index,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    report["classes"] = dict(
        report["classes"]
    )

    report["subjects"] = dict(
        report["subjects"]
    )

    report["chapters"] = dict(
        report["chapters"]
    )

    report["finished_at"] = now_iso()

    report["status"] = (
        "PASS"
        if not report["invalid_json"]
        else "FAIL"
    )

    report["source_modified"] = False

    REPORT_PATH.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # HUMAN AUDIT
    # --------------------------------------------------------

    lines = [
        "# GURUKUL AI Contents Normalization Audit",
        "",
        f"Generated: {now_iso()}",
        "",
        "## Source",
        "",
        f"`{source}`",
        "",
        "## Safety",
        "",
        "- Original Contents tree modified: **NO**",
        "- Normalization performed into separate output tree.",
        "",
        "## Inventory",
        "",
        f"- Files: **{len(all_files)}**",
        f"- JSON files: **{len(json_files)}**",
        f"- Resources detected: **{report['resources']}**",
        f"- Direct YouTube URLs: **{report['direct_youtube']}**",
        f"- YouTube search URLs: **{report['youtube_search']}**",
        f"- Official NCERT/DIKSHA resources: **{report['official_resources']}**",
        f"- Placeholder resources: **{report['placeholder_resources']}**",
        f"- Invalid URLs: **{report['invalid_urls']}**",
        "",
        "## Classes",
        "",
    ]

    for cls, count in sorted(
        report["classes"].items()
    ):
        lines.append(
            f"- `{cls}`: {count} files"
        )

    lines.extend([
        "",
        "## Validation",
        "",
        f"- Invalid JSON files: **{len(report['invalid_json'])}**",
        f"- Overall status: **{report['status']}**",
        "",
        "## Output",
        "",
        f"`{output}`",
        "",
        "## Important",
        "",
        "No external resources or YouTube videos are fabricated.",
        "Search URLs remain discovery resources.",
        "Direct videos remain direct videos only when an actual",
        "YouTube watch URL is present.",
        "",
    ])

    AUDIT_PATH.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    # --------------------------------------------------------
    # OPTIONAL APPLY
    # --------------------------------------------------------

    if args.apply:

        if report["status"] != "PASS":

            raise SystemExit(
                "APPLY ABORTED: validation failed."
            )

        backup = (
            PROJECT_ROOT /
            f"Contents_JSON_BACKUP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        backup.mkdir(
            parents=True,
            exist_ok=False,
        )

        for json_file in json_files:

            relative = json_file.relative_to(
                source
            )

            destination = backup / relative

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                json_file,
                destination,
            )

        # Replace JSON only.
        for json_file in json_files:

            relative = json_file.relative_to(
                source
            )

            normalized_file = output / relative

            shutil.copy2(
                normalized_file,
                json_file,
            )

        report["source_modified"] = True
        report["apply_backup"] = str(backup)
        report["status"] = "APPLIED"

        REPORT_PATH.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print("")
        print("============================================================")
        print("NORMALIZATION APPLIED")
        print("============================================================")
        print(f"Backup: {backup}")

    else:

        print("")
        print("============================================================")
        print("NORMALIZATION COMPLETE")
        print("============================================================")
        print("")
        print("Original Contents was NOT modified.")
        print("")
        print(f"Output : {output}")
        print(f"Report : {REPORT_PATH}")
        print(f"Audit  : {AUDIT_PATH}")
        print("")
        print("Review the report before using --apply.")

    print("")
    print("Classes:", report["classes"])
    print("JSON:", len(json_files))
    print("Resources:", report["resources"])
    print("Direct YouTube:", report["direct_youtube"])
    print("YouTube search:", report["youtube_search"])
    print("Official:", report["official_resources"])
    print("Invalid JSON:", len(report["invalid_json"]))
    print("Invalid URLs:", report["invalid_urls"])
    print("Status:", report["status"])


if __name__ == "__main__":
    main()
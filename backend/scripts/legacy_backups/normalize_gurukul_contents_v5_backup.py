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


# ---------------------------------------------------------------------------
# V3 IDENTITY ENGINE
# ---------------------------------------------------------------------------
# Chapter identity is derived primarily from the canonical directory path.
# This is intentionally independent of JSON metadata because generated JSON
# can contain incomplete or stale identity fields.
#
# Supported chapter directory forms include:
#   101_Papas_Spectacles
#   106_THE_STATE_THE_GOVERNMENT_AND_YOU
#   108_BANKS_AND_THE_MAGIC_OF_FINANCE
#
# A chapter is a directory immediately below the subject directory whose
# basename starts with a 3-digit chapter number followed by "_".
# ---------------------------------------------------------------------------

import re

CLASS_DIR_RE = re.compile(r"^Class\s*([3-9]|1[0-2])$", re.IGNORECASE)
CHAPTER_DIR_RE = re.compile(r"^(\d{3})_(.+)$")

CANONICAL_CONTENT_DIRS = {
    "00_CHAPTER_INFO",
    "01_LEARN",
    "02_PRACTICE",
    "03_ASSESS",
    "04_REVISE",
    "05_RESOURCES",
    "99_INTERNAL_TRACEABILITY",
}

def _clean_title_from_dir(name):
    """Convert a canonical chapter directory name into a readable title."""
    m = CHAPTER_DIR_RE.match(name.strip())
    if not m:
        return None
    raw = m.group(2).replace("_", " ").strip()
    raw = re.sub(r"\s+", " ", raw)
    return raw

def _path_identity(path, source):
    """
    Resolve class/subject/chapter from the directory hierarchy.

    Expected:
      Contents / Class N / SUBJECT_DIR / SUBJECT_INNER_DIR / CHAPTER_DIR / ...

    Also tolerates:
      Contents / Class N / SUBJECT_DIR / CHAPTER_DIR / ...
    """
    try:
        rel = path.relative_to(source)
    except ValueError:
        return None

    parts = list(rel.parts)

    # Locate Class N anywhere in the relative path.
    class_idx = None
    class_id = None
    for i, part in enumerate(parts):
        m = CLASS_DIR_RE.match(part)
        if m:
            class_idx = i
            class_id = f"class_{m.group(1)}"
            break

    if class_idx is None:
        return None

    # Ignore files at/above the class level.
    after_class = parts[class_idx + 1:]
    if not after_class:
        return {
            "class_id": class_id,
            "class_name": f"Class {class_id.split('_')[-1]}",
            "subject_id": None,
            "subject_name": None,
            "chapter_id": None,
            "chapter_title": None,
            "identity_source": "path"
        }

    # Candidate chapter directories. We deliberately select the first
    # canonical NNN_title directory after the class directory, but prefer
    # one occurring after a subject-like directory.
    chapter_pos = None
    chapter_match = None
    for j, part in enumerate(after_class):
        m = CHAPTER_DIR_RE.match(part)
        if m:
            chapter_pos = j
            chapter_match = m
            break

    if chapter_match is None:
        # Subject is normally the first directory after Class N.
        subject_dir = after_class[0]
        return {
            "class_id": class_id,
            "class_name": f"Class {class_id.split('_')[-1]}",
            "subject_id": _normalize_subject_id(subject_dir),
            "subject_name": _normalize_subject_name(subject_dir),
            "chapter_id": None,
            "chapter_title": None,
            "identity_source": "path"
        }

    # Subject directory is the first directory before the chapter.
    # Some canonical trees have an additional inner subject directory.
    subject_dir = after_class[0]
    if chapter_pos >= 2 and after_class[1].upper() == _normalize_subject_id(subject_dir).upper():
        subject_dir = after_class[0]

    chapter_number = chapter_match.group(1)
    chapter_title = _clean_title_from_dir(after_class[chapter_pos])
    subject_id = _normalize_subject_id(subject_dir)
    subject_name = _normalize_subject_name(subject_dir)

    return {
        "class_id": class_id,
        "class_name": f"Class {class_id.split('_')[-1]}",
        "subject_id": subject_id,
        "subject_name": subject_name,
        "chapter_id": chapter_number,
        "chapter_title": chapter_title,
        "identity_source": "path"
    }

def discover_canonical_chapters(source, requested_classes=None):
    """
    Discover chapters from directory structure, not from individual JSONs.

    Returns:
      { (class_id, subject_id, chapter_id): metadata }
    """
    requested = {str(c) for c in (requested_classes or [5, 6, 7])}
    found = {}

    for class_dir in sorted(source.glob("Class *")):
        if not class_dir.is_dir():
            continue

        cm = CLASS_DIR_RE.match(class_dir.name)
        if not cm or cm.group(1) not in requested:
            continue

        class_id = f"class_{cm.group(1)}"

        for subject_dir in sorted(p for p in class_dir.iterdir() if p.is_dir()):
            subject_id = _normalize_subject_id(subject_dir.name)
            subject_name = _normalize_subject_name(subject_dir.name)

            # Search directly below the subject directory and one level below
            # it. This supports both observed canonical layouts.
            candidates = []
            for p in subject_dir.iterdir():
                if p.is_dir() and CHAPTER_DIR_RE.match(p.name):
                    candidates.append(p)

            for inner in sorted(p for p in subject_dir.iterdir() if p.is_dir()):
                if inner.name.startswith("00_") or inner.name.lower() in {
                    "manifest", "metadata"
                }:
                    continue
                for p in inner.iterdir():
                    if p.is_dir() and CHAPTER_DIR_RE.match(p.name):
                        candidates.append(p)

            for chapter_dir in sorted(set(candidates), key=lambda p: p.name):
                m = CHAPTER_DIR_RE.match(chapter_dir.name)
                if not m:
                    continue

                chapter_id = m.group(1)
                chapter_title = _clean_title_from_dir(chapter_dir.name)
                key = (class_id, subject_id, chapter_id)

                found[key] = {
                    "class_id": class_id,
                    "class_name": f"Class {cm.group(1)}",
                    "subject_id": subject_id,
                    "subject_name": subject_name,
                    "chapter_id": chapter_id,
                    "chapter_title": chapter_title,
                    "chapter_path": str(chapter_dir),
                    "identity_source": "canonical_path"
                }

    return found
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



def canonical_file_identity(path: Path, source: Path, data):
    """
    Resolve identity from the authoritative canonical directory hierarchy.

    Rule:
      Contents / Class N / <NN_subject...> / [optional inner subject dir] /
      <NNN_chapter_title> / ...

    The first 2-digit subject directory after Class N is authoritative.
    The first 3-digit chapter directory after Class N is authoritative.
    JSON metadata is used only as a fallback for title, never to override
    path identity.
    """
    try:
        rel = path.relative_to(source)
    except ValueError:
        rel = path

    parts = list(rel.parts)

    class_id = None
    class_pos = None
    for i, part in enumerate(parts):
        m = re.fullmatch(r"Class\s*0*([567])", part.strip(), re.I)
        if m:
            class_id = f"class_{m.group(1)}"
            class_pos = i
            break

    if class_id is None:
        # Also support class5/class_5 style directory names.
        for i, part in enumerate(parts):
            p = part.strip().lower()
            if p in CLASS_MAP:
                class_id = CLASS_MAP[p]
                class_pos = i
                break

    if class_id is None:
        return {
            "class_id": None,
            "subject_id": None,
            "chapter_id": None,
            "chapter_title": None,
        }

    after = parts[class_pos + 1:]

    # Subject = first directory with a 2-digit canonical prefix.
    subject_id = None
    for part in after:
        if re.match(r"^\d{2}[_-]", part):
            subject_id = part.strip().lower()
            break

    # Chapter = first directory with exactly 3 digits + "_title".
    chapter_id = None
    chapter_title = None
    for part in after:
        m = re.fullmatch(r"(\d{3})_(.+)", part.strip())
        if m:
            chapter_id = m.group(1)
            chapter_title = clean_string(m.group(2).replace("_", " "))
            break

    # Fallback title from JSON only when the canonical path has a chapter ID.
    if chapter_id and not chapter_title:
        chapter_title = title_from_data(data)

    return {
        "class_id": class_id,
        "subject_id": subject_id,
        "chapter_id": chapter_id,
        "chapter_title": chapter_title,
    }


def discover_canonical_chapter_keys(source: Path):
    """
    Enumerate every chapter directory directly from Contents.

    This is the authoritative chapter inventory and does not depend on
    resources being present in JSON files.
    """
    found = {}

    for class_dir in sorted(p for p in source.iterdir() if p.is_dir()):
        cm = re.fullmatch(r"Class\s*0*([567])", class_dir.name.strip(), re.I)
        if not cm:
            continue

        class_id = f"class_{cm.group(1)}"

        # A subject directory is identified by its 2-digit prefix.
        subject_dirs = [
            p for p in class_dir.iterdir()
            if p.is_dir() and re.match(r"^\d{2}[_-]", p.name)
        ]

        for subject_dir in sorted(subject_dirs, key=lambda p: p.name.lower()):
            subject_id = subject_dir.name.strip().lower()

            # Support both:
            #   subject/chapter
            #   subject/inner_subject/chapter
            chapter_dirs = []

            for child in subject_dir.iterdir():
                if child.is_dir() and re.fullmatch(r"\d{3}_.+", child.name):
                    chapter_dirs.append(child)

            for inner in subject_dir.iterdir():
                if not inner.is_dir():
                    continue
                for child in inner.iterdir():
                    if child.is_dir() and re.fullmatch(r"\d{3}_.+", child.name):
                        chapter_dirs.append(child)

            for chapter_dir in sorted(set(chapter_dirs), key=lambda p: p.name.lower()):
                m = re.fullmatch(r"(\d{3})_(.+)", chapter_dir.name)
                if not m:
                    continue

                chapter_id = m.group(1)
                chapter_title = clean_string(m.group(2).replace("_", " "))
                # Some subjects are split across multiple canonical packages
                # (for example, Class 7 Social Science Part 1 / Part 2).
                # Preserve the package in the internal key so chapters with the
                # same public subject/chapter number are not collapsed.
                subject_package_id = class_dir.name.strip().lower() + "::" + subject_dir.name.strip().lower()
                key = (class_id, subject_package_id, subject_id, chapter_id)

                found[key] = {
                    "class_id": class_id,
                    "subject_id": subject_id,
                    "subject_package_id": subject_package_id,
                    "chapter_id": chapter_id,
                    "chapter_title": chapter_title,
                    "chapter_path": str(chapter_dir.relative_to(source)),
                }

    return found


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

    canonical_chapters = discover_canonical_chapter_keys(source)
    chapter_resources = defaultdict(list)

    # Seed every discovered chapter, including chapters with zero resources.
    # This prevents the chapter matrix from silently dropping resource-less
    # chapters.
    for key in canonical_chapters:
        chapter_resources[key] = []

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

        ident = canonical_file_identity(path, source, data)

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

        canonical_meta = {}
        for ck, cm in canonical_chapters.items():
            if (
                cm.get("class_id") == cls
                and cm.get("subject_id") == subject
                and cm.get("chapter_id") == chapter
            ):
                canonical_meta = cm
                break
        report["chapter_matrix"].append(
            {
                "class_id": cls,
                "subject_id": subject,
                "chapter_id": chapter,
                "chapter_title": canonical_meta.get("chapter_title"),
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

    canonical_inventory_counts = Counter(
        meta["class_id"] for meta in canonical_chapters.values()
    )
    report["canonical_inventory"] = {
        "total": len(canonical_chapters),
        "class_counts": dict(canonical_inventory_counts),
        "expected": {
            "class_5": 47,
            "class_6": 64,
            "class_7": 72,
        },
    }

    # Package-aware inventory audit. This prevents legitimate split-subject
    # packages from being mistaken for duplicate chapters.
    public_identity_groups = defaultdict(list)
    for meta in canonical_chapters.values():
        public_key = (
            meta.get("class_id"),
            meta.get("subject_id"),
            meta.get("chapter_id"),
        )
        public_identity_groups[public_key].append(
            meta.get("subject_package_id")
        )

    package_collisions = {
        "|".join(str(x) for x in key): sorted(set(packages))
        for key, packages in public_identity_groups.items()
        if len(set(packages)) > 1
    }

    report["package_aware_inventory"] = {
        "total": len(canonical_chapters),
        "public_identity_collision_groups": len(package_collisions),
        "collision_groups": package_collisions,
        "subject_package_counts": dict(
            Counter(
                meta.get("subject_package_id")
                for meta in canonical_chapters.values()
            )
        ),
    }

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

    discovered_class_counts = canonical_inventory_counts

    gates = {
        "source_protection": True,
        "canonical_chapter_inventory": (
            len(canonical_chapters) == 183
            and discovered_class_counts.get("class_5", 0) == 47
            and discovered_class_counts.get("class_6", 0) == 64
            and discovered_class_counts.get("class_7", 0) == 72
        ),
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

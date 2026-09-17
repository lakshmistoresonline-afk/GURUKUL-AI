from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from typing import Any


# ============================================================
# GURUKUL AI
# CLASS 5 CANONICAL CONTENT ADAPTER
# ============================================================
#
# PURPOSE
# -------
# Convert the preserved Class 5 source packages into deterministic
# runtime data WITHOUT flattening source structure into meaningless
# paragraph cards.
#
# PRINCIPLES
# ----------
# 1. Source is authoritative.
# 2. Never invent missing textbook text.
# 3. Preserve source provenance.
# 4. Preserve fragments internally when they cannot safely become
#    student-facing educational units.
# 5. Generated material is explicitly marked GENERATED.
# 6. Renderer should not perform semantic reconstruction.
# 7. Deterministic IDs prevent accidental record collisions.
# 8. Full chapter source is preserved separately from student units.
#
# ============================================================


PROJECT_ROOT = Path(r"D:\GURUKUL-AI")
CONTENTS_ROOT = PROJECT_ROOT / "Contents" / "Class 5"
RUNTIME_ROOT = PROJECT_ROOT / "runtime-data"
CHAPTERS_OUT = RUNTIME_ROOT / "chapters"
SEARCH_OUT = RUNTIME_ROOT / "search"

ADAPTER_VERSION = "CLASS5_CANONICAL_ADAPTER_V2"


# ------------------------------------------------------------
# Known source/package folders
# ------------------------------------------------------------

PILLAR_MAP = {
    "01_LEARN": "learn",
    "02_PRACTICE": "practice",
    "03_ASSESS": "assess",
    "04_REVISE": "revise",
    "05_RESOURCES": "resources",
}

ASSET_ORDER = {
    "01_LESSONS": 10,
    "02_CONCEPTS": 20,
    "03_EXAMPLES": 30,
    "04_SOURCE_DERIVED": 40,
    "01_TEXTBOOK_ACTIVITIES": 50,
    "02_QUESTIONS": 60,
    "03_WORKED_PRACTICE": 70,
    "04_APPLICATION": 80,
    "01_TEXTBOOK_ASSESSMENTS": 90,
    "02_MCQ": 100,
    "03_SHORT_ANSWER": 110,
    "01_RECALL": 120,
    "02_KEY_POINTS": 130,
    "03_REVISION_ACTIVITIES": 140,
    "01_VIDEOS": 150,
    "02_YOUTUBE_SEARCH": 160,
    "03_CHANNELS": 170,
    "04_OFFICIAL_PORTALS": 180,
}


# ------------------------------------------------------------
# Obvious non-content / OCR artifacts
# ------------------------------------------------------------

REJECT_EXACT = {
    "",
    ".",
    "..",
    "-",
    "_",
    "—",
    "–",
    "?",
    "!",
    ",",
    ":",
    ";",
}


REJECT_PATTERNS = [
    r"^[0-9]+$",
    r"^[A-Za-z]$",
    r"^[ivxlcdmIVXLCDM]+$",
    r"^[\W_]+$",
    r"^page\s*[0-9]+$",
    r"^chapter\s*[0-9]+$",
]


# ------------------------------------------------------------
# Basic utilities
# ------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    """
    Read JSON robustly.

    Some source files in the project have appeared with UTF-16
    encoding, while others are UTF-8.
    """
    raw = path.read_bytes()

    encodings = [
        "utf-8-sig",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
    ]

    last_error = None

    for enc in encodings:
        try:
            text = raw.decode(enc)
            return json.loads(text)
        except Exception as exc:
            last_error = exc

    raise ValueError(f"Unable to parse JSON: {path} :: {last_error}")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def clean_text(value: Any) -> str:
    if value is None:
        return ""

    text = str(value)

    replacements = {
        "\ufeff": "",
        "\u00a0": " ",
        "â€™": "’",
        "â€˜": "‘",
        "â€œ": "“",
        "â€": "”",
        "â€“": "–",
        "â€”": "—",
        "â€¦": "…",
        "Ã©": "é",
        "Ã¨": "è",
        "Ã¡": "á",
        "Ã": "A",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Preserve meaningful line structure but remove excessive whitespace.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def normalize_for_id(text: str) -> str:
    text = clean_text(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slug(value: str) -> str:
    value = normalize_for_id(value)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "unknown"


def looks_like_reject(text: str) -> bool:
    t = clean_text(text)

    if t in REJECT_EXACT:
        return True

    for pattern in REJECT_PATTERNS:
        if re.match(pattern, t, flags=re.IGNORECASE):
            return True

    # Obvious OCR noise.
    if len(t) >= 8 and len(set(t.lower())) <= 2:
        return True

    return False


def stable_id(
    chapter_id: str,
    pillar: str,
    asset: str,
    source_ref: str,
    sequence: int,
    text: str,
) -> str:
    """
    Stable deterministic record identifier.

    IMPORTANT:
    The hash contains the source reference and sequence so two
    legitimate identical words appearing at different source
    locations do not collide.
    """
    material = "|".join(
        [
            chapter_id,
            pillar,
            asset,
            source_ref,
            str(sequence),
            normalize_for_id(text),
        ]
    )

    digest = hashlib.sha256(
        material.encode("utf-8")
    ).hexdigest()[:20]

    return f"{chapter_id}_{pillar}_{asset}_{sequence:04d}_{digest}"


# ------------------------------------------------------------
# Text extraction
# ------------------------------------------------------------

TEXT_FIELDS = [
    "text",
    "content",
    "source_text",
    "question_or_prompt",
    "question",
    "prompt",
    "heading",
    "title",
    "activity",
    "description",
    "body",
    "answer",
    "answer_guidance",
]


def best_text(obj: dict[str, Any]) -> str:
    for field in TEXT_FIELDS:
        value = obj.get(field)

        if isinstance(value, str) and clean_text(value):
            return clean_text(value)

    return ""


def get_source_ref(obj: dict[str, Any], default: str) -> str:
    for field in [
        "source_ref",
        "source",
        "source_reference",
    ]:
        value = obj.get(field)

        if value:
            return str(value)

    return default


def get_source_page(obj: dict[str, Any]) -> Any:
    for field in [
        "source_page",
        "page",
        "page_number",
    ]:
        if field in obj:
            return obj[field]

    return None


# ------------------------------------------------------------
# Semantic classification
# ------------------------------------------------------------

def detect_type(
    text: str,
    asset_name: str,
    section: str = "",
) -> str:

    t = clean_text(text)
    low = t.lower()

    asset = asset_name.lower()
    sec = section.lower()

    if not t:
        return "empty"

    if "mcq" in asset:
        return "mcq"

    if "short_answer" in asset:
        return "short_answer"

    if "textbook_assessment" in asset:
        return "assessment_question"

    if "question" in asset:
        if "fill" in low or "................" in t or "______" in t:
            return "fill_in_the_blank"

        if "arrange" in low or "order" in low:
            return "ordering"

        if "spell" in low:
            return "spelling_selection"

        if t.endswith("?"):
            return "question"

        if re.match(r"^\d+[\.\)]\s*", t) and len(t) > 25:
            return "question"

    if "activity" in asset or "application" in asset:
        return "activity"

    if "worked" in asset:
        return "worked_practice"

    if "lesson" in asset:
        return "lesson"

    if "concept" in asset:
        return "concept"

    if "example" in asset:
        return "example"

    if "recall" in asset:
        return "revision_recall"

    if "key_points" in asset:
        return "revision_key_point"

    if "revision_activities" in asset:
        return "revision_activity"

    if "youtube" in asset:
        return "resource_search"

    if "portal" in asset:
        return "official_resource"

    if "video" in asset:
        return "video_resource"

    if "channel" in asset:
        return "channel_resource"

    # Dialogue.
    if re.search(
        r"(^|\n)\s*[A-Z][A-Za-z ]{0,30}:\s+",
        t,
    ):
        return "dialogue"

    # Poem heuristic.
    lines = [x.strip() for x in t.splitlines() if x.strip()]

    if len(lines) >= 3:
        short_lines = sum(
            1 for line in lines
            if len(line.split()) <= 10
        )

        if short_lines / len(lines) >= 0.65:
            return "poem"

    # Heading.
    if (
        len(t) <= 90
        and (
            t.isupper()
            or low.startswith("let us ")
            or low in {
                "new words",
                "think and discuss",
                "just for fun",
                "look at the words",
                "note the following phrase",
                "fun with matchsticks",
            }
        )
    ):
        return "heading"

    return "paragraph"


# ------------------------------------------------------------
# Fragment / quality detection
# ------------------------------------------------------------

def is_likely_fragment(
    text: str,
    asset_name: str,
) -> bool:

    t = clean_text(text)

    if not t:
        return True

    # Never reject clearly complete exercises.
    if "................" in t or "______" in t:
        return False

    if t.endswith("?") or t.endswith(".") or t.endswith("!") or t.endswith(":"):
        return False

    # Numbered question without a terminating sentence is frequently
    # an OCR/extraction fragment.
    if re.match(r"^\d+[\.\)]\s+", t):
        words = t.split()

        if len(words) < 8:
            return True

        # A line ending with a conjunction/preposition is suspicious.
        if words[-1].lower() in {
            "to",
            "for",
            "of",
            "in",
            "on",
            "at",
            "with",
            "and",
            "or",
            "but",
            "can",
            "where",
            "what",
            "how",
            "that",
            "the",
            "a",
            "an",
        }:
            return True

    # Very short ordinary text is generally not a standalone unit.
    if len(t.split()) <= 3:
        return True

    # Obvious OCR noise.
    if "bbbbbbbb" in t.lower():
        return True

    return False


# ------------------------------------------------------------
# Canonical record creation
# ------------------------------------------------------------

def make_record(
    *,
    chapter_id: str,
    chapter_title: str,
    pillar: str,
    asset_name: str,
    source_file: Path,
    obj: dict[str, Any],
    sequence: int,
    text: str,
    inherited_section: str = "",
    inherited_page: Any = None,
) -> dict[str, Any] | None:

    text = clean_text(text)

    if not text:
        return None

    source_ref = get_source_ref(
        obj,
        f"{source_file.name}::record:{sequence}",
    )

    source_page = get_source_page(obj)

    if source_page is None:
        source_page = inherited_page

    section = clean_text(
        obj.get("section")
        or obj.get("section_title")
        or inherited_section
    )

    rec_type = detect_type(
        text,
        asset_name,
        section,
    )

    fragment = is_likely_fragment(
        text,
        asset_name,
    )

    status = str(
        obj.get("status")
        or "SOURCE_DERIVED"
    ).upper()

    generated = status == "GENERATED"

    visibility = "student"

    # Source fragments remain available for traceability, but do not
    # become student-facing units.
    if fragment and not generated:
        visibility = "internal"

    if rec_type == "empty":
        visibility = "internal"

    if looks_like_reject(text):
        visibility = "internal"

    rid = stable_id(
        chapter_id,
        pillar,
        asset_name,
        source_ref,
        sequence,
        text,
    )

    record: dict[str, Any] = {
        "record_id": rid,
        "chapter_id": chapter_id,
        "chapter_title": chapter_title,
        "pillar": pillar,
        "asset": asset_name,
        "type": rec_type,
        "text": text,
        "visibility": visibility,
        "student_facing": visibility == "student",
        "content_origin": (
            "GENERATED"
            if generated
            else "SOURCE_DERIVED"
        ),
        "status": status,
        "source": {
            "file": str(
                source_file.relative_to(PROJECT_ROOT)
            ),
            "source_ref": source_ref,
            "source_page": source_page,
            "section": section,
        },
        "quality": {
            "is_fragment": fragment,
            "is_ocr_suspect": (
                "bbbbbbbb" in text.lower()
                or len(set(text.lower().replace(" ", ""))) <= 2
            ),
        },
        "sequence": sequence,
    }

    # Preserve all useful structured fields.
    for field in [
        "options",
        "answer",
        "answer_guidance",
        "source_basis",
        "metadata",
        "category",
        "difficulty",
        "skill",
        "tags",
    ]:
        if field in obj:
            record[field] = obj[field]

    return record


# ------------------------------------------------------------
# Asset normalization
# ------------------------------------------------------------

def normalize_items(
    data: Any,
    asset_name: str,
) -> list[tuple[dict[str, Any], str, str, Any]]:
    """
    Convert different source JSON schemas into a common stream.

    Returns:
        (object, text, inherited_section, inherited_page)
    """

    result = []

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                result.append(
                    (
                        item,
                        best_text(item),
                        "",
                        get_source_page(item),
                    )
                )
            elif isinstance(item, str):
                result.append(
                    (
                        {},
                        clean_text(item),
                        "",
                        None,
                    )
                )

        return result

    if not isinstance(data, dict):
        return result

    # Standard items.
    if isinstance(data.get("items"), list):
        for item in data["items"]:
            if isinstance(item, dict):
                result.append(
                    (
                        item,
                        best_text(item),
                        clean_text(
                            item.get("section")
                            or item.get("section_title")
                            or ""
                        ),
                        get_source_page(item),
                    )
                )
            elif isinstance(item, str):
                result.append(
                    (
                        {},
                        clean_text(item),
                        "",
                        None,
                    )
                )

    # Revision structures.
    for field in [
        "prompts",
        "key_points",
        "activities",
        "queries",
    ]:
        values = data.get(field)

        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict):
                    text = best_text(item)
                    result.append(
                        (
                            item,
                            text,
                            "",
                            get_source_page(item),
                        )
                    )
                else:
                    result.append(
                        (
                            {
                                "status": data.get(
                                    "status",
                                    "SOURCE_DERIVED",
                                ),
                                "source_basis": data.get(
                                    "source_basis"
                                ),
                            },
                            clean_text(item),
                            "",
                            None,
                        )
                    )

    # Official portals.
    portals = data.get("recommended_portals")

    if isinstance(portals, list):
        for item in portals:
            if isinstance(item, dict):
                text = best_text(item)

                if not text:
                    text = clean_text(
                        item.get("name")
                        or item.get("title")
                        or ""
                    )

                result.append(
                    (
                        item,
                        text,
                        "",
                        get_source_page(item),
                    )
                )

            else:
                result.append(
                    (
                        {
                            "status": data.get(
                                "status",
                                "SOURCE_DERIVED",
                            ),
                        },
                        clean_text(item),
                        "",
                        None,
                    )
                )

    return result


# ------------------------------------------------------------
# Full chapter source
# ------------------------------------------------------------

def load_full_chapter_source(
    chapter_dir: Path,
) -> dict[str, Any] | None:

    source_dir = (
        chapter_dir
        / "01_LEARN"
        / "04_SOURCE_DERIVED"
    )

    if not source_dir.exists():
        return None

    candidates = list(
        source_dir.glob("*.json")
    )

    for path in candidates:
        try:
            data = read_json(path)

            if isinstance(data, dict) and (
                "pages" in data
                or "full_chapter_text" in path.name.lower()
            ):
                return {
                    "file": str(
                        path.relative_to(PROJECT_ROOT)
                    ),
                    "data": data,
                }

        except Exception:
            continue

    return None


# ------------------------------------------------------------
# Chapter metadata
# ------------------------------------------------------------

def load_chapter_info(
    chapter_dir: Path,
) -> dict[str, Any]:

    info_path = (
        chapter_dir
        / "00_CHAPTER_INFO"
        / "CHAPTER_INFO.json"
    )

    if not info_path.exists():
        return {}

    try:
        data = read_json(info_path)

        if isinstance(data, dict):
            return data

    except Exception:
        pass

    return {}


# ------------------------------------------------------------
# Find Class 5 chapter directories
# ------------------------------------------------------------

def find_chapters() -> list[Path]:

    chapters = []

    if not CONTENTS_ROOT.exists():
        raise FileNotFoundError(
            f"Class 5 contents root not found: "
            f"{CONTENTS_ROOT}"
        )

    for subject_root in sorted(
        CONTENTS_ROOT.iterdir()
    ):
        if not subject_root.is_dir():
            continue

        # Typical structure:
        #
        # Class 5/
        #   01_ENGLISH_COMPLETE/
        #       01_ENGLISH/
        #           101_Papas_Spectacles/
        #
        for candidate_root in [
            subject_root,
            *[
                p
                for p in subject_root.iterdir()
                if p.is_dir()
            ],
        ]:
            if not candidate_root.exists():
                continue

            try:
                candidates = list(
                    candidate_root.iterdir()
                )
            except Exception:
                continue

            for chapter_dir in candidates:
                if not chapter_dir.is_dir():
                    continue

                if (
                    chapter_dir / "01_LEARN"
                ).exists():
                    chapters.append(chapter_dir)

    # Remove duplicates while preserving order.
    unique = {}

    for path in chapters:
        unique[str(path.resolve())] = path

    return sorted(
        unique.values(),
        key=lambda p: str(p).lower(),
    )


# ------------------------------------------------------------
# Process one chapter
# ------------------------------------------------------------

def process_chapter(
    chapter_dir: Path,
) -> dict[str, Any]:

    info = load_chapter_info(chapter_dir)

    folder_name = chapter_dir.name

    chapter_id = clean_text(
        str(
            info.get("chapter_id")
            or re.match(
                r"^(\d+)",
                folder_name,
            ).group(1)
            if re.match(
                r"^(\d+)",
                folder_name,
            )
            else folder_name
        )
    )

    chapter_title = clean_text(
        info.get("chapter_title")
        or re.sub(
            r"^\d+[_\-\s]*",
            "",
            folder_name,
        ).replace("_", " ")
    )

    # --------------------------------------------------------
    # Find subject.
    # --------------------------------------------------------

    subject_name = "unknown"

    try:
        relative = chapter_dir.relative_to(
            CONTENTS_ROOT
        )

        parts = list(relative.parts)

        if parts:
            subject_name = parts[0]

    except Exception:
        pass

    output_id = f"class_5_{slug(subject_name)}_{chapter_id}"

    package: dict[str, Any] = {
        "schema_version": "canonical-runtime-v2",
        "adapter_version": ADAPTER_VERSION,
        "generated_at": utc_now(),

        "id": output_id,
        "chapter_id": chapter_id,
        "chapter_title": chapter_title,

        "class_id": "class_5",
        "class_name": "Class 5",

        "subject_id": slug(subject_name),
        "subject_name": subject_name,

        "source": {
            "chapter_folder": str(
                chapter_dir.relative_to(PROJECT_ROOT)
            ),
            "source_pdf": info.get(
                "source_pdf"
            ),
            "page_count": info.get(
                "page_count"
            ),
            "grade": info.get(
                "grade",
                "Class 5",
            ),
            "textbook": info.get(
                "textbook"
            ),
            "source_authority": info.get(
                "source_authority"
            ),
            "source_preservation": info.get(
                "source_preservation"
            ),
        },

        "learn": [],
        "practice": [],
        "assess": [],
        "revise": [],
        "resources": [],

        # Complete source records that should never be
        # mistaken for student-facing educational units.
        "source_records": [],

        "source_document": None,

        "traceability": {
            "chapter_info": info,
            "chapter_folder": str(
                chapter_dir.relative_to(PROJECT_ROOT)
            ),
            "source_files": [],
        },

        "accounting": {},
    }

    # --------------------------------------------------------
    # Preserve complete chapter source separately.
    # --------------------------------------------------------

    full_source = load_full_chapter_source(
        chapter_dir
    )

    if full_source:
        package["source_document"] = full_source

    # --------------------------------------------------------
    # Process each pillar.
    # --------------------------------------------------------

    for pillar_dir_name, pillar in PILLAR_MAP.items():

        pillar_dir = (
            chapter_dir
            / pillar_dir_name
        )

        if not pillar_dir.exists():
            continue

        asset_dirs = [
            p
            for p in pillar_dir.iterdir()
            if p.is_dir()
        ]

        asset_dirs.sort(
            key=lambda p: (
                ASSET_ORDER.get(
                    p.name,
                    9999,
                ),
                p.name.lower(),
            )
        )

        for asset_dir in asset_dirs:

            json_files = sorted(
                asset_dir.glob("*.json")
            )

            for source_file in json_files:

                # Full chapter text is preserved separately.
                if (
                    "full_chapter_text"
                    in source_file.name.lower()
                ):
                    package[
                        "traceability"
                    ][
                        "source_files"
                    ].append(
                        str(
                            source_file.relative_to(
                                PROJECT_ROOT
                            )
                        )
                    )
                    continue

                try:
                    data = read_json(
                        source_file
                    )
                except Exception as exc:

                    package[
                        "traceability"
                    ].setdefault(
                        "parse_errors",
                        [],
                    ).append(
                        {
                            "file": str(
                                source_file.relative_to(
                                    PROJECT_ROOT
                                )
                            ),
                            "error": str(exc),
                        }
                    )

                    continue

                package[
                    "traceability"
                ][
                    "source_files"
                ].append(
                    str(
                        source_file.relative_to(
                            PROJECT_ROOT
                        )
                    )
                )

                normalized = normalize_items(
                    data,
                    asset_dir.name,
                )

                for local_index, (
                    obj,
                    text,
                    inherited_section,
                    inherited_page,
                ) in enumerate(
                    normalized,
                    start=1,
                ):

                    if not text:
                        continue

                    record = make_record(
                        chapter_id=chapter_id,
                        chapter_title=chapter_title,
                        pillar=pillar,
                        asset_name=asset_dir.name,
                        source_file=source_file,
                        obj=obj,
                        sequence=local_index,
                        text=text,
                        inherited_section=inherited_section,
                        inherited_page=inherited_page,
                    )

                    if record is None:
                        continue

                    # Source records are always preserved.
                    package[
                        "source_records"
                    ].append(record)

                    # Student-facing records only enter their
                    # corresponding pillar array.
                    if record["student_facing"]:
                        package[pillar].append(
                            record
                        )

    # --------------------------------------------------------
    # Deterministic ordering.
    # --------------------------------------------------------

    for pillar in [
        "learn",
        "practice",
        "assess",
        "revise",
        "resources",
    ]:
        package[pillar].sort(
            key=lambda r: (
                r.get("source", {}).get(
                    "source_page"
                )
                is None,
                r.get("source", {}).get(
                    "source_page"
                )
                or 999999,
                r.get("asset", ""),
                r.get("sequence", 0),
                r.get("record_id", ""),
            )
        )

    package["source_records"].sort(
        key=lambda r: (
            r.get("source", {}).get(
                "source_page"
            )
            is None,
            r.get("source", {}).get(
                "source_page"
            )
            or 999999,
            r.get("pillar", ""),
            r.get("asset", ""),
            r.get("sequence", 0),
        )
    )

    # --------------------------------------------------------
    # Exact accounting.
    # --------------------------------------------------------

    all_student = []

    for pillar in [
        "learn",
        "practice",
        "assess",
        "revise",
        "resources",
    ]:
        all_student.extend(
            package[pillar]
        )

    all_source = package[
        "source_records"
    ]

    student_ids = [
        r["record_id"]
        for r in all_student
    ]

    source_ids = [
        r["record_id"]
        for r in all_source
    ]

    package["accounting"] = {
        "student_facing_records": len(
            all_student
        ),
        "student_facing_unique_ids": len(
            set(student_ids)
        ),
        "source_records": len(
            all_source
        ),
        "source_unique_ids": len(
            set(source_ids)
        ),
        "internal_records": sum(
            1
            for r in all_source
            if not r["student_facing"]
        ),
        "id_collision_count": (
            len(student_ids)
            - len(set(student_ids))
        ),
        "type_counts": dict(
            Counter(
                r["type"]
                for r in all_student
            )
        ),
        "pillar_counts": {
            pillar: len(
                package[pillar]
            )
            for pillar in [
                "learn",
                "practice",
                "assess",
                "revise",
                "resources",
            ]
        },
    }

    # --------------------------------------------------------
    # Data quality flags.
    # --------------------------------------------------------

    package["quality"] = {
        "has_duplicate_student_ids": (
            len(student_ids)
            != len(set(student_ids))
        ),
        "has_parse_errors": bool(
            package[
                "traceability"
            ].get("parse_errors")
        ),
        "generated_records": sum(
            1
            for r in all_student
            if r.get("content_origin")
            == "GENERATED"
        ),
        "source_derived_records": sum(
            1
            for r in all_student
            if r.get("content_origin")
            == "SOURCE_DERIVED"
        ),
        "internal_fragment_records": sum(
            1
            for r in all_source
            if not r["student_facing"]
        ),
    }

    # --------------------------------------------------------
    # Write chapter.
    # --------------------------------------------------------

    subject_folder = slug(
        subject_name
    )

    out_dir = (
        CHAPTERS_OUT
        / "class_5"
        / subject_folder
    )

    out_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        out_dir
        / f"{chapter_id}.json"
    )

    write_json(
        output_file,
        package,
    )

    return package


# ------------------------------------------------------------
# Search index
# ------------------------------------------------------------

def build_search_index(
    packages: list[dict[str, Any]],
) -> dict[str, Any]:

    records = []

    for package in packages:

        for pillar in [
            "learn",
            "practice",
            "assess",
            "revise",
            "resources",
        ]:

            for record in package.get(
                pillar,
                [],
            ):

                text = clean_text(
                    record.get("text")
                )

                if not text:
                    continue

                records.append(
                    {
                        "record_id": record[
                            "record_id"
                        ],
                        "chapter_id": package[
                            "chapter_id"
                        ],
                        "chapter_title": package[
                            "chapter_title"
                        ],
                        "class_id": package[
                            "class_id"
                        ],
                        "subject_id": package[
                            "subject_id"
                        ],
                        "pillar": pillar,
                        "type": record[
                            "type"
                        ],
                        "text": text,
                        "source": record.get(
                            "source",
                            {},
                        ),
                    }
                )

    return {
        "schema_version": "canonical-search-v2",
        "adapter_version": ADAPTER_VERSION,
        "generated_at": utc_now(),
        "record_count": len(records),
        "records": records,
    }


# ------------------------------------------------------------
# Global manifest
# ------------------------------------------------------------

def build_manifest(
    packages: list[dict[str, Any]],
) -> dict[str, Any]:

    student_records = []
    source_records = []

    for package in packages:

        for pillar in [
            "learn",
            "practice",
            "assess",
            "revise",
            "resources",
        ]:
            student_records.extend(
                package.get(
                    pillar,
                    [],
                )
            )

        source_records.extend(
            package.get(
                "source_records",
                [],
            )
        )

    student_ids = [
        r["record_id"]
        for r in student_records
    ]

    source_ids = [
        r["record_id"]
        for r in source_records
    ]

    return {
        "schema_version": "class5-runtime-manifest-v2",
        "adapter_version": ADAPTER_VERSION,
        "generated_at": utc_now(),

        "class": "Class 5",

        "chapter_count": len(
            packages
        ),

        "student_facing_records": len(
            student_records
        ),

        "student_facing_unique_ids": len(
            set(student_ids)
        ),

        "source_records": len(
            source_records
        ),

        "source_unique_ids": len(
            set(source_ids)
        ),

        "internal_records": sum(
            1
            for r in source_records
            if not r.get(
                "student_facing",
                False,
            )
        ),

        "student_id_collisions": (
            len(student_ids)
            - len(set(student_ids))
        ),

        "generated_student_records": sum(
            1
            for r in student_records
            if r.get(
                "content_origin"
            ) == "GENERATED"
        ),

        "source_derived_student_records": sum(
            1
            for r in student_records
            if r.get(
                "content_origin"
            ) == "SOURCE_DERIVED"
        ),

        "chapters": [
            {
                "chapter_id": p[
                    "chapter_id"
                ],
                "chapter_title": p[
                    "chapter_title"
                ],
                "subject_id": p[
                    "subject_id"
                ],
                "accounting": p[
                    "accounting"
                ],
                "quality": p[
                    "quality"
                ],
            }
            for p in packages
        ],
    }


# ------------------------------------------------------------
# Main processing
# ------------------------------------------------------------

def process_all() -> None:

    print()
    print("=" * 72)
    print("GURUKUL AI — CLASS 5 CANONICAL ADAPTER V2")
    print("=" * 72)
    print()

    print(
        f"Source root : {CONTENTS_ROOT}"
    )
    print(
        f"Runtime root: {RUNTIME_ROOT}"
    )
    print()

    chapter_dirs = find_chapters()

    if not chapter_dirs:
        raise RuntimeError(
            "No Class 5 chapter directories were found."
        )

    print(
        f"Discovered chapters: {len(chapter_dirs)}"
    )
    print()

    packages = []

    for index, chapter_dir in enumerate(
        chapter_dirs,
        start=1,
    ):

        print(
            f"[{index:02d}/{len(chapter_dirs):02d}] "
            f"{chapter_dir.name}"
        )

        try:
            package = process_chapter(
                chapter_dir
            )

            packages.append(package)

            acc = package[
                "accounting"
            ]

            print(
                f"      student={acc['student_facing_records']} "
                f"internal={acc['internal_records']} "
                f"collisions={acc['id_collision_count']}"
            )

        except Exception as exc:

            print(
                f"      ERROR: {exc}"
            )

    # --------------------------------------------------------
    # Search index
    # --------------------------------------------------------

    SEARCH_OUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    search_index = build_search_index(
        packages
    )

    write_json(
        SEARCH_OUT / "index.json",
        search_index,
    )

    # --------------------------------------------------------
    # Manifest
    # --------------------------------------------------------

    manifest = build_manifest(
        packages
    )

    write_json(
        RUNTIME_ROOT
        / "CLASS5_CANONICAL_RUNTIME_MANIFEST.json",
        manifest,
    )

    # --------------------------------------------------------
    # Human-readable audit
    # --------------------------------------------------------

    audit_lines = [
        "GURUKUL AI — CLASS 5 CANONICAL ADAPTER V2",
        "=" * 60,
        "",
        f"Generated: {manifest['generated_at']}",
        "",
        f"Chapters: {manifest['chapter_count']}",
        f"Student-facing records: {manifest['student_facing_records']}",
        f"Unique student IDs: {manifest['student_facing_unique_ids']}",
        f"Source records: {manifest['source_records']}",
        f"Unique source IDs: {manifest['source_unique_ids']}",
        f"Internal records: {manifest['internal_records']}",
        f"Student ID collisions: {manifest['student_id_collisions']}",
        f"Generated student records: {manifest['generated_student_records']}",
        f"Source-derived student records: {manifest['source_derived_student_records']}",
        "",
        "CHAPTERS",
        "-" * 60,
    ]

    for chapter in manifest["chapters"]:
        acc = chapter["accounting"]
        quality = chapter["quality"]

        audit_lines.extend(
            [
                "",
                f"{chapter['chapter_id']} — "
                f"{chapter['chapter_title']}",
                f"  Subject: {chapter['subject_id']}",
                f"  Student: {acc['student_facing_records']}",
                f"  Internal: {acc['internal_records']}",
                f"  Source: {acc['source_records']}",
                f"  ID collisions: {acc['id_collision_count']}",
                f"  Generated: {quality['generated_records']}",
                f"  Source-derived: {quality['source_derived_records']}",
            ]
        )

    audit_path = (
        RUNTIME_ROOT
        / "CLASS5_CANONICAL_RUNTIME_AUDIT.txt"
    )

    audit_path.write_text(
        "\n".join(audit_lines),
        encoding="utf-8",
    )

    print()
    print("=" * 72)
    print("PROCESSING COMPLETE")
    print("=" * 72)
    print()
    print(
        f"Chapters              : {manifest['chapter_count']}"
    )
    print(
        f"Student-facing records: {manifest['student_facing_records']}"
    )
    print(
        f"Unique student IDs    : {manifest['student_facing_unique_ids']}"
    )
    print(
        f"Internal records      : {manifest['internal_records']}"
    )
    print(
        f"ID collisions         : {manifest['student_id_collisions']}"
    )
    print()
    print(
        f"Manifest: "
        f"{RUNTIME_ROOT / 'CLASS5_CANONICAL_RUNTIME_MANIFEST.json'}"
    )
    print(
        f"Audit   : "
        f"{audit_path}"
    )
    print(
        f"Search  : "
        f"{SEARCH_OUT / 'index.json'}"
    )
    print()


if __name__ == "__main__":
    process_all()
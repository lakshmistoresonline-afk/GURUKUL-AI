from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
from typing import Any

# ============================================================
# GURUKUL AI
# GENERIC CANONICAL CONTENT ADAPTER (CLASS 5, 6, 7)
# ============================================================
#
# PURPOSE
# -------
# Convert the preserved source packages into deterministic
# runtime data for Class 5, 6, and 7.
#
# ============================================================

PROJECT_ROOT = Path(r"D:\GURUKUL-AI")
RUNTIME_ROOT = PROJECT_ROOT / "runtime-data"
STAGING_ROOT = RUNTIME_ROOT / ".canonical_build"
STAGING_CHAPTERS = STAGING_ROOT / "chapters"
STAGING_SEARCH = STAGING_ROOT / "search"
FINAL_CHAPTERS = RUNTIME_ROOT / "chapters"
FINAL_SEARCH = RUNTIME_ROOT / "search"

ADAPTER_VERSION = "GENERIC_CANONICAL_ADAPTER_V3"

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
    "90_GENERATED": 200,
}

REJECT_EXACT = {"", ".", "..", "-", "_", "—", "–", "?", "!", ",", ":", ";"}

REJECT_PATTERNS = [
    r"^[0-9]+$",
    r"^[A-Za-z]$",
    r"^[ivxlcdmIVXLCDM]+$",
    r"^[\W_]+$",
    r"^page\s*[0-9]+$",
    r"^chapter\s*[0-9]+$",
]

TEXT_FIELDS = [
    "text", "content", "source_text", "question_or_prompt", "question",
    "prompt", "heading", "title", "activity", "description", "body",
    "answer", "answer_guidance",
]

# ------------------------------------------------------------
# Utilities
# ------------------------------------------------------------

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: Path) -> Any:
    raw = path.read_bytes()
    encodings = ["utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"]
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
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def clean_text(value: Any) -> str:
    if value is None: return ""
    text = str(value)
    replacements = {
        "\ufeff": "", "\u00a0": " ", "â€™": "’", "â€˜": "‘", "â€œ": "“",
        "â€": "”", "â€“": "–", "â€”": "—", "â€¦": "…", "Ã©": "é",
        "Ã¨": "è", "Ã¡": "á", "Ã": "A",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
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
    if t in REJECT_EXACT: return True
    for pattern in REJECT_PATTERNS:
        if re.match(pattern, t, flags=re.IGNORECASE): return True
    if len(t) >= 8 and len(set(t.lower())) <= 2: return True
    return False

def stable_id(class_id: str, chapter_id: str, pillar: str, asset: str, source_ref: str, sequence: int, text: str) -> str:
    material = "|".join([class_id, chapter_id, pillar, asset, source_ref, str(sequence), normalize_for_id(text)])
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:20]
    return f"{class_id}_{chapter_id}_{pillar}_{asset}_{sequence:04d}_{digest}"

def best_text(obj: dict[str, Any]) -> str:
    for field in TEXT_FIELDS:
        value = obj.get(field)
        if isinstance(value, str) and clean_text(value):
            return clean_text(value)
    return ""

def get_source_ref(obj: dict[str, Any], default: str) -> str:
    for field in ["source_ref", "source", "source_reference"]:
        value = obj.get(field)
        if value: return str(value)
    return default

def get_source_page(obj: dict[str, Any]) -> Any:
    for field in ["source_page", "page", "page_number"]:
        if field in obj: return obj[field]
    return None

def detect_type(text: str, asset_name: str, section: str = "") -> str:
    t = clean_text(text)
    low = t.lower()
    asset = asset_name.lower()
    if not t: return "empty"
    if "mcq" in asset: return "mcq"
    if "short_answer" in asset: return "short_answer"
    if "textbook_assessment" in asset: return "assessment_question"
    if "question" in asset:
        if "fill" in low or "................" in t or "______" in t: return "fill_in_the_blank"
        if "arrange" in low or "order" in low: return "ordering"
        if "spell" in low: return "spelling_selection"
        if t.endswith("?"): return "question"
        if re.match(r"^\d+[\.\)]\s*", t) and len(t) > 25: return "question"
    if "activity" in asset or "application" in asset: return "activity"
    if "worked" in asset: return "worked_practice"
    if "lesson" in asset: return "lesson"
    if "concept" in asset: return "concept"
    if "example" in asset: return "example"
    if "recall" in asset: return "revision_recall"
    if "key_points" in asset: return "revision_key_point"
    if "revision_activities" in asset: return "revision_activity"
    if "youtube" in asset: return "resource_search"
    if "portal" in asset: return "official_resource"
    if "video" in asset: return "video_resource"
    if "channel" in asset: return "channel_resource"
    if re.search(r"(^|\n)\s*[A-Z][A-Za-z ]{0,30}:\s+", t): return "dialogue"
    lines = [x.strip() for x in t.splitlines() if x.strip()]
    if len(lines) >= 3:
        short_lines = sum(1 for line in lines if len(line.split()) <= 10)
        if short_lines / len(lines) >= 0.65: return "poem"
    if len(t) <= 90 and (t.isupper() or low.startswith("let us ") or low in {"new words", "think and discuss", "just for fun"}):
        return "heading"
    return "paragraph"

def is_likely_fragment(text: str, asset_name: str) -> bool:
    t = clean_text(text)
    if not t: return True
    if "................" in t or "______" in t: return False
    if t.endswith("?") or t.endswith(".") or t.endswith("!") or t.endswith(":"): return False
    if re.match(r"^\d+[\.\)]\s+", t):
        words = t.split()
        if len(words) < 8: return True
        if words[-1].lower() in {"to", "for", "of", "in", "on", "at", "with", "and", "or", "but", "can", "where", "what", "how", "that", "the", "a", "an"}:
            return True
    if len(t.split()) <= 3: return True
    if "bbbbbbbb" in t.lower(): return True
    return False

# ------------------------------------------------------------
# Record Creation
# ------------------------------------------------------------

def make_record(*, class_id: str, chapter_id: str, chapter_title: str, pillar: str, asset_name: str, source_file: Path, obj: dict[str, Any], sequence: int, text: str, inherited_section: str = "", inherited_page: Any = None) -> dict[str, Any] | None:
    text = clean_text(text)
    if not text: return None
    source_ref = get_source_ref(obj, f"{source_file.name}::record:{sequence}")
    source_page = get_source_page(obj) or inherited_page
    section = clean_text(obj.get("section") or obj.get("section_title") or inherited_section)
    rec_type = detect_type(text, asset_name, section)
    fragment = is_likely_fragment(text, asset_name)
    status = str(obj.get("status") or "SOURCE_DERIVED").upper()
    generated = status == "GENERATED" or "90_GENERATED" in str(source_file)
    if "90_GENERATED" in str(source_file):
        status = "GENERATED"
        generated = True
    visibility = "student"
    if (fragment and not generated) or rec_type == "empty" or looks_like_reject(text):
        visibility = "internal"
    rid = stable_id(class_id, chapter_id, pillar, asset_name, source_ref, sequence, text)
    record = {
        "record_id": rid, "chapter_id": chapter_id, "chapter_title": chapter_title,
        "pillar": pillar, "asset": asset_name, "type": rec_type, "text": text,
        "visibility": visibility, "student_facing": visibility == "student",
        "content_origin": "GENERATED" if generated else "SOURCE_DERIVED",
        "status": status,
        "source": {
            "file": str(source_file.relative_to(PROJECT_ROOT)),
            "source_ref": source_ref, "source_page": source_page, "section": section,
        },
        "quality": {
            "is_fragment": fragment,
            "is_ocr_suspect": ("bbbbbbbb" in text.lower() or len(set(text.lower().replace(" ", ""))) <= 2),
        },
        "sequence": sequence,
    }
    for field in ["options", "answer", "answer_guidance", "source_basis", "metadata", "category", "difficulty", "skill", "tags"]:
        if field in obj: record[field] = obj[field]
    return record

def normalize_items(data: Any, asset_name: str) -> list[tuple[dict[str, Any], str, str, Any]]:
    result = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict): result.append((item, best_text(item), "", get_source_page(item)))
            elif isinstance(item, str): result.append(({}, clean_text(item), "", None))
        return result
    if not isinstance(data, dict): return result
    if isinstance(data.get("items"), list):
        for item in data["items"]:
            if isinstance(item, dict):
                result.append((item, best_text(item), clean_text(item.get("section") or item.get("section_title") or ""), get_source_page(item)))
            elif isinstance(item, str): result.append(({}, clean_text(item), "", None))
    for field in ["prompts", "key_points", "activities", "queries"]:
        values = data.get(field)
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict): result.append((item, best_text(item), "", get_source_page(item)))
                else: result.append(({"status": data.get("status", "SOURCE_DERIVED"), "source_basis": data.get("source_basis")}, clean_text(item), "", None))
    portals = data.get("recommended_portals")
    if isinstance(portals, list):
        for item in portals:
            if isinstance(item, dict):
                text = best_text(item) or clean_text(item.get("name") or item.get("title") or "")
                result.append((item, text, "", get_source_page(item)))
            else: result.append(({"status": data.get("status", "SOURCE_DERIVED")}, clean_text(item), "", None))
    return result

# ------------------------------------------------------------
# Chapter Processing
# ------------------------------------------------------------

def load_chapter_info(chapter_dir: Path) -> dict[str, Any]:
    info_path = chapter_dir / "00_CHAPTER_INFO" / "CHAPTER_INFO.json"
    if not info_path.exists():
        info_path = chapter_dir / "00_CHAPTER_INFO" / "chapter.json"
    if not info_path.exists(): return {}
    try:
        data = read_json(info_path)
        return data if isinstance(data, dict) else {}
    except: return {}

def load_full_chapter_source(chapter_dir: Path) -> dict[str, Any] | None:
    source_dir = chapter_dir / "01_LEARN" / "04_SOURCE_DERIVED"
    if not source_dir.exists(): return None
    for path in source_dir.glob("*.json"):
        try:
            data = read_json(path)
            if isinstance(data, dict) and ("pages" in data or "full_chapter_text" in path.name.lower()):
                return {"file": str(path.relative_to(PROJECT_ROOT)), "data": data}
        except: continue
    return None

def process_chapter(chapter_dir: Path, class_id: str) -> dict[str, Any]:
    info = load_chapter_info(chapter_dir)
    folder_name = chapter_dir.name
    chapter_id = clean_text(str(info.get("chapter_id") or (re.match(r"^(\d+)", folder_name).group(1) if re.match(r"^(\d+)", folder_name) else folder_name)))
    chapter_title = clean_text(info.get("chapter_title") or re.sub(r"^\d+[_\-\s]*", "", folder_name).replace("_", " "))

    subject_name = "unknown"
    try:
        rel = chapter_dir.relative_to(PROJECT_ROOT / "Contents" / f"Class {class_id.split('_')[1]}")
        parts = list(rel.parts)
        subject_name = parts[0]
    except: pass

    output_id = f"{class_id}_{slug(subject_name)}_{chapter_id}"
    package = {
        "schema_version": "canonical-runtime-v2", "adapter_version": ADAPTER_VERSION, "generated_at": utc_now(),
        "id": output_id, "chapter_id": chapter_id, "chapter_title": chapter_title,
        "title": chapter_title, # API compatibility
        "class_id": class_id, "class_name": f"Class {class_id.split('_')[1]}",
        "classId": class_id, # API compatibility
        "subject_id": slug(subject_name), "subject_name": subject_name,
        "subjectId": slug(subject_name), # API compatibility
        "source": {
            "chapter_folder": str(chapter_dir.relative_to(PROJECT_ROOT)),
            "source_pdf": info.get("source_pdf"), "page_count": info.get("page_count"),
            "grade": f"Class {class_id.split('_')[1]}", "textbook": info.get("textbook"),
            "source_authority": info.get("source_authority"), "source_preservation": info.get("source_preservation"),
        },
        "learn": [], "practice": [], "assess": [], "revise": [], "resources": [],
        "source_records": [], "source_document": load_full_chapter_source(chapter_dir),
        "traceability": {"chapter_info": info, "chapter_folder": str(chapter_dir.relative_to(PROJECT_ROOT)), "source_files": []},
        "accounting": {},
    }

    for pillar_dir_name, pillar in PILLAR_MAP.items():
        pillar_dir = chapter_dir / pillar_dir_name
        if not pillar_dir.exists(): continue
        asset_dirs = sorted([p for p in pillar_dir.iterdir() if p.is_dir()], key=lambda p: (ASSET_ORDER.get(p.name, 9999), p.name.lower()))
        for asset_dir in asset_dirs:
            for source_file in sorted(asset_dir.glob("*.json")):
                if "full_chapter_text" in source_file.name.lower():
                    package["traceability"]["source_files"].append(str(source_file.relative_to(PROJECT_ROOT)))
                    continue
                try:
                    data = read_json(source_file)
                except Exception as exc:
                    package["traceability"].setdefault("parse_errors", []).append({"file": str(source_file.relative_to(PROJECT_ROOT)), "error": str(exc)})
                    continue
                package["traceability"]["source_files"].append(str(source_file.relative_to(PROJECT_ROOT)))
                normalized = normalize_items(data, asset_dir.name)
                for local_index, (obj, text, inherited_section, inherited_page) in enumerate(normalized, start=1):
                    if not text: continue
                    record = make_record(class_id=class_id, chapter_id=chapter_id, chapter_title=chapter_title, pillar=pillar, asset_name=asset_dir.name, source_file=source_file, obj=obj, sequence=local_index, text=text, inherited_section=inherited_section, inherited_page=inherited_page)
                    if record:
                        package["source_records"].append(record)
                        if record["student_facing"]: package[pillar].append(record)

    # Ordering & Accounting
    for p in PILLAR_MAP.values():
        package[p].sort(key=lambda r: (r.get("source", {}).get("source_page") is None, r.get("source", {}).get("source_page") or 999999, r.get("asset", ""), r.get("sequence", 0), r.get("record_id", "")))

    student_ids = [r["record_id"] for r in (package["learn"] + package["practice"] + package["assess"] + package["revise"] + package["resources"])]
    source_ids = [r["record_id"] for r in package["source_records"]]

    package["accounting"] = {
        "student_facing_records": len(student_ids), "student_facing_unique_ids": len(set(student_ids)),
        "source_records": len(source_ids), "source_unique_ids": len(set(source_ids)),
        "internal_records": len(source_ids) - len(student_ids),
        "id_collision_count": len(student_ids) - len(set(student_ids)),
        "pillar_counts": {p: len(package[p]) for p in PILLAR_MAP.values()},
    }
    package["quality"] = {
        "has_duplicate_student_ids": package["accounting"]["id_collision_count"] > 0,
        "generated_records": sum(1 for r in package["source_records"] if r["student_facing"] and r.get("content_origin") == "GENERATED"),
        "source_derived_records": sum(1 for r in package["source_records"] if r["student_facing"] and r.get("content_origin") == "SOURCE_DERIVED"),
    }

    out_dir = STAGING_CHAPTERS / class_id / slug(subject_name)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_json(out_dir / f"{chapter_id}.json", package)
    return package

# ------------------------------------------------------------
# Build Orchestration
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Gurukul AI Canonical Runtime Materializer")
    parser.add_argument("--classes", nargs="+", default=["5", "6", "7"], help="Classes to process")
    args = parser.parse_args()

    print(f"GURUKUL AI — GENERIC CANONICAL ADAPTER {ADAPTER_VERSION}")
    print("=" * 60)

    if STAGING_ROOT.exists(): shutil.rmtree(STAGING_ROOT)
    STAGING_ROOT.mkdir(parents=True)

    all_packages = []
    total_expected = 183

    for cls_num in args.classes:
        class_id = f"class_{cls_num}"
        contents_root = PROJECT_ROOT / "Contents" / f"Class {cls_num}"
        if not contents_root.exists():
            print(f"WARNING: Contents root not found for Class {cls_num}")
            continue

        chapter_dirs = []
        for p in contents_root.rglob("01_LEARN"):
            chapter_dirs.append(p.parent)

        print(f"Processing Class {cls_num}: {len(chapter_dirs)} chapters found")
        for chapter_dir in sorted(chapter_dirs):
            print(f"  -> {chapter_dir.name}")
            pkg = process_chapter(chapter_dir, class_id)
            if pkg["accounting"]["id_collision_count"] > 0:
                print(f"CRITICAL ERROR: ID Collision in {chapter_dir}")
                sys.exit(1)
            all_packages.append(pkg)

    print("-" * 60)
    print(f"Total chapters processed: {len(all_packages)}")

    if len(all_packages) != total_expected:
        print(f"CRITICAL ERROR: Chapter count mismatch. Expected {total_expected}, got {len(all_packages)}")
        sys.exit(1)

    # Catalog
    catalog = {"schema_version": "canonical-catalog-v2", "generated_at": utc_now(), "classes": []}
    class_map = {}
    for pkg in all_packages:
        cid = pkg["class_id"]
        if cid not in class_map:
            class_map[cid] = {"id": cid, "name": pkg["class_name"], "subjects": []}
            catalog["classes"].append(class_map[cid])

        subj_map = {s["id"]: s for s in class_map[cid]["subjects"]}
        sid = pkg["subject_id"]
        if sid not in subj_map:
            subj_map[sid] = {"id": sid, "name": pkg["subject_name"], "chapters": []}
            class_map[cid]["subjects"].append(subj_map[sid])

        subj_map[sid]["chapters"].append({
            "id": pkg["id"], "chapter_id": pkg["chapter_id"], "title": pkg["chapter_title"],
            "classId": pkg["class_id"], "subjectId": pkg["subject_id"], # API compatibility
            "accounting": pkg["accounting"], "quality": pkg["quality"],
        })
    write_json(STAGING_ROOT / "catalog.json", catalog)

    # Search
    search_records = []
    for pkg in all_packages:
        for p in PILLAR_MAP.values():
            for r in pkg[p]:
                search_records.append({
                    "record_id": r["record_id"], "chapter_id": pkg["chapter_id"], "chapter_title": pkg["chapter_title"],
                    "class_id": pkg["class_id"], "subject_id": pkg["subject_id"], "pillar": p, "type": r["type"],
                    "text": r["text"], "source": r.get("source", {}),
                })
    write_json(STAGING_SEARCH / "index.json", {
        "schema_version": "canonical-search-v2", "record_count": len(search_records), "records": search_records
    })

    # Manifest
    manifest = {
        "adapter_version": ADAPTER_VERSION, "generated_at": utc_now(), "classes": args.classes,
        "class_count": len(args.classes), "chapter_count": len(all_packages),
        "student_facing_records": sum(p["accounting"]["student_facing_records"] for p in all_packages),
        "source_records": sum(p["accounting"]["source_records"] for p in all_packages),
        "student_id_collisions": 0,
    }
    write_json(STAGING_ROOT / "CANONICAL_RUNTIME_MANIFEST.json", manifest)

    # Reconciliation (Ground Truth compatibility)
    reconciliation = {"classes": {}, "grand_totals": {"processed": 0, "student_facing": 0, "internal": 0}}
    for pkg in all_packages:
        cid = pkg["class_id"]
        sid = pkg["subject_id"]
        chid = pkg["chapter_id"]

        # Calculate legacy counts for ground truth script
        st_count = sum(len(pkg[p]) for p in ["learn", "practice", "assess", "revise"])
        res_count = len(pkg["resources"])
        trace_count = len(pkg["traceability"])
        proc_count = st_count + res_count + trace_count

        reconciliation["classes"].setdefault(cid, {"subjects": {}, "totals": {"processed": 0, "student_facing": 0, "internal": 0}})
        reconciliation["classes"][cid]["subjects"].setdefault(sid, {"chapters": {}, "totals": {"processed": 0, "student_facing": 0, "internal": 0}, "processed": 0, "student_facing": 0, "internal": 0})

        reconciliation["classes"][cid]["subjects"][sid]["chapters"][chid] = {
            "processed": proc_count, "student_facing": st_count, "internal": res_count + trace_count,
            "counts": {p: len(pkg[p]) for p in PILLAR_MAP.values()} | {"traceability": trace_count}
        }

        reconciliation["classes"][cid]["subjects"][sid]["processed"] += proc_count
        reconciliation["classes"][cid]["subjects"][sid]["student_facing"] += st_count
        reconciliation["classes"][cid]["subjects"][sid]["internal"] += (res_count + trace_count)

        reconciliation["classes"][cid]["totals"]["processed"] += proc_count
        reconciliation["classes"][cid]["totals"]["student_facing"] += st_count
        reconciliation["classes"][cid]["totals"]["internal"] += (res_count + trace_count)

        reconciliation["grand_totals"]["processed"] += proc_count
        reconciliation["grand_totals"]["student_facing"] += st_count
        reconciliation["grand_totals"]["internal"] += (res_count + trace_count)

    write_json(STAGING_ROOT / "CANONICAL_RUNTIME_RECONCILIATION.json", reconciliation)

    # Atomic Swap
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = RUNTIME_ROOT / "backups" / ts
    backup_dir.mkdir(parents=True, exist_ok=True)

    if FINAL_CHAPTERS.exists(): shutil.move(str(FINAL_CHAPTERS), str(backup_dir / "chapters"))
    if FINAL_SEARCH.exists(): shutil.move(str(FINAL_SEARCH), str(backup_dir / "search"))
    for f in ["catalog.json", "CANONICAL_RUNTIME_MANIFEST.json", "CANONICAL_RUNTIME_RECONCILIATION.json"]:
        if (RUNTIME_ROOT / f).exists(): shutil.move(str(RUNTIME_ROOT / f), str(backup_dir / f))

    shutil.move(str(STAGING_CHAPTERS), str(FINAL_CHAPTERS))
    shutil.move(str(STAGING_SEARCH), str(FINAL_SEARCH))
    shutil.move(str(STAGING_ROOT / "catalog.json"), str(RUNTIME_ROOT / "catalog.json"))
    shutil.move(str(STAGING_ROOT / "CANONICAL_RUNTIME_MANIFEST.json"), str(RUNTIME_ROOT / "CANONICAL_RUNTIME_MANIFEST.json"))
    shutil.move(str(STAGING_ROOT / "CANONICAL_RUNTIME_RECONCILIATION.json"), str(RUNTIME_ROOT / "CANONICAL_RUNTIME_RECONCILIATION.json"))

    # Also update the root reconciliation file which ground truth script uses
    shutil.copy(str(RUNTIME_ROOT / "CANONICAL_RUNTIME_RECONCILIATION.json"), str(PROJECT_ROOT / "RECORD_COUNT_RECONCILIATION.json"))

    print("ATOMIC BUILD SUCCESSFUL")
    print(f"Backup created at: {backup_dir}")

if __name__ == "__main__":
    main()

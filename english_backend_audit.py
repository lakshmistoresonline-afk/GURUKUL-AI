import json
import collections
from pathlib import Path

ROOT = Path(r"D:\GURUKUL-AI\runtime-data\chapters\class_5\01_english_complete")

print()
print("=" * 70)
print("CLASS 5 ENGLISH — BACKEND CONTENT AUDIT")
print("=" * 70)
print()

pillars = [
    "learn",
    "practice",
    "assess",
    "revise",
    "resources",
]

files = sorted(
    ROOT.glob("*.json"),
    key=lambda p: int(p.stem) if p.stem.isdigit() else 9999
)

for file in files:

    if not file.stem.isdigit():
        continue

    try:
        data = json.loads(
            file.read_text(encoding="utf-8")
        )
    except Exception as e:
        print(f"ERROR READING {file.name}: {e}")
        continue

    records = []

    for pillar in pillars:
        records.extend(
            data.get(pillar, [])
        )

    type_counts = collections.Counter(
        record.get("type", "UNKNOWN")
        for record in records
    )

    generated = sum(
        record.get("content_origin") == "GENERATED"
        for record in records
    )

    source_derived = sum(
        record.get("content_origin") == "SOURCE_DERIVED"
        for record in records
    )

    accounting = data.get(
        "accounting",
        {}
    )

    print(
        f"{data.get('chapter_id')} — "
        f"{data.get('chapter_title')}"
    )

    print(
        "  PILLARS:"
    )

    for pillar in pillars:
        print(
            f"    {pillar:10}: "
            f"{len(data.get(pillar, []))}"
        )

    print(
        f"  TYPES: {dict(type_counts)}"
    )

    print(
        f"  GENERATED: {generated}"
    )

    print(
        f"  SOURCE-DERIVED: {source_derived}"
    )

    print(
        f"  INTERNAL: "
        f"{accounting.get('internal_records', 0)}"
    )

    print(
        f"  ID COLLISIONS: "
        f"{accounting.get('id_collision_count', 0)}"
    )

    print()

print("=" * 70)
print("AUDIT COMPLETE")
print("=" * 70)
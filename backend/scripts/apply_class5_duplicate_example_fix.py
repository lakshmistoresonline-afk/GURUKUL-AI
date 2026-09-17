from pathlib import Path

path = Path(r"D:\GURUKUL-AI\backend\scripts\canonical_adapter_class5.py")
text = path.read_text(encoding="utf-8")

# ============================================================
# PATCH 1: Add presentation-artifact cleaning
# ============================================================

old = '''def clean_text(value: Any) -> str:
    if value is None:
        return ""

    text = str(value)

    replacements = {
'''

new = '''def clean_text(value: Any) -> str:
    if value is None:
        return ""

    text = str(value)

    replacements = {
'''

if old not in text:
    raise RuntimeError("PATCH 1 anchor not found")

# Keep existing replacements intact; artifact removal is inserted
# after the existing replacement loop.

old = '''    for old, new in replacements.items():
        text = text.replace(old, new)

    # Preserve meaningful line structure but remove excessive whitespace.
    text = text.replace("\\r\\n", "\\n").replace("\\r", "\\n")
    text = re.sub(r"[ \\t]+", " ", text)
    text = re.sub(r"\\n{3,}", "\\n\\n", text)

    return text.strip()
'''

new = '''    for old, new in replacements.items():
        text = text.replace(old, new)

    # --------------------------------------------------------
    # Student-presentation artifact removal
    # --------------------------------------------------------
    # These are print-production / OCR artifacts rather than
    # educational content. Original source files remain untouched.
    text = re.sub(
        r"(?im)^\\s*Reprint\\s+20\\d{2}-\\d{2}\\s*$",
        "",
        text,
    )

    # Examples:
    #   Chapter 1.indd 1
    #   Chapter 1.indd 1 09-06-2025 15:24:17
    #   Chapter 12.indd 12
    text = re.sub(
        r"(?im)^\\s*Chapter\\s+\\d+\\.indd\\s+\\d+(?:\\s+\\d{2}-\\d{2}-\\d{4}\\s+\\d{2}:\\d{2}:\\d{2})?\\s*$",
        "",
        text,
    )

    # Generic InDesign extraction artifact if it occurs inline.
    text = re.sub(
        r"\\s*Chapter\\s+\\d+\\.indd\\s+\\d+(?:\\s+\\d{2}-\\d{2}-\\d{4}\\s+\\d{2}:\\d{2}:\\d{2})?",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Preserve meaningful line structure but remove excessive whitespace.
    text = text.replace("\\r\\n", "\\n").replace("\\r", "\\n")
    text = re.sub(r"[ \\t]+", " ", text)
    text = re.sub(r"\\n{3,}", "\\n\\n", text)

    return text.strip()
'''

if old not in text:
    raise RuntimeError("PATCH 1B anchor not found")

text = text.replace(old, new, 1)

# ============================================================
# PATCH 2: Add duplicate-example tracking
# ============================================================

old = '''    # --------------------------------------------------------
    # Process each pillar.
    # --------------------------------------------------------

    for pillar_dir_name, pillar in PILLAR_MAP.items():
'''

new = '''    # --------------------------------------------------------
    # Process each pillar.
    # --------------------------------------------------------

    # Normalized Lesson text is used only to detect redundant
    # EXAMPLES records. Original source records are ALWAYS kept.
    lesson_text_keys: set[str] = set()

    for pillar_dir_name, pillar in PILLAR_MAP.items():
'''

if old not in text:
    raise RuntimeError("PATCH 2 anchor not found")

text = text.replace(old, new, 1)

# ============================================================
# PATCH 3: Capture Lesson text and suppress duplicate Examples
# ============================================================

old = '''                    # Source records are always preserved.
                    package[
                        "source_records"
                    ].append(record)

                    # Student-facing records only enter their
                    # corresponding pillar array.
                    if record["student_facing"]:
                        package[pillar].append(
                            record
                        )
'''

new = '''                    # ------------------------------------------------
                    # Source records are ALWAYS preserved.
                    # ------------------------------------------------
                    package[
                        "source_records"
                    ].append(record)

                    # ------------------------------------------------
                    # Record canonical Lesson text.
                    # ------------------------------------------------
                    # Only Learn/01_LESSONS establishes the baseline
                    # against which duplicate Examples are checked.
                    if (
                        pillar == "learn"
                        and asset_dir.name == "01_LESSONS"
                        and record["student_facing"]
                    ):
                        lesson_text_keys.add(
                            normalize_for_id(record["text"])
                        )

                    # ------------------------------------------------
                    # Suppress exact duplicate Examples.
                    # ------------------------------------------------
                    # EXAMPLES.json is preserved in source_records, but
                    # if its cleaned normalized text is already present
                    # as Lesson content, it must not become another
                    # student-facing card.
                    if (
                        pillar == "learn"
                        and asset_dir.name == "03_EXAMPLES"
                        and record["student_facing"]
                        and normalize_for_id(record["text"])
                        in lesson_text_keys
                    ):
                        record["student_facing"] = False
                        record["visibility"] = "internal"
                        record["duplicate_of"] = "01_LESSONS"
                        record["suppression_reason"] = (
                            "EXACT_DUPLICATE_OF_LESSON_CONTENT"
                        )

                    # Student-facing records only enter their
                    # corresponding pillar array.
                    if record["student_facing"]:
                        package[pillar].append(
                            record
                        )
'''

if old not in text:
    raise RuntimeError("PATCH 3 anchor not found")

text = text.replace(old, new, 1)

# ============================================================
# PATCH 4: Add accounting for suppressed duplicate Examples
# ============================================================

old = '''        "internal_records": sum(
            1
            for r in all_source
            if not r["student_facing"]
        ),
        "id_collision_count": (
'''

new = '''        "internal_records": sum(
            1
            for r in all_source
            if not r["student_facing"]
        ),
        "suppressed_duplicate_examples": sum(
            1
            for r in all_source
            if r.get("suppression_reason")
            == "EXACT_DUPLICATE_OF_LESSON_CONTENT"
        ),
        "id_collision_count": (
'''

if old not in text:
    raise RuntimeError("PATCH 4 anchor not found")

text = text.replace(old, new, 1)

# ============================================================
# PATCH 5: Add quality metric
# ============================================================

old = '''        "internal_fragment_records": sum(
            1
            for r in all_source
            if not r["student_facing"]
        ),
    }
'''

new = '''        "internal_fragment_records": sum(
            1
            for r in all_source
            if not r["student_facing"]
        ),
        "suppressed_duplicate_examples": sum(
            1
            for r in all_source
            if r.get("suppression_reason")
            == "EXACT_DUPLICATE_OF_LESSON_CONTENT"
        ),
    }
'''

if old not in text:
    raise RuntimeError("PATCH 5 anchor not found")

text = text.replace(old, new, 1)

# ============================================================
# PATCH 6: Make the audit explicitly report duplicate suppression
# ============================================================

old = '''                f"  Source: {acc['source_records']}",
                f"  ID collisions: {acc['id_collision_count']}",
                f"  Generated: {quality['generated_records']}",
'''

new = '''                f"  Source: {acc['source_records']}",
                f"  ID collisions: {acc['id_collision_count']}",
                f"  Suppressed duplicate Examples: {acc.get('suppressed_duplicate_examples', 0)}",
                f"  Generated: {quality['generated_records']}",
'''

if old not in text:
    raise RuntimeError("PATCH 6 anchor not found")

text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")
print("PATCH APPLIED SUCCESSFULLY")
print(f"Adapter: {path}")
print(f"Backup : {path}.backup_before_duplicate_example_fix_*")

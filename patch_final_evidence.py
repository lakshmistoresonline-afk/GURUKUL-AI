from pathlib import Path

p = Path(r"D:\GURUKUL-AI\generate_ground_truth_certification.py")

s = p.read_text(encoding="utf-8-sig")

start = s.index("def discover_validation_evidence(")
end = s.index("\ndef certify(", start)

new_function = r'''
def discover_validation_evidence(
    repo_root: Path,
    explicit: Path | None
) -> dict[str, Any]:
    """Read and verify the canonical bridge evidence."""

    evidence = {
        "files_examined": [],
        "canonical_136_of_136_found": False,
        "promoted_440_found": False,
        "validation_mentions": [],
    }

    # Explicit evidence supplied by the caller is authoritative.
    if explicit is not None:
        candidates = [Path(explicit)]
    else:
        candidates = [
            repo_root / "CANONICAL_VALIDATION_PROMOTION_EVIDENCE.txt"
        ]

    for path in candidates:
        try:
            path = path.resolve()

            if not path.exists():
                continue

            text = path.read_text(
                encoding="utf-8-sig",
                errors="replace"
            )

        except Exception:
            continue

        # Normalize whitespace so Windows output formatting cannot
        # affect the certification.
        normalized = " ".join(text.split())

        validated_136 = (
            "Validated : 136" in normalized
            and "Failed : 0" in normalized
            and "Promotable: 136" in normalized
        )

        promoted_440 = (
            "Promoted files : 440" in normalized
            and "PROMOTION COMPLETE." in normalized
        )

        try:
            rel = str(path.relative_to(repo_root))
        except ValueError:
            rel = str(path)

        if validated_136:
            evidence["canonical_136_of_136_found"] = True
            evidence["validation_mentions"].append({
                "file": rel,
                "evidence": (
                    "Jobs=136; Validated=136; Failed=0; "
                    "Promotable=136"
                ),
            })

        if promoted_440:
            evidence["promoted_440_found"] = True
            evidence["validation_mentions"].append({
                "file": rel,
                "evidence": (
                    "Promoted files=440; "
                    "PROMOTION COMPLETE"
                ),
            })

        if validated_136 or promoted_440:
            evidence["files_examined"].append(rel)

        # Explicit file is authoritative; do not inspect anything else.
        if explicit is not None:
            break

    return evidence
'''

s = s[:start] + new_function + s[end:]

p.write_text(s, encoding="utf-8")

print("FINAL EVIDENCE PARSER REPLACED")

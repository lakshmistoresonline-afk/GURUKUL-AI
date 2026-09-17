from __future__ import annotations
import json, re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\GURUKUL-AI")
SOURCE = ROOT / "Contents"
OUT_JSON = ROOT / "CHAPTER_FORENSIC_V8.json"
OUT_MD = ROOT / "CHAPTER_FORENSIC_V8.md"

EXPECTED = {"class_5": 47, "class_6": 64, "class_7": 72}
EXCLUDED = {
    "GURUKUL_AI_CHAPTER_RESOURCE_PACK_V1",
    "Contents_HARDENED",
    "Contents_HARDENED_FINAL",
    "Contents_HARDENED_FINAL_V7",
    "Contents_HARDENED_FINAL_V7_1",
}

CLASS_RE = re.compile(r"^Class[\s_-]*0*([567])$", re.I)
CHAPTER_RE = re.compile(r"^(\d{3})_(.+)$", re.I)

STRONG_DIRS = {
    "00_CHAPTER_INFO","01_LEARN","02_PRACTICE","03_ASSESS",
    "04_REVISE","05_RESOURCES","99_INTERNAL_TRACEABILITY"
}

def now():
    return datetime.now(timezone.utc).isoformat()

def excluded(p):
    try:
        return any(x in EXCLUDED for x in p.relative_to(SOURCE).parts)
    except ValueError:
        return True

def class_id(path):
    for part in path.parts:
        m = CLASS_RE.match(part)
        if m:
            return f"class_{m.group(1)}"
    return None

def chapter_parts(name):
    m = CHAPTER_RE.match(name)
    if not m:
        return None, None
    return m.group(1), re.sub(r"\s+", " ", m.group(2).replace("_"," ").strip())

def rel(p):
    return str(p.relative_to(SOURCE))

def immediate_signature(p):
    dirs = sorted(x.name.upper() for x in p.iterdir() if x.is_dir())
    files = sorted(x.name.upper() for x in p.iterdir() if x.is_file())
    return dirs, files

def has_chapter_info(p):
    return (p / "00_CHAPTER_INFO" / "CHAPTER_INFO.json").is_file()

def has_strong_content(p):
    dirs = {x.name.upper() for x in p.iterdir() if x.is_dir()}
    return len(dirs & STRONG_DIRS) >= 2

def has_any_content(p):
    dirs = {x.name.upper() for x in p.iterdir() if x.is_dir()}
    return bool(dirs & STRONG_DIRS)

def find_candidates():
    rows = []
    seen = set()

    # Walk directories once. A candidate must have a chapter-style name.
    for p in SOURCE.rglob("*"):
        if not p.is_dir() or excluded(p):
            continue
        cid, title = chapter_parts(p.name)
        if not cid:
            continue
        c = class_id(p)
        if c not in EXPECTED:
            continue

        dirs, files = immediate_signature(p)
        info = has_chapter_info(p)
        strong = has_strong_content(p)
        any_content = has_any_content(p)

        # Determine package/ancestor path, but do not collapse anything.
        rp = p.relative_to(SOURCE).parts
        ci = next(i for i,x in enumerate(rp) if class_id(Path(x)) == c)
        ancestors = list(rp[ci+1:-1])
        package = ancestors[0] if ancestors else ""
        inner = ancestors[1:] if len(ancestors) > 1 else []

        if info:
            category = "CHAPTER_INFO_ANCHORED"
            confidence = "HIGH"
            reason = "Contains 00_CHAPTER_INFO/CHAPTER_INFO.json"
        elif strong:
            category = "CANONICAL_CONTENT_ROOT"
            confidence = "HIGH"
            reason = "Contains at least two canonical content directories"
        elif any_content:
            category = "WEAK_CONTENT_ROOT"
            confidence = "MEDIUM"
            reason = "Contains one canonical content directory"
        else:
            category = "NUMERIC_DIRECTORY_ONLY"
            confidence = "LOW"
            reason = "3-digit chapter-style directory without canonical content"

        key = (c, rel(p).lower())
        if key in seen:
            continue
        seen.add(key)

        rows.append({
            "class_id": c,
            "chapter_id": cid,
            "chapter_title": title,
            "path": rel(p),
            "package": package,
            "inner_ancestors": inner,
            "category": category,
            "confidence": confidence,
            "reason": reason,
            "has_chapter_info": info,
            "canonical_dirs": sorted(set(dirs) & STRONG_DIRS),
            "all_immediate_dirs": dirs,
            "immediate_files": files,
        })
    return rows

def build_report(rows):
    by_cat = Counter(r["category"] for r in rows)
    by_class_cat = Counter((r["class_id"], r["category"]) for r in rows)

    strong = [
        r for r in rows
        if r["category"] in {"CHAPTER_INFO_ANCHORED","CANONICAL_CONTENT_ROOT"}
    ]

    # Candidate inventory using path uniqueness. This is intentionally not
    # declared as the final 183 until the report shows the actual paths.
    unique_strong = {}
    for r in strong:
        key = (r["class_id"], r["path"].lower())
        unique_strong[key] = r

    report = {
        "schema_version": "GURUKUL_CHAPTER_FORENSIC_V8",
        "generated_at": now(),
        "source": str(SOURCE),
        "total_chapter_style_directories": len(rows),
        "category_counts": dict(by_cat),
        "class_category_counts": {
            f"{c}|{cat}": n for (c,cat),n in sorted(by_class_cat.items())
        },
        "strong_candidate_count": len(unique_strong),
        "strong_candidates_by_class": dict(Counter(
            r["class_id"] for r in unique_strong.values()
        )),
        "expected": EXPECTED,
        "candidates": rows,
    }

    # Identify duplicate chapter numbers within each class. These are expected
    # in split packages, so paths/packages are shown instead of treating them
    # as errors.
    groups = defaultdict(list)
    for r in rows:
        groups[(r["class_id"], r["chapter_id"])].append(r)
    duplicates = []
    for k, vals in sorted(groups.items()):
        if len(vals) > 1:
            duplicates.append({
                "class_id": k[0],
                "chapter_id": k[1],
                "count": len(vals),
                "paths": [v["path"] for v in vals]
            })
    report["same_number_multiple_paths"] = duplicates

    return report

def write_md(report):
    cc = Counter()
    for r in report["candidates"]:
        cc[(r["class_id"], r["category"])] += 1

    lines = [
        "# GURUKUL AI — CHAPTER FORENSIC V8",
        "",
        f"Source: `{SOURCE}`",
        "",
        "## Summary",
        "",
        f"- Chapter-style directories: **{report['total_chapter_style_directories']}**",
        f"- Strong candidates: **{report['strong_candidate_count']}**",
        "",
        "| Class | Expected | Chapter-info | Canonical | Weak | Numeric-only |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for c,n in EXPECTED.items():
        lines.append(
            f"| {c} | {n} | {cc[(c,'CHAPTER_INFO_ANCHORED')]} | "
            f"{cc[(c,'CANONICAL_CONTENT_ROOT')]} | "
            f"{cc[(c,'WEAK_CONTENT_ROOT')]} | "
            f"{cc[(c,'NUMERIC_DIRECTORY_ONLY')]} |"
        )

    lines += [
        "",
        "## Same chapter number at multiple paths",
        "",
        "These are NOT automatically errors; split packages can legitimately "
        "reuse chapter numbers.",
        "",
    ]
    for x in report["same_number_multiple_paths"]:
        lines.append(f"### {x['class_id']} / {x['chapter_id']} ({x['count']} paths)")
        for p in x["paths"]:
            lines.append(f"- `{p}`")

    lines += [
        "",
        "## Candidate paths",
        "",
    ]
    for r in sorted(report["candidates"], key=lambda x: (
        x["class_id"], x["chapter_id"], x["path"].lower()
    )):
        lines.append(
            f"- **{r['category']}** `{r['class_id']}/{r['chapter_id']}` "
            f"`{r['path']}` — {r['reason']}"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

def main():
    if not SOURCE.is_dir():
        raise SystemExit(f"Source not found: {SOURCE}")
    rows = find_candidates()
    report = build_report(rows)
    OUT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )
    write_md(report)

    print("="*78)
    print("GURUKUL AI — CHAPTER FORENSIC V8")
    print("="*78)
    print(f"Chapter-style dirs : {report['total_chapter_style_directories']}")
    print(f"Strong candidates  : {report['strong_candidate_count']}")
    for c in EXPECTED:
        print(
            f"{c:10} expected={EXPECTED[c]:3} "
            f"anchored={sum(1 for r in rows if r['class_id']==c and r['category']=='CHAPTER_INFO_ANCHORED'):3} "
            f"canonical={sum(1 for r in rows if r['class_id']==c and r['category']=='CANONICAL_CONTENT_ROOT'):3} "
            f"weak={sum(1 for r in rows if r['class_id']==c and r['category']=='WEAK_CONTENT_ROOT'):3} "
            f"numeric={sum(1 for r in rows if r['class_id']==c and r['category']=='NUMERIC_DIRECTORY_ONLY'):3}"
        )
    print(f"JSON report : {OUT_JSON}")
    print(f"MD report   : {OUT_MD}")
    print("="*78)

if __name__ == "__main__":
    main()

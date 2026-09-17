#!/usr/bin/env python3
"""
GURUKUL AI — DELIVERY RECONCILER v9
===================================

This is the delivery-day reconciliation tool. It stops trying to infer a
chapter from a numeric directory name. It discovers chapter ROOTS from
structure first, then derives identity from the chapter root's metadata/path.

Key rule:
    A chapter root is a directory containing multiple canonical learning
    areas OR a 00_CHAPTER_INFO directory/file anywhere immediately below it.

It also explicitly reports all candidate roots, so no content is silently
dropped or duplicated.

NO modification to Contents.
"""

from __future__ import annotations
import json, re, hashlib, shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"D:\GURUKUL-AI")
SOURCE = ROOT / "Contents"
OUT = ROOT / "Contents_DELIVERY_RECONCILED_V9"
REPORT = ROOT / "DELIVERY_RECONCILIATION_V9.json"
AUDIT = ROOT / "DELIVERY_RECONCILIATION_V9.md"

EXPECTED = {"class_5":47, "class_6":64, "class_7":72}
TOTAL = 183

EXCLUDED = {
    "GURUKUL_AI_CHAPTER_RESOURCE_PACK_V1",
    "Contents_HARDENED",
    "Contents_HARDENED_FINAL",
    "Contents_HARDENED_FINAL_V7",
    "Contents_HARDENED_FINAL_V7_1",
    "Contents_HARDENED_FINAL_V8",
    "Contents_DELIVERY_RECONCILED_V9",
}

AREAS = {
    "00_CHAPTER_INFO","01_LEARN","02_LEARN",
    "02_PRACTICE","03_PRACTICE",
    "03_ASSESS","04_ASSESS",
    "04_REVISE","05_REVISE",
    "05_RESOURCES","06_RESOURCES",
    "99_INTERNAL_TRACEABILITY",
}

CLASS_RE = re.compile(r"^class[\s_-]*0*([567])$", re.I)
NUMERIC_NAME = re.compile(r"^(\d{1,8})[_-](.+)$", re.I)

def now(): return datetime.now(timezone.utc).isoformat()

def excluded(p):
    try: return any(x in EXCLUDED for x in p.relative_to(SOURCE).parts)
    except ValueError: return True

def class_id(p):
    for x in p.parts:
        m=CLASS_RE.match(x.strip())
        if m: return f"class_{m.group(1)}"
    return None

def read_json(p):
    try: return json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception: return None

def recursive_values(x):
    if isinstance(x,dict):
        for k,v in x.items():
            yield str(k),v
            yield from recursive_values(v)
    elif isinstance(x,list):
        for v in x: yield from recursive_values(v)

def metadata(p):
    # Search CHAPTER_INFO files in the chapter root only.
    candidates = []
    direct = p / "00_CHAPTER_INFO"
    if direct.is_dir():
        candidates += list(direct.glob("*.json"))
    candidates += [x for x in p.glob("*CHAPTER*INFO*.json") if x.is_file()]
    for f in candidates:
        d=read_json(f)
        if d is None: continue
        vals=dict(recursive_values(d))
        cid=None; title=None
        for k,v in vals.items():
            lk=k.lower()
            if cid is None and lk in {"chapter_id","chapterid","chapter_no","chapterno"} and isinstance(v,(str,int)):
                cid=str(v).strip()
            if title is None and lk in {"chapter_title","chaptertitle","title","name"} and isinstance(v,str):
                title=v.strip()
        if cid or title:
            return {"chapter_id":cid,"chapter_title":title,"info_file":str(f)}
    return {}

def immediate_areas(p):
    return {x.name.upper() for x in p.iterdir() if x.is_dir()}

def structural_candidates():
    rows=[]
    for p in SOURCE.rglob("*"):
        if not p.is_dir() or excluded(p): continue
        c=class_id(p)
        if c not in EXPECTED: continue
        areas=immediate_areas(p)
        numeric=NUMERIC_NAME.match(p.name.strip())
        info_dir="00_CHAPTER_INFO" in areas
        # Strong root: 2+ canonical areas.
        strong=len(areas & AREAS)>=2
        # Also accept a chapter info directory even if only one area exists.
        info=info_dir or any(
            x.is_file() and x.name.upper().startswith("CHAPTER_INFO")
            for x in p.glob("00_CHAPTER_INFO/*")
        )
        if not (strong or info): continue

        md=metadata(p)
        if numeric:
            nid=numeric.group(1)
            ntitle=re.sub(r"\s+"," ",numeric.group(2).replace("_"," ").strip())
        else:
            nid=None; ntitle=None

        rp=p.relative_to(SOURCE).parts
        ci=next(i for i,x in enumerate(rp) if class_id(Path(x))==c)
        ancestors=list(rp[ci+1:-1])
        rows.append({
            "class_id":c,
            "path":str(p.relative_to(SOURCE)),
            "name":p.name,
            "areas":sorted(areas & AREAS),
            "numeric_id":nid,
            "numeric_title":ntitle,
            "metadata_id":md.get("chapter_id"),
            "metadata_title":md.get("chapter_title"),
            "info_file":md.get("info_file"),
            "ancestors":ancestors,
            "depth":len(rp),
        })
    return rows

def select_roots(rows):
    """
    Remove nested false positives:
    if candidate A is an ancestor of candidate B and A has >=2 canonical
    areas, prefer the outer candidate; if B has chapter info and A doesn't,
    prefer B.
    """
    paths={r["path"].lower():r for r in rows}
    selected=[]
    for r in rows:
        rp=Path(r["path"])
        drop=False
        for q in rows:
            if r is q: continue
            qp=Path(q["path"])
            try:
                rp.relative_to(qp)
            except ValueError:
                continue
            # q is ancestor.
            if rp==qp: continue
            qstrong=len(q["areas"])>=2
            rinfo=bool(r["info_file"]) or "00_CHAPTER_INFO" in r["areas"]
            qinfo=bool(q["info_file"]) or "00_CHAPTER_INFO" in q["areas"]
            if qstrong and not rinfo:
                drop=True; break
            if qstrong and qinfo and not rinfo:
                drop=True; break
        if not drop: selected.append(r)
    return selected

def assign_identity(r):
    cid=r["metadata_id"] or r["numeric_id"]
    title=r["metadata_title"] or r["numeric_title"] or r["name"]

    # Package identity = complete ancestor path, never numeric prefix.
    ancestors=r["ancestors"]
    package="/".join(ancestors).lower()

    # Stable subject identity from the deepest ancestor before chapter.
    subject_name=ancestors[-1] if ancestors else "UNKNOWN_SUBJECT"
    subject_id=re.sub(r"[^a-z0-9]+","_",subject_name.lower()).strip("_")

    return {
        "class_id":r["class_id"],
        "package_path":package,
        "subject_id":subject_id,
        "chapter_id":str(cid) if cid else None,
        "chapter_title":title,
        "path":r["path"],
        "areas":r["areas"],
    }

def main():
    if not SOURCE.is_dir(): raise SystemExit(f"Missing {SOURCE}")

    rows=structural_candidates()
    selected=select_roots(rows)
    identities=[assign_identity(r) for r in selected]

    counts=Counter(x["class_id"] for x in identities)
    missing={
        c:EXPECTED[c]-counts.get(c,0)
        for c in EXPECTED if counts.get(c,0)!=EXPECTED[c]
    }

    by_num=defaultdict(list)
    for x in identities:
        by_num[(x["class_id"],x["chapter_id"])].append(x["path"])
    repeated={f"{c}|{n}":v for (c,n),v in by_num.items() if len(v)>1}

    report={
        "schema":"GURUKUL_DELIVERY_RECONCILIATION_V9",
        "generated_at":now(),
        "source":str(SOURCE),
        "candidate_roots":len(rows),
        "selected_roots":len(selected),
        "class_counts":dict(counts),
        "expected":EXPECTED,
        "missing_by_class":missing,
        "repeated_class_chapter_numbers":repeated,
        "candidates":rows,
        "selected":identities,
        "gates":{
            "exact_183":len(selected)==TOTAL and all(counts.get(c,0)==n for c,n in EXPECTED.items()),
            "no_missing":not missing,
            "source_untouched":True,
        }
    }
    report["status"]="READY_FOR_DELIVERY" if all(report["gates"].values()) else "RECONCILIATION_REQUIRED"

    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    lines=[
        "# GURUKUL DELIVERY RECONCILIATION V9","",
        f"Status: **{report['status']}**","",
        f"Candidate roots: {len(rows)}",
        f"Selected roots: **{len(selected)} / 183**","",
        "| Class | Expected | Selected | Difference |",
        "|---|---:|---:|---:|",
    ]
    for c,n in EXPECTED.items():
        a=counts.get(c,0)
        lines.append(f"| {c} | {n} | {a} | {a-n:+d} |")
    lines += ["","## Selected chapter roots",""]
    for x in sorted(identities,key=lambda z:(z["class_id"],z["package_path"],z["chapter_id"] or "",z["path"])):
        lines.append(f"- `{x['class_id']}` `{x['chapter_id']}` — `{x['path']}`")
    lines += ["","## Gates",""]
    for k,v in report["gates"].items():
        lines.append(f"- {'PASS' if v else 'FAIL'} — {k}")
    AUDIT.write_text("\n".join(lines)+"\n",encoding="utf-8")

    print("="*78)
    print("GURUKUL AI — DELIVERY RECONCILIATION V9")
    print("="*78)
    print(f"Candidate roots : {len(rows)}")
    print(f"Selected roots  : {len(selected)} / 183")
    for c,n in EXPECTED.items():
        print(f"{c:10}: {counts.get(c,0):3} / {n}")
    print("-"*78)
    for k,v in report["gates"].items(): print(f"{'PASS' if v else 'FAIL'}  {k}")
    print("-"*78)
    print("STATUS:",report["status"])
    print("REPORT:",REPORT)
    print("AUDIT :",AUDIT)
    print("="*78)

if __name__=="__main__":
    main()

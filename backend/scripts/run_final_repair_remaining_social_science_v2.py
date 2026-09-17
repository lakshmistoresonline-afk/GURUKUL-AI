#!/usr/bin/env python3
"""
GURUKUL AI — Final surgical repair, v2.

Important fix:
The previous script selected RAW_GENERATED.json by chapter ID alone.
This version selects the exact Class 7 Social Science Part 2 job by JOB.json
chapter metadata, so duplicate chapter IDs cannot cause the wrong RAW file
to be edited.

Only repairs fields already present as items:
105: assess[0..5].question
106: assess[0..5].question, revise[0].point

It never promotes.
"""
import argparse, json, re, time
from pathlib import Path
from urllib.request import Request, urlopen

MODEL = "qwen3.5:2b-q4_K_M"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

TARGETS = {
    "105": {
        "title": "India, a Home to Many",
        "subject": "03_SOCIAL_SCIENCE_GRADE7_PART2",
        "fields": [("assess", i, "question") for i in range(6)],
    },
    "106": {
        "title": "The State, the Government, and You",
        "subject": "03_SOCIAL_SCIENCE_GRADE7_PART2",
        "fields": [("assess", i, "question") for i in range(6)]
                 + [("revise", 0, "point")],
    },
}

BAD = [
    "which source", "source section", "chapter-specific",
    "validation", "validator", "json", "field name",
    "placeholder", "fill in", "missing field", "provide the missing",
    "i cannot", "as an ai", "based on the prompt",
]

def load(p):
    with open(p, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save(p, d):
    tmp = Path(str(p) + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(p)

def job_matches(job, cid, spec):
    ch = job.get("chapter", {})
    return (
        str(ch.get("chapter_id", "")) == cid
        and ch.get("class_name") == "Class 7"
        and ch.get("subject_name") == spec["subject"]
        and ch.get("chapter_title") == spec["title"]
    )

def find_exact_job(run, cid, spec):
    found = []
    for jp in Path(run).glob("jobs/**/JOB.json"):
        try:
            j = load(jp)
            if job_matches(j, cid, spec):
                raw = jp.parent / "RAW_GENERATED.json"
                if raw.exists():
                    found.append((jp, raw))
        except Exception:
            continue
    if len(found) != 1:
        raise RuntimeError(
            f"Expected exactly 1 exact job for {cid} / {spec['title']}, "
            f"found {len(found)}: {[str(x[0]) for x in found]}"
        )
    return found[0]

def source_text(job_dir, limit=10000):
    chunks = []
    for p in sorted(job_dir.rglob("*")):
        if not p.is_file() or p.name in {"RAW_GENERATED.json","JOB.json","PROMPT.txt"}:
            continue
        if p.suffix.lower() not in {".txt",".md",".json",".csv"}:
            continue
        try:
            s = p.read_text(encoding="utf-8-sig", errors="replace").strip()
        except Exception:
            continue
        if s:
            chunks.append(f"\n--- SOURCE: {p.name} ---\n{s}")
    return "\n".join(chunks)[:limit]

def ask(prompt):
    payload = {
        "model": MODEL, "prompt": prompt, "stream": False,
        "format": "json", "think": False,
        "options": {"temperature": 0.05, "num_ctx": 4096, "num_predict": 300}
    }
    req = Request(OLLAMA_URL,
                  data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                  headers={"Content-Type":"application/json"}, method="POST")
    with urlopen(req, timeout=120) as r:
        outer = json.loads(r.read().decode("utf-8"))
    return json.loads(outer.get("response",""))

def norm(v):
    if isinstance(v, dict):
        for k in ("value","answer","text","question","point"):
            if k in v:
                v = v[k]
                break
    if not isinstance(v, str):
        return ""
    return re.sub(r"\s+", " ", v).strip().strip('"').strip("'").strip()

def valid(v, field):
    if len(v) < (20 if field == "question" else 25):
        return False
    lo = v.lower()
    if any(x in lo for x in BAD) or not re.search(r"[A-Za-z]", v):
        return False
    if field == "question":
        return "?" in v or v.lower().split(" ",1)[0] in {
            "what","who","why","how","which","where","when","name",
            "explain","describe","identify","state","mention","give"
        }
    return len(re.findall(r"[A-Za-z]", v)) >= 5

def items_for(raw, pillar):
    obj = raw.setdefault("pillars", {}).get(pillar)
    if isinstance(obj, list):
        obj = {"items": obj, "gap": None}
        raw["pillars"][pillar] = obj
    if not isinstance(obj, dict):
        raise RuntimeError(f"Invalid/missing {pillar} pillar")
    return obj.setdefault("items", [])

def repair(raw, src, cid, title, pillar, idx, field):
    items = items_for(raw, pillar)
    if idx >= len(items):
        raise RuntimeError(
            f"EXACT JOB HAS ONLY {len(items)} {pillar} items; "
            f"cannot repair {pillar}[{idx}]. Verify bridge/RAW state."
        )
    item = items[idx]
    if isinstance(item.get(field), str) and item[field].strip():
        print(f"      SKIP {pillar}[{idx}].{field}: already populated")
        return 0

    if field == "question":
        task = "Write ONE chapter-specific assessment question answerable directly from the source."
    else:
        task = ("Write ONE natural-language revision point stating an important fact or "
                "concept explicitly supported by the source. Never return a number, ratio, "
                "score, label, metadata, or JSON field name.")

    prompt = f"""Repair exactly one missing educational-content field.

Class 7, Social Science, chapter {cid}: {title}
Field: {pillar}[{idx}].{field}

{task}
Use ONLY the supplied source. Do not invent facts.
Do not mention source, prompts, JSON, validation, or these instructions.
Return ONLY JSON: {{"value":"..."}}

CURRENT ITEM:
{json.dumps(item, ensure_ascii=False, indent=2)[:5000]}

SOURCE:
{src}
"""
    for attempt in range(1,4):
        try:
            v = norm(ask(prompt).get("value",""))
            if valid(v, field):
                item[field] = v
                print(f"      PASS {pillar}[{idx}].{field} attempt {attempt}: {v}")
                return 1
            print(f"      REJECT {pillar}[{idx}].{field} attempt {attempt}: {v!r}")
            prompt += "\nPrevious answer was invalid. Produce a different valid source-grounded answer."
        except Exception as e:
            print(f"      ERROR {pillar}[{idx}].{field} attempt {attempt}: {e}")
        time.sleep(.5)
    raise RuntimeError(f"{pillar}[{idx}].{field} failed after 3 attempts")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    a = ap.parse_args()
    run = Path(a.input_run).resolve()

    print("="*80)
    print("GURUKUL AI — FINAL SURGICAL REPAIR v2")
    print("="*80)
    print(f"Model: {MODEL}")
    print("Promotion: DISABLED")
    print()

    for cid, spec in TARGETS.items():
        jp, rawp = find_exact_job(run, cid, spec)
        raw = load(rawp)
        src = source_text(jp.parent)
        if len(src) < 200:
            raise RuntimeError(f"Insufficient source text for {cid}: {len(src)} chars")

        print(f"[REPAIR] Class 7 | {spec['subject']} | {cid} | {spec['title']}")
        print(f"    JOB : {jp}")
        print(f"    RAW : {rawp}")

        changed = 0
        for pillar, idx, field in spec["fields"]:
            changed += repair(raw, src, cid, spec["title"], pillar, idx, field)

        save(rawp, raw)
        print(f"    Saved. Fields changed: {changed}")
        print()

    print("="*80)
    print("FINAL SURGICAL REPAIR COMPLETE")
    print("Run the canonical bridge next.")
    print("="*80)

if __name__ == "__main__":
    main()

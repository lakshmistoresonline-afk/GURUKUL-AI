
#!/usr/bin/env python3
'''GURUKUL AI — FINAL SURGICAL REPAIR FOR THE 3 CANONICAL FAILURES'''

from __future__ import annotations
import argparse
import importlib.util
import json
import sys
import time
import urllib.request
from pathlib import Path

MODEL = "qwen3.5:2b-q4_K_M"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

TARGETS = [
    ("Class 7", "02_HINDI_GRADE7_COMPLETE", "109", "109_", {"assess": [0,1], "revise": [0]}),
    ("Class 7", "03_SOCIAL_SCIENCE_GRADE7_PART2", "105", "India, a Home to Many", {"assess": [0,1,2,3,4,5], "revise": [0]}),
    ("Class 7", "03_SOCIAL_SCIENCE_GRADE7_PART2", "106", "The State, the Government, and You", {"assess": [0,1,2,3,4,5], "revise": [0]}),
]

BAD = (
    "source section should be used", "source chapter text", "placeholder",
    "sample question", "lorem ipsum", "as an ai", "generation"
)

def readj(p):
    return json.loads(Path(p).read_text(encoding="utf-8-sig"))

def writej(p, x):
    Path(p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def load_validator(root):
    p = root / "backend" / "scripts" / "generate_all_valid_contents.py"
    spec = importlib.util.spec_from_file_location("gurukul_validator_final", p)
    if not spec or not spec.loader:
        raise RuntimeError("Cannot load official validator")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod

def required(schema, pillar):
    if isinstance(schema, dict) and isinstance(schema.get(pillar), dict):
        f = schema[pillar].get("required_fields")
        if isinstance(f, (list, tuple)):
            return list(f)
    def walk(x):
        if isinstance(x, dict):
            if isinstance(x.get(pillar), dict):
                f = x[pillar].get("required_fields")
                if isinstance(f, (list, tuple)):
                    return list(f)
            for v in x.values():
                z = walk(v)
                if z: return z
        elif isinstance(x, list):
            for v in x:
                z = walk(v)
                if z: return z
        return None
    z = walk(schema)
    if z: return z
    raise RuntimeError(f"Cannot find required fields for {pillar}")

def find_job(run_root, cls, subj, cid, title):
    for d in sorted((run_root / "jobs").glob("*")):
        jp, rp = d / "JOB.json", d / "RAW_GENERATED.json"
        if not jp.exists() or not rp.exists():
            continue
        try:
            j = readj(jp)
        except Exception:
            continue
        c = j.get("chapter", {})
        if (c.get("class_name"), c.get("subject_name"), str(c.get("chapter_id")), c.get("chapter_title")) == (cls, subj, cid, title):
            return d, j
    return None, None

def source_text(chapter_path, limit=9000):
    root = Path(chapter_path)
    out, total = [], 0
    if not root.exists():
        return ""
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in {".txt",".md",".json",".csv"}:
            continue
        try:
            t = p.read_text(encoding="utf-8-sig", errors="replace").strip()
        except Exception:
            continue
        if not t:
            continue
        s = f"\n--- {p.name} ---\n{t[:3000]}"
        out.append(s)
        total += len(s)
        if total >= limit:
            break
    return "".join(out)[:limit]

def ollama(prompt, timeout=150):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": 0.05, "num_ctx": 3072, "num_predict": 400}
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type":"application/json; charset=utf-8"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        outer = json.loads(r.read().decode("utf-8", errors="replace"))
    text = outer.get("response", "")
    if not text:
        raise ValueError("empty Ollama response")
    return json.loads(text)

def good(v, field):
    if not isinstance(v, str):
        return False
    v = v.strip()
    if not v or any(x in v.lower() for x in BAD):
        return False
    if field == "question" and (len(v) < 12 or "?" not in v):
        return False
    if field == "point" and len(v) < 12:
        return False
    return True

def repair(field, item, pillar, title, source):
    existing = {k:v for k,v in item.items() if k not in {"chapter_id","source_bundle_sha256"}}
    if field == "question":
        task = "Create exactly one chapter-specific assessment question. If options exist, the question must be answerable using the existing options. Do not change any other field."
    else:
        task = "Create exactly one concise, chapter-specific revision point based on the existing item and source. Do not change any other field."
    prompt = f'''Repair ONE missing field in an existing GURUKUL AI educational record.
Chapter: {title}
Pillar: {pillar}
Missing field: {field}

Existing item:
{json.dumps(existing, ensure_ascii=False, indent=2)}

Relevant source:
{source}

{task}

Return ONLY this JSON shape:
{{"{field}":"..."}}

Do not return other fields. Do not mention AI, generation, source sections, placeholders, or this repair. Stay faithful to the source and existing item.'''
    result = ollama(prompt)
    if not isinstance(result, dict):
        raise ValueError("response is not an object")
    value = result.get(field)
    if not good(value, field):
        raise ValueError(f"invalid {field}: {value!r}")
    return value.strip()

def normalize(raw, pillar):
    p = raw.setdefault("pillars", {}).get(pillar)
    if isinstance(p, list):
        raw["pillars"][pillar] = {"items": p, "gap": None}
        return raw["pillars"][pillar]
    if isinstance(p, dict) and isinstance(p.get("items"), list):
        p.setdefault("gap", None)
        return p
    raise ValueError(f"unsupported {pillar} representation")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    a = ap.parse_args()
    root, run = Path(a.repo_root).resolve(), Path(a.input_run).resolve()

    print("GURUKUL AI — FINAL SURGICAL FIELD REPAIR")
    print(f"Model: {MODEL}")
    print(f"Run: {run}")

    validator = load_validator(root)
    schema = validator.GENERATION_SCHEMA
    assess_req = required(schema, "assess")
    revise_req = required(schema, "revise")
    print("[OK] Official schema loaded")
    print(f"[OK] assess required fields: {assess_req}")
    print(f"[OK] revise required fields: {revise_req}")

    repaired = 0

    for cls, subj, cid, title, targets in TARGETS:
        print(f"\n[TARGET] {cls} | {subj} | {cid} | {title}")
        d, job = find_job(run, cls, subj, cid, title)
        if d is None:
            raise RuntimeError(f"Target not found: {cls} | {subj} | {cid} | {title}")

        raw_path = d / "RAW_GENERATED.json"
        raw = readj(raw_path)
        src = source_text(job["chapter"]["path"])

        for pillar, indexes in targets.items():
            pdata = normalize(raw, pillar)
            items = pdata["items"]
            req = assess_req if pillar == "assess" else revise_req

            for i in indexes:
                if i >= len(items):
                    raise RuntimeError(f"{raw_path}: {pillar}[{i}] missing")

                item = items[i]
                missing = [
                    f for f in req
                    if not isinstance(item.get(f), str) or not item.get(f).strip()
                ]

                allowed = {"question"} if pillar == "assess" else {"point"}
                unexpected = [f for f in missing if f not in allowed]

                if unexpected:
                    raise RuntimeError(
                        f"{raw_path}: {pillar}[{i}] unexpected missing fields {unexpected}"
                    )

                for field in missing:
                    print(f"  {pillar}[{i}]: repairing ONLY {field}")
                    value = None
                    err = None

                    for attempt in range(1, 4):
                        try:
                            print(f"    Ollama attempt {attempt}/3")
                            value = repair(field, item, pillar, title, src)
                            break
                        except Exception as e:
                            err = e
                            print(f"    REJECT: {e}")
                            time.sleep(1)

                    if value is None:
                        raise RuntimeError(
                            f"{raw_path}: {pillar}[{i}].{field} failed: {err}"
                        )

                    item[field] = value
                    repaired += 1

        writej(raw_path, raw)

        check = readj(raw_path)
        for pillar, indexes in targets.items():
            items = normalize(check, pillar)["items"]
            req = assess_req if pillar == "assess" else revise_req

            for i in indexes:
                missing = [
                    f for f in req
                    if not isinstance(items[i].get(f), str)
                    or not items[i].get(f).strip()
                ]
                if missing:
                    raise RuntimeError(
                        f"{raw_path}: {pillar}[{i}] still missing {missing}"
                    )

        print("  PASS: repaired target and locally revalidated")

    print("\n" + "="*80)
    print(f"REPAIR COMPLETE — fields repaired: {repaired}")
    print("Promotion: NOT performed")
    print("Next: canonical bridge validation")
    print("="*80)

if __name__ == "__main__":
    main()

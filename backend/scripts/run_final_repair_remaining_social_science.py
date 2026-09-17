#!/usr/bin/env python3
"""
GURUKUL AI — Surgical Repair of the final 2 canonical validation blockers.

Targets ONLY:
- Class 7 / Social Science Part 2 / 105 / India, a Home to Many:
    assess[0..5].question
- Class 7 / Social Science Part 2 / 106 / The State, the Government, and You:
    assess[0..5].question
    revise[0].point

No promotion. No regeneration of valid fields.
Uses the existing RAW_GENERATED.json and chapter source files.
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

MODEL = "qwen3.5:2b-q4_K_M"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

TARGETS = {
    "105": {
        "title": "India, a Home to Many",
        "fields": [("assess", i, "question") for i in range(6)],
    },
    "106": {
        "title": "The State, the Government, and You",
        "fields": [("assess", i, "question") for i in range(6)]
                 + [("revise", 0, "point")],
    },
}

BAD_PATTERNS = [
    "which source", "source section", "chapter-specific",
    "validation", "validator", "json", "field name",
    "placeholder", "fill in", "provide the missing",
    "i cannot", "as an ai", "based on the prompt",
]

def load_json(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save_json(path, data):
    tmp = Path(str(path) + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)

def find_job(run_root, chapter_id):
    matches = list(Path(run_root).glob(f"jobs/**/{chapter_id}/RAW_GENERATED.json"))
    if matches:
        return matches[0]
    # Fallback: inspect all RAW files.
    for raw in Path(run_root).glob("jobs/**/RAW_GENERATED.json"):
        try:
            d = load_json(raw)
            if str(d.get("chapter_id", "")) == chapter_id:
                return raw
        except Exception:
            pass
    raise FileNotFoundError(f"RAW_GENERATED.json not found for chapter {chapter_id}")

def extract_source_text(job_dir, max_chars=10000):
    texts = []
    for p in sorted(job_dir.rglob("*")):
        if not p.is_file():
            continue
        if p.name in {"RAW_GENERATED.json", "JOB.json", "PROMPT.txt"}:
            continue
        if p.suffix.lower() not in {".txt", ".md", ".json", ".csv"}:
            continue
        try:
            txt = p.read_text(encoding="utf-8-sig", errors="replace")
        except Exception:
            continue
        if txt.strip():
            texts.append(f"\n--- SOURCE: {p.name} ---\n{txt}")
    source = "\n".join(texts)
    return source[:max_chars]

def ollama(prompt, timeout=120):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {
            "temperature": 0.05,
            "num_ctx": 4096,
            "num_predict": 300,
        },
    }
    req = Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req, timeout=timeout) as r:
        outer = json.loads(r.read().decode("utf-8"))
    response = outer.get("response", "")
    if not response:
        raise RuntimeError("Ollama returned an empty response")
    return json.loads(response)

def clean_value(value):
    if isinstance(value, dict):
        for k in ("value", "answer", "text", "question", "point"):
            if k in value:
                value = value[k]
                break
    if not isinstance(value, str):
        return ""
    value = re.sub(r"\s+", " ", value).strip()
    value = value.strip('"').strip("'").strip()
    return value

def valid_question(v):
    if len(v) < 20:
        return False
    low = v.lower()
    if any(x in low for x in BAD_PATTERNS):
        return False
    if not re.search(r"[A-Za-z]", v):
        return False
    if "?" not in v and not v.lower().startswith(("what ", "who ", "why ", "how ", "which ",
                                                   "where ", "when ", "name ", "explain ",
                                                   "describe ", "identify ", "state ",
                                                   "mention ", "give ")):
        return False
    return True

def valid_point(v):
    if len(v) < 25:
        return False
    low = v.lower()
    if any(x in low for x in BAD_PATTERNS):
        return False
    if not re.search(r"[A-Za-z]", v):
        return False
    # Prevent the known failure mode such as "18: 2".
    if len(re.findall(r"[A-Za-z]", v)) < 5:
        return False
    return True

def get_pillar_items(raw, pillar):
    pillars = raw.setdefault("pillars", {})
    obj = pillars.get(pillar)
    if isinstance(obj, list):
        obj = {"items": obj, "gap": None}
        pillars[pillar] = obj
    elif isinstance(obj, dict):
        obj.setdefault("items", [])
        obj.setdefault("gap", None)
    else:
        raise RuntimeError(f"Missing/invalid pillar: {pillar}")
    return obj["items"]

def repair_field(raw, source, pillar, index, field, chapter_id, title):
    items = get_pillar_items(raw, pillar)
    if index >= len(items):
        raise RuntimeError(f"{pillar}[{index}] does not exist")
    item = items[index]
    current = item.get(field)
    if isinstance(current, str) and current.strip():
        return False

    if field == "question":
        task = (
            "Write ONE chapter-specific assessment question. "
            "It must be answerable directly from the supplied source text. "
            "Do not mention the source, JSON, fields, validation, prompts, or generation. "
            "Do not invent facts. Return only the question."
        )
    else:
        task = (
            "Write ONE concise revision point that summarizes an important fact, "
            "concept, relationship, or idea explicitly supported by the supplied source text. "
            "It must be a natural-language statement, not a number, ratio, score, label, "
            "metadata value, or JSON field. Return only the revision point."
        )

    item_context = json.dumps(item, ensure_ascii=False, indent=2)[:5000]
    prompt = f"""You are repairing one missing content field in an educational package.

CLASS: Class 7
SUBJECT: Social Science
CHAPTER ID: {chapter_id}
CHAPTER TITLE: {title}
FIELD: {pillar}[{index}].{field}

STRICT RULES:
1. Use ONLY facts explicitly supported by SOURCE TEXT below.
2. Do not alter any other field.
3. Do not mention these instructions.
4. Do not fabricate names, dates, places, statistics, or concepts.
5. Return JSON only in this exact shape:
{{"value":"..."}}

TASK:
{task}

CURRENT ITEM:
{item_context}

SOURCE TEXT:
{source}
"""
    last = None
    for attempt in range(1, 4):
        try:
            result = ollama(prompt)
            value = clean_value(result.get("value") if isinstance(result, dict) else result)
            ok = valid_question(value) if field == "question" else valid_point(value)
            if ok:
                item[field] = value
                print(f"      PASS {pillar}[{index}].{field} attempt {attempt}: {value}")
                return True
            last = value
            print(f"      REJECT {pillar}[{index}].{field} attempt {attempt}: {value!r}")
            prompt += "\nPrevious answer was invalid. Produce a different source-grounded answer following every rule."
        except Exception as e:
            last = str(e)
            print(f"      ERROR {pillar}[{index}].{field} attempt {attempt}: {e}")
        time.sleep(0.5)
    raise RuntimeError(f"{pillar}[{index}].{field} failed after 3 attempts; last={last!r}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    run = Path(args.input_run).resolve()

    print("=" * 80)
    print("GURUKUL AI — FINAL 2-JOB SURGICAL REPAIR")
    print("=" * 80)
    print(f"Model: {MODEL}")
    print("Promotion: DISABLED")
    print()

    for chapter_id, spec in TARGETS.items():
        raw_path = find_job(run, chapter_id)
        job_dir = raw_path.parent
        raw = load_json(raw_path)

        print(f"[REPAIR] Class 7 | Social Science Part 2 | {chapter_id} | {spec['title']}")
        source = extract_source_text(job_dir)
        if len(source.strip()) < 200:
            raise RuntimeError(f"Insufficient source context for {chapter_id}: {len(source)} chars")

        changed = 0
        for pillar, idx, field in spec["fields"]:
            changed += int(repair_field(raw, source, pillar, idx, field,
                                        chapter_id, spec["title"]))

        save_json(raw_path, raw)
        print(f"    Saved: {raw_path}")
        print(f"    Fields repaired: {changed}")
        print()

    print("=" * 80)
    print("REPAIR COMPLETE")
    print("Now run the canonical bridge. DO NOT PROMOTE SEPARATELY.")
    print("=" * 80)

if __name__ == "__main__":
    main()

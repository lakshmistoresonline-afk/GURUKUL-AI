#!/usr/bin/env python3
"""
GURUKUL AI — Deterministic final canonical repair for Class 7 Social Science Part 2.

Repairs ONLY the exact validator blockers:

105 India, a Home to Many
  assess[0..5].question

106 The State, the Government, and You
  assess[0..5].question
  revise[0].point

No Ollama. No regeneration. No promotion.

The repair preserves all existing fields and only adds the canonical fields
required by the validator.
"""
import argparse
import json
from pathlib import Path

TARGETS = {
    "105": {
        "title": "India, a Home to Many",
        "subject": "03_SOCIAL_SCIENCE_GRADE7_PART2",
        "dirname": "105_INDIA_A_HOME_TO_MANY",
    },
    "106": {
        "title": "The State, the Government, and You",
        "subject": "03_SOCIAL_SCIENCE_GRADE7_PART2",
        "dirname": "106_THE_STATE_THE_GOVERNMENT_AND_YOU",
    },
}

QUESTIONS_105 = [
    "How does India's geographical and cultural diversity contribute to a sense of unity?",
    "How do the values of vasudhaiva kutumbakam, atithi devo bhava, and sarve bhavantu sukhinah promote inclusion and acceptance?",
    "What examples from the Age of Reorganisation show that diverse groups could be absorbed into Indian culture?",
    "Why has India historically served as a sanctuary for people persecuted in their own homelands or seeking new opportunities?",
    "Why are India's foundational values relevant to contemporary global challenges such as climate change, inequality, and discrimination?",
    "Which Parsis mentioned in the chapter are examples of people who excelled academically and professionally in Indian society?",
]

def load(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def save(path, data):
    tmp = Path(str(path) + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(path)

def find_exact_raw(run, cid, spec):
    expected_fragment = (
        f"jobs/Contents__Class 7__{spec['subject']}_COMPLETE__"
        f"{spec['subject']}__{spec['dirname']}/RAW_GENERATED.json"
    )
    matches = list(Path(run).glob(f"jobs/**/{spec['dirname']}/RAW_GENERATED.json"))
    if len(matches) != 1:
        # Exact known generated-job directory fallback.
        matches = [
            p for p in Path(run).glob("jobs/**/RAW_GENERATED.json")
            if spec["dirname"] in str(p)
        ]
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected exactly one RAW for chapter {cid} ({spec['title']}), "
            f"found {len(matches)}: {[str(x) for x in matches]}"
        )
    return matches[0]

def canonical_items(raw, pillar):
    pillars = raw.get("pillars")
    if not isinstance(pillars, dict):
        raise RuntimeError("RAW has no valid pillars object")
    obj = pillars.get(pillar)
    if isinstance(obj, list):
        # Preserve every existing item; only normalize the wrapper.
        obj = {"items": obj, "gap": None}
        pillars[pillar] = obj
    if not isinstance(obj, dict):
        raise RuntimeError(f"{pillar} pillar is missing/invalid")
    items = obj.get("items")
    if not isinstance(items, list):
        raise RuntimeError(f"{pillar}.items is not a list")
    return items

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--input-run", required=True)
    args = ap.parse_args()

    run = Path(args.input_run).resolve()

    print("=" * 80)
    print("GURUKUL AI — DETERMINISTIC FINAL CANONICAL REPAIR")
    print("=" * 80)
    print("Ollama: NOT USED")
    print("Promotion: DISABLED")
    print()

    # ---------------- 105 ----------------
    p105 = find_exact_raw(run, "105", TARGETS["105"])
    d105 = load(p105)
    a105 = canonical_items(d105, "assess")

    if len(a105) < 6:
        raise RuntimeError(f"Chapter 105 has only {len(a105)} assess items; expected 6")

    print("[105] India, a Home to Many")
    for i in range(6):
        item = a105[i]
        old = item.get("question")
        if isinstance(old, str) and old.strip():
            print(f"  assess[{i}].question already exists — preserved")
        else:
            item["question"] = QUESTIONS_105[i]
            print(f"  assess[{i}].question ADDED")
    save(p105, d105)
    print(f"  Saved: {p105}")
    print()

    # ---------------- 106 ----------------
    p106 = find_exact_raw(run, "106", TARGETS["106"])
    d106 = load(p106)
    a106 = canonical_items(d106, "assess")

    if len(a106) < 6:
        raise RuntimeError(f"Chapter 106 has only {len(a106)} assess items; expected 6")

    print("[106] The State, the Government, and You")
    for i in range(6):
        item = a106[i]
        if isinstance(item.get("question"), str) and item["question"].strip():
            print(f"  assess[{i}].question already exists — preserved")
        else:
            qt = item.get("question_text")
            if not isinstance(qt, str) or not qt.strip():
                raise RuntimeError(
                    f"Chapter 106 assess[{i}] has no usable question_text"
                )
            item["question"] = qt.strip()
            print(f"  assess[{i}].question ADDED from existing question_text")

    r106 = canonical_items(d106, "revise")
    if len(r106) < 1:
        raise RuntimeError("Chapter 106 revise has no item 0")

    if isinstance(r106[0].get("point"), str) and r106[0]["point"].strip():
        print("  revise[0].point already exists — preserved")
    else:
        r106[0]["point"] = (
            "The Constitution limits the powers of Parliament and government "
            "through checks and balances, fundamental rights, and the rule of law."
        )
        print("  revise[0].point ADDED")

    save(p106, d106)
    print(f"  Saved: {p106}")
    print()

    print("=" * 80)
    print("REPAIR COMPLETE — 13 CANONICAL FIELDS HAVE BEEN ADDRESSED")
    print("No promotion was performed.")
    print("NEXT: run bridge_v4_to_canonical.py")
    print("=" * 80)

if __name__ == "__main__":
    main()

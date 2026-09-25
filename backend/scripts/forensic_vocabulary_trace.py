import sys
import os
import json

p = r"D:\GURUKUL\Contents\Class 5\English"

notes_raw = json.load(open(os.path.join(p, "santoor_chapters_notes.json"), encoding="utf-8")).get("chapters", [])
vocab_raw = json.load(open(os.path.join(p, "santoor_vocabulary.json"), encoding="utf-8")).get("chapters", [])

print("==========================================================================")
print("FORENSIC TRACE: TERMINOLOGY vs VOCABULARY ACROSS ALL 10 CHAPTERS")
print("==========================================================================\n")

reconciliation_matrix = []

for n_ch in notes_raw:
    u = n_ch["unitNumber"]
    c = n_ch["chapterNumber"]
    title = n_ch["chapterTitle"]

    terms = n_ch.get("keyTerminology", [])
    term_words = {t["term"].strip().lower(): t for t in terms}

    # Find matching vocabulary
    v_ch = next((v for v in vocab_raw if (v.get("chapterNumber") == c or v.get("chapter") == c)), None)
    vocab_items = v_ch.get("vocabulary", []) if v_ch else []
    vocab_words = {v["term"].strip().lower(): v for v in vocab_items}

    exact_duplicates = set(term_words.keys()).intersection(set(vocab_words.keys()))
    term_only = set(term_words.keys()) - set(vocab_words.keys())
    vocab_only = set(vocab_words.keys()) - set(term_words.keys())

    reconciliation_matrix.append({
        "chapterNumber": c,
        "title": title,
        "terms_count": len(terms),
        "vocab_count": len(vocab_items),
        "exact_duplicates": list(exact_duplicates),
        "term_only": list(term_only),
        "vocab_only": list(vocab_only),
    })

    print(f"Chapter {c}: {title}")
    print(f"  Key Terminology Count: {len(terms)} | Deep Vocabulary Count: {len(vocab_items)}")
    print(f"  Exact Overlapping Terms ({len(exact_duplicates)}): {sorted(list(exact_duplicates))}")
    print(f"  Vocabulary Only Terms ({len(vocab_only)}): {sorted(list(vocab_only))}")
    print("-" * 74)

if __name__ == "__main__":
    pass

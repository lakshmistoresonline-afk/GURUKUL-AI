import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def test_enrichment():
    p = r"D:\GURUKUL\Contents\Class 5\English"
    notes_raw = json.load(open(os.path.join(p, "santoor_chapters_notes.json"), encoding="utf-8")).get("chapters", [])

    print("=== TESTING UNIFIED TERMINOLOGY & DEEP VOCABULARY ENRICHMENT ACROSS 10 CHAPTERS ===")

    for n in notes_raw:
        u = n["unitNumber"]
        c = n["chapterNumber"]
        ch_id = f"G5-ENG-U{u:02d}-C{c:02d}"

        data = ContentLoaderService.load_chapter_source("5", "English", ch_id)

        terms = data.get("keyTerminology", [])
        vocab = data.get("vocabulary", [])

        # Build enriched term list
        merged_terms = []
        vocab_by_term = {v["term"].strip().lower(): v for v in vocab if isinstance(v, dict) and "term" in v}

        seen_terms = set()
        for t in terms:
            t_name = t["term"].strip()
            fp = t_name.lower()
            seen_terms.add(fp)

            enrichment = vocab_by_term.get(fp, {})
            merged_terms.append({
                "term": t_name,
                "definition": t.get("definition") or enrichment.get("definition"),
                "contextSentence": enrichment.get("contextSentence"),
                "synonyms": enrichment.get("synonyms"),
                "antonyms": enrichment.get("antonyms"),
                "isEnriched": fp in vocab_by_term
            })

        # Add distinct vocab terms not in keyTerminology
        distinct_added = 0
        for v in vocab:
            if isinstance(v, dict) and "term" in v:
                v_name = v["term"].strip()
                fp = v_name.lower()
                if fp not in seen_terms:
                    seen_terms.add(fp)
                    merged_terms.append({
                        "term": v_name,
                        "definition": v.get("definition"),
                        "contextSentence": v.get("contextSentence"),
                        "synonyms": v.get("synonyms"),
                        "antonyms": v.get("antonyms"),
                        "isEnriched": True
                    })
                    distinct_added += 1

        print(f"Chapter {c}: {n['chapterTitle']}")
        print(f"  Notes Terms: {len(terms)} | Deep Vocab Terms: {len(vocab)}")
        print(f"  Enriched Unified Terms Count: {len(merged_terms)} ({distinct_added} distinct vocab terms appended)")
        print("-" * 74)

if __name__ == "__main__":
    test_enrichment()

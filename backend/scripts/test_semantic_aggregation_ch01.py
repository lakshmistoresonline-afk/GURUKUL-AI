import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def test_aggregation():
    data = ContentLoaderService.load_chapter_source("5", "English", "G5-ENG-U01-C01")

    sq = data.get("studyQuestions", {})
    tb = data.get("master_testbank", {})
    mqb = data.get("model_question_bank", {})
    fib = data.get("fill_in_the_blanks", {})

    # 1. MCQs
    mcqs = []
    seen_q = set()

    # From studyQuestions
    for q in sq.get("multipleChoiceQuestions", []):
        fp = q["question"].strip().lower()
        if fp not in seen_q:
            seen_q.add(fp)
            mcqs.append({"source": "santoor_chapters_notes.json", "data": q})

    # From master_testbank
    for q in tb.get("multipleChoiceQuestions", []):
        fp = q["question"].strip().lower()
        if fp not in seen_q:
            seen_q.add(fp)
            mcqs.append({"source": "santoor_master_testbank.json", "data": q})

    # From model_question_bank partA
    for q in mqb.get("partA", []):
        if isinstance(q, dict) and "question" in q:
            fp = q["question"].strip().lower()
            if fp not in seen_q:
                seen_q.add(fp)
                mcqs.append({"source": "santoor_model_question_bank.json", "data": q})

    # 2. Short Answer
    saqs = []
    seen_sa = set()
    for q in sq.get("shortAnswerQuestions", []):
        fp = q["question"].strip().lower()
        if fp not in seen_sa:
            seen_sa.add(fp)
            saqs.append({"source": "santoor_chapters_notes.json", "data": q})

    for q in tb.get("shortAnswerQuestions", []):
        fp = q["question"].strip().lower()
        if fp not in seen_sa:
            seen_sa.add(fp)
            saqs.append({"source": "santoor_master_testbank.json", "data": q})

    for q in mqb.get("partB", []):
        if isinstance(q, dict) and "question" in q:
            fp = q["question"].strip().lower()
            if fp not in seen_sa:
                seen_sa.add(fp)
                saqs.append({"source": "santoor_model_question_bank.json", "data": q})

    # 3. Reflections
    rfqs = []
    seen_rf = set()
    for q in sq.get("reflectionQuestions", []):
        fp = q["question"].strip().lower()
        if fp not in seen_rf:
            seen_rf.add(fp)
            rfqs.append({"source": "santoor_chapters_notes.json", "data": q})

    for q in tb.get("reflectionQuestions", []):
        fp = q["question"].strip().lower()
        if fp not in seen_rf:
            seen_rf.add(fp)
            rfqs.append({"source": "santoor_master_testbank.json", "data": q})

    print("=== CHAPTER 1 SEMANTIC PRACTICE AGGREGATION RESULTS ===")
    print(f"Aggregated MCQs Count: {len(mcqs)} (Numbered 1 to {len(mcqs)})")
    for i, m in enumerate(mcqs, 1):
        print(f"  {i}. [{m['source']}] {m['data']['question']}")

    print(f"\nAggregated Short Answer Count: {len(saqs)} (Numbered 1 to {len(saqs)})")
    for i, s in enumerate(saqs, 1):
        print(f"  {i}. [{s['source']}] {s['data']['question']}")

    print(f"\nAggregated Reflections Count: {len(rfqs)} (Numbered 1 to {len(rfqs)})")
    for i, r in enumerate(rfqs, 1):
        print(f"  {i}. [{r['source']}] {r['data']['question']}")

if __name__ == "__main__":
    test_aggregation()

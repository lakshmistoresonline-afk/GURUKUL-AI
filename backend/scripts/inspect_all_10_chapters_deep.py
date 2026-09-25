import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def inspect_all_chapters():
    p = 'D:/GURUKUL/Contents/Class 5/English'
    notes_raw = json.load(open(os.path.join(p, 'santoor_chapters_notes.json'), encoding='utf-8'))
    chapters = notes_raw.get('chapters', [])

    print("=== INSPECTING ALL 10 CHAPTERS FOR FIELD VARIATIONS ===")

    for c in chapters:
        ch_id = f"G5-ENG-U{c['unitNumber']:02d}-C{c['chapterNumber']:02d}"
        print(f"\n--- {ch_id}: {c['chapterTitle']} ---")

        # Overview
        ov = c.get('overview', {})
        print("Overview keys:", list(ov.keys()))

        # Terminology
        terms = c.get('keyTerminology', [])
        term_keys = set()
        for t in terms:
            term_keys.update(t.keys())
        print(f"KeyTerminology count: {len(terms)} | Item keys: {sorted(list(term_keys))}")

        # Detailed Breakdown
        bd = c.get('detailedBreakdown', [])
        bd_keys = set()
        for b in bd:
            bd_keys.update(b.keys())
            # Check structure of details
            d = b.get('details')
            if isinstance(d, list):
                print(f"  Section '{b.get('sectionTitle')}': details list length = {len(d)}")
            else:
                print(f"  Section '{b.get('sectionTitle')}': details type = {type(d).__name__}")
        print(f"DetailedBreakdown sections: {len(bd)} | Item keys: {sorted(list(bd_keys))}")

        # Takeaways
        tk = c.get('importantTakeaways', [])
        print(f"ImportantTakeaways items: {len(tk)}")

        # Study Questions
        sq = c.get('studyQuestions', {})
        mcq = sq.get('multipleChoiceQuestions', [])
        sa = sq.get('shortAnswerQuestions', [])
        rf = sq.get('reflectionQuestions', [])
        print(f"StudyQuestions -> MCQ: {len(mcq)}, ShortAnswer: {len(sa)}, Reflection: {len(rf)}")
        if mcq:
            mcq_keys = set()
            for m in mcq: mcq_keys.update(m.keys())
            print(f"  MCQ Item keys: {sorted(list(mcq_keys))}")
            # Check options structure
            for m in mcq:
                opts = m.get('options', [])
                ans = m.get('answer') or m.get('correctAnswer')
                print(f"    MCQ Options count: {len(opts)} | Answer: {ans}")
        if sa:
            sa_keys = set()
            for s in sa: sa_keys.update(s.keys())
            print(f"  ShortAnswer Item keys: {sorted(list(sa_keys))}")
            for s in sa:
                print(f"    ShortAnswer Q: {s.get('question')} | Answer: {s.get('answer')}")

if __name__ == "__main__":
    inspect_all_chapters()

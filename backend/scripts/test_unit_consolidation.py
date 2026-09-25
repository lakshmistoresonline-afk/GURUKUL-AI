import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def test_consolidation():
    for sub in ["English", "Hindi", "Maths", "Science"]:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])
        print(f"SUBJECT: {sub} -> {len(units)} Consolidated Units:")
        for u in units:
            chs = u.get("chapters", [])
            print(f"  Unit {u.get('unitNumber')} ({u.get('id')}) - '{u.get('title')}': {len(chs)} chapters -> {[c.get('chapterNumber') for c in chs]}")
        print("-" * 60)

if __name__ == "__main__":
    test_consolidation()

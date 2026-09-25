import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

for sub in ["English", "Hindi", "Maths", "Science"]:
    meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
    units = meta.get("units", [])
    print(f"=== SUBJECT: {sub} ===")
    print(f"  Curriculum Framework: {meta.get('curriculumFramework')}")
    print(f"  Curricular Goals Count: {len(meta.get('curricularGoals', []))}")
    print(f"  Units Count: {len(units)}")
    for u in units:
        print(f"    Unit ID: '{u.get('id')}', Number: {u.get('unitNumber')}, Title: '{u.get('title')}', Chapters Count: {len(u.get('chapters', []))}")
        for c in u.get("chapters", [])[:2]:
            print(f"      - Ch ID: '{c.get('id')}', ChNum: {c.get('chapterNumber')}, Title: '{c.get('title')}'")
    print("-" * 60)

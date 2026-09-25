import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def trace_route():
    for sub in ["English", "Hindi", "Maths", "Science"]:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        units = meta.get("units", [])
        total_ch = sum(len(u.get("chapters", [])) for u in units)
        print(f"Subject '{sub}': framework='{meta.get('curriculumFramework')}', goals={len(meta.get('curricularGoals', []))}, units={len(units)}, total_chapters={total_ch}")
        if not units or total_ch == 0:
            print(f"  WARNING: 0 chapters returned for {sub}!")

if __name__ == "__main__":
    trace_route()

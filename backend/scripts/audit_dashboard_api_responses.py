import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

def audit_api_responses():
    subjects = ["English", "Hindi", "Maths", "Science"]
    print("==========================================================================")
    print("FORENSIC AUDIT OF SUBJECT DASHBOARD API RESPONSES (CLASS 5)")
    print("==========================================================================\n")

    for sub in subjects:
        meta = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
        print(f"SUBJECT: Class 5 {sub}")
        print(f"  Framework: {meta.get('curriculumFramework')}")
        print(f"  Curricular Goals Count: {len(meta.get('curricularGoals', []))}")
        print(f"  Curricular Goals List: {meta.get('curricularGoals')}")

        units = meta.get("units", [])
        print(f"  Units Count: {len(units)}")
        for u in units:
            chs = u.get("chapters", [])
            print(f"    Unit {u.get('unitNumber')} ({u.get('title')}): {len(chs)} chapters")
            for ch in chs:
                print(f"      - Chapter {ch.get('chapterNumber')}: {ch.get('title')} | resources: {ch.get('resourceCount')} | types: {ch.get('contentTypes')}")
        print("-" * 74)

if __name__ == "__main__":
    audit_api_responses()

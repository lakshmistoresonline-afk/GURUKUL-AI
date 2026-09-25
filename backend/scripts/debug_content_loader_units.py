import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.content_loader import ContentLoaderService

meta = ContentLoaderService.get_subject_curriculum_metadata("5", "English")
print("Meta Framework:", meta.get("curriculumFramework"))
print("Meta Goals:", len(meta.get("curricularGoals", [])))
print("Meta Units:", len(meta.get("units", [])))

for sub in ["English", "Hindi", "Maths", "Science"]:
    m = ContentLoaderService.get_subject_curriculum_metadata("5", sub)
    u = m.get("units", [])
    ch_count = sum(len(x.get("chapters", [])) for x in u)
    print(f"Subject {sub:<8}: {len(u)} Units | {ch_count} Chapters")

import os

backend_src = r"D:\GURUKUL\backend\src"
subjects_dir = os.path.join(backend_src, "subjects")

for sub in ["hindi", "english", "maths", "science"]:
    sub_path = os.path.join(subjects_dir, sub)
    for p in ["processors", "models", "presentation", "renderers"]:
        os.makedirs(os.path.join(sub_path, p), exist_ok=True)

# Create registry template for Hindi
hindi_registry_py = '''from typing import Dict, Any, List
from ...core.models import ContentBlock
from ..processors.hindi_processor import HindiProcessor

class HindiEngineRegistry:
    @staticmethod
    def process_chapter(source_data: Dict[str, Any], chapter_id: str, dataset: str = "NCERT") -> List[ContentBlock]:
        processor = HindiProcessor()
        return processor.process_chapter(source_data, chapter_id, dataset)
'''

os.makedirs(os.path.join(subjects_dir, "hindi"), exist_ok=True)
with open(os.path.join(subjects_dir, "hindi", "registry.py"), "w", encoding="utf-8") as f:
    f.write(hindi_registry_py)

print("SUBJECT ENGINES DIRECTORY STRUCTURE CREATED SUCCESSFULLY!")

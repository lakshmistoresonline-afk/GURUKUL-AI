import os
from pathlib import Path

CLASSES = {
    "class5": ["english", "hindi", "mathematics", "science"],
    "class6": ["english", "hindi", "mathematics", "science", "social_science"],
    "class7": ["english", "hindi", "mathematics", "science", "social_science"]
}

BASE_DIR = Path(r"D:/GURUKUL/backend/src/curriculum/classes")

TEMPLATE_EXTRACTOR = """from typing import Dict, Any
class Class{grade}{Subject}Extractor:
    @classmethod
    def extract(cls, source_path: str) -> Dict[str, Any]:
        with open(source_path, "r", encoding="utf-8") as f:
            import json
            return json.load(f)
"""

TEMPLATE_NORMALIZER = """from typing import Dict, Any
class Class{grade}{Subject}Normalizer:
    @classmethod
    def normalize(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return data
"""

TEMPLATE_VALIDATOR = """from typing import Dict, Any
class Class{grade}{Subject}Validator:
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        return isinstance(data, (dict, list))
"""

TEMPLATE_MAPPER = """from typing import Dict, Any
class Class{grade}{Subject}Mapper:
    @classmethod
    def map_to_dto(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        return data
"""

TEMPLATE_PROCESSOR = """from typing import Dict, Any
class Class{grade}{Subject}Processor:
    @classmethod
    def process(cls, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
"""

def scaffold():
    for grade_key, subjects in CLASSES.items():
        grade_num = grade_key.replace("class", "")
        for subj in subjects:
            subj_dir = BASE_DIR / grade_key / subj
            subj_dir.mkdir(parents=True, exist_ok=True)

            subj_title = subj.replace("_", "").capitalize()

            files = {
                "extractor.py": TEMPLATE_EXTRACTOR.format(grade=grade_num, Subject=subj_title),
                "normalizer.py": TEMPLATE_NORMALIZER.format(grade=grade_num, Subject=subj_title),
                "validator.py": TEMPLATE_VALIDATOR.format(grade=grade_num, Subject=subj_title),
                "mapper.py": TEMPLATE_MAPPER.format(grade=grade_num, Subject=subj_title),
                "processor.py": TEMPLATE_PROCESSOR.format(grade=grade_num, Subject=subj_title)
            }

            for fname, content in files.items():
                f_path = subj_dir / fname
                if not f_path.exists():
                    with open(f_path, "w", encoding="utf-8") as f:
                        f.write(content)

    print("Modular class/subject processors scaffolded successfully.")

if __name__ == "__main__":
    scaffold()

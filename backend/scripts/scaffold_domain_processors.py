import os
import json
from pathlib import Path

CLASSES_SUBJECTS = {
    "class5": ["english", "hindi", "mathematics", "science"],
    "class6": ["english", "hindi", "mathematics", "science", "social_science"],
    "class7": ["english", "hindi", "mathematics_i", "mathematics_ii", "science", "social_science_i", "social_science_ii"]
}

DOMAINS = [
    "overview",
    "notes",
    "master",
    "foundational",
    "flashcards",
    "mindmaps",
    "quiz",
    "question_papers"
]

BASE_DIR = Path(r"D:/GURUKUL/backend/src/curriculum/domains")

TEMPLATE_EXTRACTOR = """import json
from pathlib import Path
class {Class}{Subject}{Domain}Extractor:
    @classmethod
    def extract(cls, source_path: Path) -> dict:
        if not source_path.exists():
            return {{}}
        with open(source_path, "r", encoding="utf-8") as f:
            return json.load(f)
"""

TEMPLATE_NORMALIZER = """class {Class}{Subject}{Domain}Normalizer:
    @classmethod
    def normalize(cls, raw_data: dict) -> dict:
        return raw_data
"""

TEMPLATE_VALIDATOR = """class {Class}{Subject}{Domain}Validator:
    @classmethod
    def validate(cls, data: dict) -> bool:
        return data is not None
"""

TEMPLATE_MAPPER = """class {Class}{Subject}{Domain}Mapper:
    @classmethod
    def map_to_runtime(cls, data: dict) -> dict:
        return data
"""

TEMPLATE_PROCESSOR = """from .extractor import {Class}{Subject}{Domain}Extractor
from .normalizer import {Class}{Subject}{Domain}Normalizer
from .validator import {Class}{Subject}{Domain}Validator
from .mapper import {Class}{Subject}{Domain}Mapper

class {Class}{Subject}{Domain}Processor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = {Class}{Subject}{Domain}Extractor.extract(source_path)
        if not {Class}{Subject}{Domain}Validator.validate(raw):
            raise ValueError("Validation failed for {Domain}")
        normalized = {Class}{Subject}{Domain}Normalizer.normalize(raw)
        return {Class}{Subject}{Domain}Mapper.map_to_runtime(normalized)
"""

def scaffold_domains():
    for grade_key, subjects in CLASSES_SUBJECTS.items():
        grade_num = grade_key.replace("class", "")
        for subj in subjects:
            for domain in DOMAINS:
                domain_dir = BASE_DIR / grade_key / subj / domain
                domain_dir.mkdir(parents=True, exist_ok=True)

                class_str = f"Class{grade_num}"
                subj_str = subj.replace("_", "").capitalize()
                domain_str = domain.replace("_", "").capitalize()

                files = {
                    "extractor.py": TEMPLATE_EXTRACTOR.format(Class=class_str, Subject=subj_str, Domain=domain_str),
                    "normalizer.py": TEMPLATE_NORMALIZER.format(Class=class_str, Subject=subj_str, Domain=domain_str),
                    "validator.py": TEMPLATE_VALIDATOR.format(Class=class_str, Subject=subj_str, Domain=domain_str),
                    "mapper.py": TEMPLATE_MAPPER.format(Class=class_str, Subject=subj_str, Domain=domain_str),
                    "processor.py": TEMPLATE_PROCESSOR.format(Class=class_str, Subject=subj_str, Domain=domain_str)
                }

                for fname, content in files.items():
                    f_path = domain_dir / fname
                    if not f_path.exists():
                        with open(f_path, "w", encoding="utf-8") as f:
                            f.write(content)

    print("Successfully scaffolded fine-grained domain processors for all classes, subjects, and source datasets.")

if __name__ == "__main__":
    scaffold_domains()

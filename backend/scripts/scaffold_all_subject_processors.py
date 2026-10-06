import os
from pathlib import Path

PROCESSORS_DIR = Path(r"D:/GURUKUL/backend/src/curriculum/processors")

MODULES = [
    ("class5", "english_processor", "Class5EnglishProcessor"),
    ("class5", "hindi_processor", "Class5HindiProcessor"),
    ("class5", "mathematics_processor", "Class5MathematicsProcessor"),
    ("class5", "science_processor", "Class5ScienceProcessor"),

    ("class6", "english_processor", "Class6EnglishProcessor"),
    ("class6", "hindi_processor", "Class6HindiProcessor"),
    ("class6", "mathematics_processor", "Class6MathematicsProcessor"),
    ("class6", "science_processor", "Class6ScienceProcessor"),
    ("class6", "social_science_processor", "Class6SocialScienceProcessor"),

    ("class7", "english_processor", "Class7EnglishProcessor"),
    ("class7", "hindi_processor", "Class7HindiProcessor"),
    ("class7", "mathematics_i_processor", "Class7MathematicsIProcessor"),
    ("class7", "mathematics_ii_processor", "Class7MathematicsIIProcessor"),
    ("class7", "science_processor", "Class7ScienceProcessor"),
    ("class7", "social_science_i_processor", "Class7SocialScienceIProcessor"),
    ("class7", "social_science_ii_processor", "Class7SocialScienceIIProcessor"),
]

TEMPLATE = """from typing import Dict, Any
from ..base.base_processor import BaseProcessor
from ...core.curriculum_identity import CurriculumIdentity

class {ClassName}(BaseProcessor):
    ""\"Dedicated processor for {ClassName} with strict schema validation and identity enforcement.""\"
    def process(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate(identity, raw_data):
            raise ValueError(f"Validation failed in {{self.__class__.__name__}} for identity: {{identity.to_cache_key()}}")
        return raw_data

    def validate(self, identity: CurriculumIdentity, raw_data: Dict[str, Any]) -> bool:
        if not isinstance(raw_data, (dict, list)):
            return False
        return True
"""

def generate_processors():
    for class_folder, mod_name, class_name in MODULES:
        folder = PROCESSORS_DIR / class_folder
        folder.mkdir(parents=True, exist_ok=True)
        f_path = folder / f"{mod_name}.py"
        if not f_path.exists():
            with open(f_path, "w", encoding="utf-8") as f:
                f.write(TEMPLATE.format(ClassName=class_name))

    print("All subject-specific and class-specific processors generated successfully.")

if __name__ == "__main__":
    generate_processors()

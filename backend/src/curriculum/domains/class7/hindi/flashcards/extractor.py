import json
from pathlib import Path
class Class7HindiFlashcardsExtractor:
    @classmethod
    def extract(cls, source_path: Path) -> dict:
        if not source_path.exists():
            return {}
        with open(source_path, "r", encoding="utf-8") as f:
            return json.load(f)

from typing import Dict, Any
class Class5ScienceExtractor:
    @classmethod
    def extract(cls, source_path: str) -> Dict[str, Any]:
        with open(source_path, "r", encoding="utf-8") as f:
            import json
            return json.load(f)

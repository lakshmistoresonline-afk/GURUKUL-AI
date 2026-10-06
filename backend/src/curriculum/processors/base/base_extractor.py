import json
from pathlib import Path
from typing import Dict, Any

class BaseExtractor:
    """Lossless source extractor for authoritative curriculum datasets."""
    @classmethod
    def extract(cls, source_path: Path) -> Dict[str, Any]:
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        with open(source_path, "r", encoding="utf-8") as f:
            return json.load(f)

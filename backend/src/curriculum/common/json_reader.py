import os
import json
from typing import Dict, Any, Optional

class JsonReader:
    @staticmethod
    def read_json_file(file_path: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to parse JSON file {file_path}: {e}")

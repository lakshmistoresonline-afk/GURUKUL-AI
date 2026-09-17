import json
from pathlib import Path
from typing import Any

def read_json_utf8(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))

def write_json_utf8(path: Path, data: Any, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent), encoding="utf-8")

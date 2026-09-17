import os
from pathlib import Path

def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path

def list_files_by_extension(path: Path, ext: str) -> list[Path]:
    if not path.exists():
        return []
    return sorted(list(path.rglob(f"*.{ext.lstrip('.')}")))

import json
from pathlib import Path
from typing import Any
from .profile import SourceProfile
from ..json_utils import read_json_utf8

class SourceProfileLoader:
    @staticmethod
    def from_dict(data: dict[str, Any]) -> SourceProfile:
        return SourceProfile(
            class_level=data.get("class_level"),
            subject=data.get("subject"),
            book=data.get("book"),
            source_package=data.get("source_package"),
            source_files=data.get("source_files", []),
            language=data.get("language", "English"),
            part=data.get("part", ""),
            section_mapping=data.get("section_mapping", {}),
            rules=data.get("rules", {})
        )

    @classmethod
    def from_file(cls, path: Path) -> SourceProfile:
        if not path.exists():
            raise FileNotFoundError(f"SourceProfile file not found: {path}")
        data = read_json_utf8(path)
        return cls.from_dict(data)

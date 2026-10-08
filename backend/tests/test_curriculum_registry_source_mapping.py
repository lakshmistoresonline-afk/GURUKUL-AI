import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.core.curriculum_registry import CurriculumRegistry, IdentityConflictError, SourceMismatchError, ManifestMalformedError

def test_registry_stale_source_hash(tmp_path, monkeypatch):
    ch_dir = tmp_path / "ProcessedContent" / "Class5" / "English" / "G5-ENG-U01-C99"
    ch_dir.mkdir(parents=True)

    # Create a dummy source file
    contents_root = tmp_path / "Contents"
    content_dir = contents_root / "Class 5" / "English"
    content_dir.mkdir(parents=True)
    src_file = content_dir / "Master.json"
    src_file.write_text("{}", encoding="utf-8")

    manifest_file = ch_dir / "manifest.json"
    manifest_data = {
        "grade": "5",
        "subject": "english",
        "book": "english",
        "part": "main",
        "unit": "U01",
        "chapter_id": "G5-ENG-U01-C99",
        "chapter_number": 1,
        "chapter_title": "Test Chapter",
        "unit_number": 1,
        "unit_title": "Unit 1",
        "source_files": ["Class 5/English/Master.json"],
        "source_json_paths": ["Class 5/English/Master.json"],
        "source_hashes": {"Class 5/English/Master.json": "stale_hash_value"},
        "source_identity": {
            "grade": "5",
            "canonical_subject": "english",
            "book": "english",
            "part": "main",
            "unit": "U01",
            "chapter_id": "G5-ENG-U01-C99"
        }
    }
    manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")

    monkeypatch.setattr("src.curriculum.core.curriculum_registry.PROCESSED_ROOT", tmp_path / "ProcessedContent")
    monkeypatch.setattr("src.curriculum.core.curriculum_registry.CONTENTS_ROOT", contents_root)
    CurriculumRegistry._INDEX = None

    with pytest.raises(SourceMismatchError):
        CurriculumRegistry.get_index()

    CurriculumRegistry._INDEX = None # reset cache

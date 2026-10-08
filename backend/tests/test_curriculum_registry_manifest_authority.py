import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, IdentityConflictError, ManifestMalformedError

def test_manifest_authority_missing_field(tmp_path, monkeypatch):
    ch_dir = tmp_path / "Class5" / "English" / "G5-ENG-U01-C99"
    ch_dir.mkdir(parents=True)
    # Manifest missing required fields
    manifest_file = ch_dir / "manifest.json"
    manifest_file.write_text(json.dumps({"grade": "5", "subject": "english"}), encoding="utf-8")

    monkeypatch.setattr("src.curriculum.core.curriculum_registry.PROCESSED_ROOT", tmp_path)
    CurriculumRegistry._INDEX = None

    with pytest.raises(ManifestMalformedError):
        CurriculumRegistry.get_index()

    CurriculumRegistry._INDEX = None # reset cache

def test_manifest_authority_identity_conflict(tmp_path, monkeypatch):
    ch_dir = tmp_path / "Class5" / "English" / "G5-ENG-U01-C99"
    ch_dir.mkdir(parents=True)
    # Manifest grade conflicts with directory grade
    manifest_file = ch_dir / "manifest.json"
    manifest_data = {
        "grade": "7",
        "subject": "english",
        "book": "english",
        "part": "main",
        "unit": "U01",
        "chapter_id": "G5-ENG-U01-C99",
        "chapter_number": 1,
        "chapter_title": "Conflict Chapter",
        "unit_number": 1,
        "unit_title": "Unit 1",
        "source_files": [],
        "source_json_paths": [],
        "source_hashes": {},
        "source_identity": {
            "grade": "7",
            "canonical_subject": "english",
            "book": "english",
            "part": "main",
            "unit": "U01",
            "chapter_id": "G5-ENG-U01-C99"
        }
    }
    manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")

    monkeypatch.setattr("src.curriculum.core.curriculum_registry.PROCESSED_ROOT", tmp_path)
    CurriculumRegistry._INDEX = None

    with pytest.raises(IdentityConflictError):
        CurriculumRegistry.get_index()

    CurriculumRegistry._INDEX = None # reset cache

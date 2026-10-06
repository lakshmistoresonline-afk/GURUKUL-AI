import os
import sys
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.strict_content_validator import StrictContentValidator, ManifestMissingError, ManifestMalformedError, IdentityConflictError, ContentSchemaInvalidError

def test_strict_validator_valid_manifest(tmp_path):
    ch_dir = tmp_path / "chapter_test"
    ch_dir.mkdir()
    manifest_data = {
        "grade": "5",
        "subject": "english",
        "book": "main",
        "part": "none",
        "unit": "U01",
        "chapter_id": "G5-ENG-U01-C01",
        "chapter_number": 1,
        "chapter_title": "Test Chapter",
        "unit_number": 1,
        "unit_title": "Test Unit"
    }
    (ch_dir / "manifest.json").write_text(json_str := str(manifest_data).replace("'", '"'), encoding="utf-8")

    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )

    model = StrictContentValidator.validate_manifest(ch_dir, identity)
    assert model.grade == "5"
    assert model.chapter_id == "G5-ENG-U01-C01"

def test_strict_validator_missing_manifest(tmp_path):
    ch_dir = tmp_path / "empty_chapter"
    ch_dir.mkdir()
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ManifestMissingError):
        StrictContentValidator.validate_manifest(ch_dir, identity)

def test_strict_validator_malformed_manifest(tmp_path):
    ch_dir = tmp_path / "bad_manifest"
    ch_dir.mkdir()
    (ch_dir / "manifest.json").write_text("{ malformed json ", encoding="utf-8")
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ManifestMalformedError):
        StrictContentValidator.validate_manifest(ch_dir, identity)

def test_strict_validator_identity_conflict(tmp_path):
    ch_dir = tmp_path / "conflict_manifest"
    ch_dir.mkdir()
    manifest_data = {
        "grade": "6", # Mismatch! Requested is 5
        "subject": "english",
        "book": "main",
        "part": "none",
        "unit": "U01",
        "chapter_id": "G5-ENG-U01-C01",
        "chapter_number": 1,
        "chapter_title": "Test Chapter",
        "unit_number": 1,
        "unit_title": "Test Unit"
    }
    import json
    (ch_dir / "manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")

    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(IdentityConflictError):
        StrictContentValidator.validate_manifest(ch_dir, identity)

def test_strict_validator_malformed_content_json(tmp_path):
    bad_file = tmp_path / "overview.json"
    bad_file.write_text("NOT VALID JSON", encoding="utf-8")
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ContentSchemaInvalidError):
        StrictContentValidator.validate_content_file(bad_file, identity)

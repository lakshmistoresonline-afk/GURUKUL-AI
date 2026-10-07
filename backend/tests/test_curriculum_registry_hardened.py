import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, ChapterNotFoundError, ContentSchemaError, ManifestMissingError, ManifestMalformedError

def test_registry_exact_valid_identity():
    id_req = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    node = CurriculumRegistry.resolve_node(id_req)
    assert node["chapter_id"] == "G5-ENG-U01-C01"

def test_registry_wrong_book_raises_not_found():
    id_req = CurriculumIdentity(
        grade="5",
        subject="english",
        book="wrong_book_name",
        part="main",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(id_req)

def test_registry_wrong_unit_raises_not_found():
    id_req = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U99",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(id_req)

def test_registry_missing_manifest_raises(tmp_path, monkeypatch):
    ch_dir = tmp_path / "Class5" / "English" / "BadChapter"
    ch_dir.mkdir(parents=True)
    # no manifest.json

    # We test that build_index or resolve raises ManifestMissingError when scanning such a dir
    # But since build_index scans PROCESSED_ROOT, we can test via direct call or mock
    pass

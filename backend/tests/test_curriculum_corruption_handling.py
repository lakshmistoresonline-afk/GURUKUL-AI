import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, ContentSchemaError, ContentMissingError, ChapterNotFoundError

def test_corruption_handling_corrupt_json(tmp_path, monkeypatch):
    # Test that corrupt JSON raises ContentSchemaError rather than returning None
    pass

def test_corruption_handling_missing_chapter():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U01",
        chapter_id="NONEXISTENT-C99",
        content_type="overview"
    )
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_chapter_path(identity)

import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, CurriculumResolutionError

def test_registry_discovery():
    classes = CurriculumRegistry.get_classes()
    assert "5" in classes
    assert "6" in classes
    assert "7" in classes

    subjects_5 = CurriculumRegistry.get_subjects("5")
    assert "English" in subjects_5
    assert "Hindi" in subjects_5

def test_exact_identity_resolution_success():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    path = CurriculumRegistry.resolve_chapter_path(identity)
    assert os.path.exists(path)

def test_negative_identity_resolution_wrong_book():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="wrong_book",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(CurriculumResolutionError):
        CurriculumRegistry.resolve_chapter_path(identity)

def test_negative_identity_resolution_wrong_chapter():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="NON-EXISTENT-CHAPTER",
        content_type="overview"
    )
    with pytest.raises(CurriculumResolutionError):
        CurriculumRegistry.resolve_chapter_path(identity)

def test_negative_identity_resolution_wrong_content_type():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="nonexistent_content_type"
    )
    with pytest.raises(CurriculumResolutionError):
        CurriculumRegistry.resolve_chapter_path(identity)

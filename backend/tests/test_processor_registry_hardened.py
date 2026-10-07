import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.processors.registry import ProcessorRegistry, ProcessorNotFoundError

def test_maths_i_cannot_resolve_maths_ii():
    # Trying to resolve maths_ii processor using maths_i identity must raise ProcessorNotFoundError
    identity = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_ii",
        part="part1", # mismatched part
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ProcessorNotFoundError):
        ProcessorRegistry.resolve(identity)

def test_maths_ii_cannot_resolve_maths_i():
    identity = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_i",
        part="part2", # mismatched part
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ProcessorNotFoundError):
        ProcessorRegistry.resolve(identity)

def test_social_i_cannot_resolve_social_ii():
    identity = CurriculumIdentity(
        grade="7",
        subject="social_science",
        book="social_ii",
        part="part1",
        unit="U01",
        chapter_id="G7-SOC-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ProcessorNotFoundError):
        ProcessorRegistry.resolve(identity)

def test_main_cannot_resolve_split_book():
    identity = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="main",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ProcessorNotFoundError):
        ProcessorRegistry.resolve(identity)

def test_processor_registry_introspection():
    details = ProcessorRegistry.introspect()
    assert len(details) > 0
    assert any(d["book"] == "maths_i" for d in details)
    assert any(d["book"] == "maths_ii" for d in details)

import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.processors.registry import ProcessorRegistry
from src.curriculum.processors.class5.english_processor import Class5EnglishProcessor
from src.curriculum.processors.class7.mathematics_i_processor import Class7MathematicsIProcessor

def test_processor_registry_resolution_class5():
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    proc = ProcessorRegistry.resolve(identity)
    assert isinstance(proc, Class5EnglishProcessor)

def test_processor_registry_resolution_class7_maths_i():
    identity = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_i",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    proc = ProcessorRegistry.resolve(identity)
    assert isinstance(proc, Class7MathematicsIProcessor)

def test_processor_registry_unknown_raises():
    identity = CurriculumIdentity(
        grade="99",
        subject="unknown_subject",
        book="main",
        part="none",
        unit="U01",
        chapter_id="X",
        content_type="overview"
    )
    with pytest.raises(ValueError):
        ProcessorRegistry.resolve(identity)

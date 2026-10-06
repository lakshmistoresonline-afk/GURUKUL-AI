import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.processors.registry import ProcessorRegistry, ProcessorNotFoundError
from src.curriculum.processors.class5.english_processor import Class5EnglishProcessor
from src.curriculum.processors.class7.mathematics_i_processor import Class7MathematicsIProcessor
from src.curriculum.processors.class7.mathematics_ii_processor import Class7MathematicsIIProcessor

def test_gen2_processor_resolution_class5_english():
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

    # Test actual execution
    res = proc.process(identity, {"title": "Papa's Spectacles"})
    assert res["title"] == "Papa's Spectacles"

def test_gen2_processor_resolution_class7_maths_i_and_ii():
    id_i = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_i",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    id_ii = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_ii",
        part="part2",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )

    proc_i = ProcessorRegistry.resolve(id_i)
    proc_ii = ProcessorRegistry.resolve(id_ii)

    assert isinstance(proc_i, Class7MathematicsIProcessor)
    assert isinstance(proc_ii, Class7MathematicsIIProcessor)
    assert proc_i != proc_ii

def test_gen2_processor_rejection_unknown_identity():
    invalid_identity = CurriculumIdentity(
        grade="99",
        subject="unknown_subject",
        book="unknown_book",
        part="unknown_part",
        unit="U99",
        chapter_id="X99",
        content_type="overview"
    )
    with pytest.raises(ProcessorNotFoundError):
        ProcessorRegistry.resolve(invalid_identity)

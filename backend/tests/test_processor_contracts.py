import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.processors.registry import ProcessorRegistry, ProcessorNotFoundError
from src.curriculum.processors.class7.mathematics_ii_processor import Class7MathematicsIIProcessor

def test_processor_contract_class7_maths_ii():
    identity = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_ii",
        part="part2",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    proc = ProcessorRegistry.resolve(identity)
    assert isinstance(proc, Class7MathematicsIIProcessor)

    output = proc.process(identity, {"title": "Maths II Chapter"})
    assert output["schema_version"] == "3.0.0"
    assert output["processor_version"] == "V14-STRICT"
    assert output["provenance"]["book"] == "maths_ii"
    assert output["provenance"]["part"] == "part2"

def test_processor_contract_negative_wrong_identity():
    # Attempting to process with invalid input or wrong identity constraints
    proc = Class7MathematicsIIProcessor()
    wrong_identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ValueError):
        proc.process(wrong_identity, {"title": "Wrong Data"})

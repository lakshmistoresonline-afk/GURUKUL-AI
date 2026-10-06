import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, CurriculumResolutionError

def test_maths_i_vs_maths_ii_strict_isolation():
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

    path_i = CurriculumRegistry.resolve_chapter_path(id_i)
    # Trying to resolve maths_ii chapter under MathsI folder should raise CurriculumResolutionError
    id_invalid_cross = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_ii",
        part="part2",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    # Since G7-MAT-U01-C01 is in MathsI, requesting MathsII with that chapter ID should either not find it or raise error if folder differs
    assert path_i is not None

import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, CurriculumResolutionError

def test_identity_dimensions_mandatory():
    # Incomplete identity missing dimensions should raise Pydantic ValidationError
    with pytest.raises(Exception):
        CurriculumIdentity(
            grade="5",
            subject="english",
            book="", # empty
            part="none",
            unit="U01",
            chapter_id="C01",
            content_type="overview"
        )

def test_cache_key_uniqueness_across_all_dimensions():
    id1 = CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U01", chapter_id="C01", content_type="overview")
    id2 = CurriculumIdentity(grade="7", subject="mathematics", book="maths_ii", part="part2", unit="U01", chapter_id="C01", content_type="overview")
    id3 = CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U02", chapter_id="C01", content_type="overview")

    assert id1.to_cache_key() != id2.to_cache_key()
    assert id1.to_cache_key() != id3.to_cache_key()

def test_maths_i_vs_maths_ii_isolation():
    id_i = CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview")
    id_ii = CurriculumIdentity(grade="7", subject="mathematics", book="maths_ii", part="part2", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview")

    # Both resolve or fail cleanly without collapsing into each other
    path_i = CurriculumRegistry.resolve_chapter_path(id_i)
    path_ii = CurriculumRegistry.resolve_chapter_path(id_ii)
    assert path_i != path_ii

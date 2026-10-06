import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.services.cache_service import CurriculumCacheService

def test_cache_collision_maths_i_vs_maths_ii():
    id_i = CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U01", chapter_id="C01", content_type="overview")
    id_ii = CurriculumIdentity(grade="7", subject="mathematics", book="maths_ii", part="part2", unit="U01", chapter_id="C01", content_type="overview")

    key_i = CurriculumCacheService.generate_cache_key(id_i)
    key_ii = CurriculumCacheService.generate_cache_key(id_ii)

    assert key_i != key_ii

    CurriculumCacheService.set(id_i, "Maths I Data")
    CurriculumCacheService.set(id_ii, "Maths II Data")

    assert CurriculumCacheService.get(id_i) == "Maths I Data"
    assert CurriculumCacheService.get(id_ii) == "Maths II Data"

def test_cache_collision_english_vs_hindi():
    id_eng = CurriculumIdentity(grade="5", subject="english", book="main", part="none", unit="U01", chapter_id="C01", content_type="notes")
    id_hin = CurriculumIdentity(grade="5", subject="hindi", book="main", part="none", unit="U01", chapter_id="C01", content_type="notes")

    assert CurriculumCacheService.generate_cache_key(id_eng) != CurriculumCacheService.generate_cache_key(id_hin)

def test_cache_collision_class5_vs_class6():
    id_c5 = CurriculumIdentity(grade="5", subject="science", book="main", part="none", unit="U01", chapter_id="C01", content_type="quiz")
    id_c6 = CurriculumIdentity(grade="6", subject="science", book="main", part="none", unit="U01", chapter_id="C01", content_type="quiz")

    assert CurriculumCacheService.generate_cache_key(id_c5) != CurriculumCacheService.generate_cache_key(id_c6)

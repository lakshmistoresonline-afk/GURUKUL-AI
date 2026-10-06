import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.services.cache_service import CurriculumCacheService

def test_cache_key_isolation_across_grades():
    id5 = CurriculumIdentity(grade="5", subject="english", book="main", part="none", unit="U01", chapter_id="C01", content_type="notes")
    id6 = CurriculumIdentity(grade="6", subject="english", book="main", part="none", unit="U01", chapter_id="C01", content_type="notes")

    key5 = CurriculumCacheService.generate_cache_key(id5)
    key6 = CurriculumCacheService.generate_cache_key(id6)

    assert key5 != key6

def test_cache_key_isolation_across_books_or_parts():
    id_part1 = CurriculumIdentity(grade="7", subject="mathematics", book="maths_i", part="part1", unit="U01", chapter_id="C01", content_type="overview")
    id_part2 = CurriculumIdentity(grade="7", subject="mathematics", book="maths_ii", part="part2", unit="U01", chapter_id="C01", content_type="overview")

    key1 = CurriculumCacheService.generate_cache_key(id_part1)
    key2 = CurriculumCacheService.generate_cache_key(id_part2)

    assert key1 != key2

def test_cache_key_isolation_across_units():
    id_u1 = CurriculumIdentity(grade="6", subject="science", book="main", part="none", unit="U01", chapter_id="C01", content_type="quiz")
    id_u2 = CurriculumIdentity(grade="6", subject="science", book="main", part="none", unit="U02", chapter_id="C01", content_type="quiz")

    key1 = CurriculumCacheService.generate_cache_key(id_u1)
    key2 = CurriculumCacheService.generate_cache_key(id_u2)

    assert key1 != key2

def test_cache_storage_retrieval():
    CurriculumCacheService.clear()
    identity = CurriculumIdentity(grade="5", subject="hindi", book="main", part="none", unit="U01", chapter_id="C01", content_type="master")

    assert CurriculumCacheService.get(identity) is None
    CurriculumCacheService.set(identity, {"data": "test_payload"})
    assert CurriculumCacheService.get(identity) == {"data": "test_payload"}

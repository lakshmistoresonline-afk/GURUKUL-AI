import os
import sys
import json
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, str(backend_dir))

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, ChapterNotFoundError, ContentSchemaError, ManifestMissingError, ManifestMalformedError

def test_registry_exact_valid_identity():
    id_req = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    node = CurriculumRegistry.resolve_node(id_req)
    assert node["chapter_id"] == "G5-ENG-U01-C01"

def test_registry_wrong_book_raises_not_found():
    id_req = CurriculumIdentity(
        grade="5",
        subject="english",
        book="wrong_book_name",
        part="main",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(id_req)

def test_registry_wrong_unit_raises_not_found():
    id_req = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U99",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(id_req)

def test_registry_maths_i_vs_maths_ii_isolation():
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
    node_i = CurriculumRegistry.resolve_node(id_i)
    node_ii = CurriculumRegistry.resolve_node(id_ii)
    assert node_i["book"] == "maths_i"
    assert node_ii["book"] == "maths_ii"
    assert node_i["book"] != node_ii["book"]

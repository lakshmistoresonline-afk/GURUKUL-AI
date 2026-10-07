import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app
from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.core.curriculum_registry import CurriculumRegistry, ChapterNotFoundError
from src.curriculum.processors.registry import ProcessorRegistry, ProcessorNotFoundError

client = TestClient(app)

def test_cross_layer_maths_i_vs_maths_ii_strict_isolation():
    # Maths I identity
    id_i = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_i",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    # Maths II identity
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
    assert node_i["processed_path"] != node_ii["processed_path"]

    proc_i = ProcessorRegistry.resolve(id_i)
    proc_ii = ProcessorRegistry.resolve(id_ii)
    assert proc_i != proc_ii

    # API request cross-contamination check
    res_i = client.get("/api/v1/curriculum/resolve?grade=7&subject=mathematics&book=maths_i&part=part1&unit=U01&chapter_id=G7-MAT-U01-C01&content_type=overview")
    res_ii = client.get("/api/v1/curriculum/resolve?grade=7&subject=mathematics&book=maths_ii&part=part2&unit=U01&chapter_id=G7-MAT-U01-C01&content_type=overview")

    assert res_i.status_code == 200
    assert res_ii.status_code == 200
    assert res_i.json()["identity"]["book"] == "maths_i"
    assert res_ii.json()["identity"]["book"] == "maths_ii"

def test_cross_layer_social_i_vs_social_ii_strict_isolation():
    id_i = CurriculumIdentity(
        grade="7",
        subject="social_science",
        book="social_i",
        part="part1",
        unit="U01",
        chapter_id="G7-SOC-U01-C01",
        content_type="overview"
    )
    id_ii = CurriculumIdentity(
        grade="7",
        subject="social_science",
        book="social_ii",
        part="part2",
        unit="U01",
        chapter_id="G7-SOC-U01-C01",
        content_type="overview"
    )

    node_i = CurriculumRegistry.resolve_node(id_i)
    node_ii = CurriculumRegistry.resolve_node(id_ii)

    assert node_i["book"] == "social_i"
    assert node_ii["book"] == "social_ii"

def test_cross_layer_class5_vs_class6_english():
    id_5 = CurriculumIdentity(
        grade="5",
        subject="english",
        book="english",
        part="main",
        unit="U01",
        chapter_id="G5-ENG-U01-C01",
        content_type="overview"
    )
    id_6 = CurriculumIdentity(
        grade="6",
        subject="english",
        book="english",
        part="main",
        unit="U01",
        chapter_id="G6-ENG-U01-C01",
        content_type="overview"
    )

    node_5 = CurriculumRegistry.resolve_node(id_5)
    node_6 = CurriculumRegistry.resolve_node(id_6)

    assert node_5["grade"] == "5"
    assert node_6["grade"] == "6"

def test_cross_layer_invalid_identity_rejections():
    # Invalid book
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(CurriculumIdentity(
            grade="7", subject="mathematics", book="invalid_book", part="part1", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview"
        ))

    # Invalid part
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(CurriculumIdentity(
            grade="7", subject="mathematics", book="maths_i", part="invalid_part", unit="U01", chapter_id="G7-MAT-U01-C01", content_type="overview"
        ))

    # Invalid unit
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(CurriculumIdentity(
            grade="7", subject="mathematics", book="maths_i", part="part1", unit="U99", chapter_id="G7-MAT-U01-C01", content_type="overview"
        ))

    # Invalid chapter
    with pytest.raises(ChapterNotFoundError):
        CurriculumRegistry.resolve_node(CurriculumIdentity(
            grade="7", subject="mathematics", book="maths_i", part="part1", unit="U01", chapter_id="NONEXISTENT", content_type="overview"
        ))

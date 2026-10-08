import os
import sys
import pytest
from fastapi.testclient import TestClient

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.main import app
from src.curriculum.core.curriculum_registry import CurriculumRegistry

client = TestClient(app)

def test_chapters_source_api_unit_number_authoritative():
    index = CurriculumRegistry.get_index()
    assert len(index) > 0

    # Pick a few representative nodes
    for key, node in list(index.items())[:10]:
        grade = node["grade"]
        subj = node["canonical_subject"]
        book = node["book"]
        part = node["part"]
        unit = node["unit"]
        ch_id = node["chapter_id"]
        expected_unit_number = node["unit_number"]

        res = client.get(f"/api/v1/chapters/{ch_id}/source?grade={grade}&subject={subj}&book={book}&part={part}&unit={unit}")
        assert res.status_code == 200, f"Failed for key {key}: {res.text}"
        data = res.json()
        assert data["unitNumber"] == expected_unit_number

def test_split_book_isolation_api():
    # Request Class 7 Maths I chapter
    res_i = client.get("/api/v1/chapters/G7-MAT-U01-C01/source?grade=7&subject=mathematics&book=maths_i&part=part1&unit=U01")
    # Request Class 7 Maths II chapter
    res_ii = client.get("/api/v1/chapters/G7-MAT-U01-C01/source?grade=7&subject=mathematics&book=maths_ii&part=part2&unit=U01")

    assert res_i.status_code == 200
    assert res_ii.status_code == 200
    assert res_i.json()["book"] == "maths_i"
    assert res_ii.json()["book"] == "maths_ii"
    assert res_i.json()["book"] != res_ii.json()["book"]

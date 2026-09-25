import pytest
from src.services.content_loader import ContentLoaderService

def test_curricular_goals_pipeline_contract():
    """Verify that ContentLoaderService extracts all 3 fields (code, name, description) for all 4 goals."""
    meta = ContentLoaderService.get_subject_curriculum_metadata("5", "English")

    assert meta["curriculumFramework"] == "NEP 2020 & NCF-SE 2023"
    goals = meta["curricularGoals"]
    assert len(goals) == 4

    expected_goals = {
        "CG1": "Communication",
        "CG2": "Reading Comprehension",
        "CG3": "Expressive Writing",
        "CG4": "Vocabulary Expansion",
    }

    for g in goals:
        assert "code" in g
        assert "name" in g
        assert "description" in g
        assert g["code"] in expected_goals
        assert g["name"] == expected_goals[g["code"]]
        assert len(g["description"]) > 10

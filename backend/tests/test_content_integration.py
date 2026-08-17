import pytest
import os
from src.utils.path_resolver import PathResolver
from src.config.app_config import settings

def test_path_resolver_class_5():
    hierarchy = PathResolver.get_class_hierarchy("class_5")
    assert "english" in hierarchy
    assert len(hierarchy["english"]) > 0
    # Class 5 English Chapter 1 should be eesa101
    found = False
    for ch in hierarchy["english"]:
        if ch["id"] == "eesa101":
            found = True
            assert ch["name"] == "Papa’s Spectacles"
    assert found

def test_path_resolver_class_6():
    hierarchy = PathResolver.get_class_hierarchy("class_6")
    assert "science" in hierarchy
    assert len(hierarchy["science"]) > 0

def test_chapter_path_resolution():
    path = PathResolver.get_chapter_path("class_5", "eesa101")
    assert path is not None
    assert "Class 5" in path
    assert "English" in path
    assert os.path.exists(os.path.join(path, "package.json"))

def test_master_content_root_exists():
    assert os.path.exists(settings.MASTER_CONTENT_ROOT)
    assert os.path.isdir(settings.MASTER_CONTENT_ROOT)

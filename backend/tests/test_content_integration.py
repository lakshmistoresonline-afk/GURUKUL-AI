import pytest
import os
from src.utils.path_resolver import PathResolver
from src.config.app_config import settings

def test_path_resolver_class_5():
    hierarchy = PathResolver.get_class_hierarchy("class_5")
    assert "english" in hierarchy
    assert len(hierarchy["english"]) > 0
    # Class 5 English Chapter 1 should be e05_c1
    found = False
    for ch in hierarchy["english"]:
        if ch["id"] == "e05_c1":
            found = True
            # Title was updated to real title in import v3
            assert "Papa" in ch["name"]
    assert found

def test_path_resolver_class_6():
    hierarchy = PathResolver.get_class_hierarchy("class_6")
    assert "science" in hierarchy
    assert len(hierarchy["science"]) > 0

def test_chapter_path_resolution():
    path = PathResolver.get_chapter_path("class_5", "e05_c1")
    assert path is not None
    assert "class_05" in path
    assert "english" in path
    assert os.path.exists(os.path.join(path, "package.json"))

def test_master_content_root_exists():
    assert os.path.exists(settings.MASTER_CONTENT_ROOT)
    assert os.path.isdir(settings.MASTER_CONTENT_ROOT)

import pytest
import os
import json
from src.utils.youtube_utils import normalize_youtube_resource, extract_video_id, is_search_url

def test_youtube_normalization_direct():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    norm = normalize_youtube_resource(url)
    assert norm["type"] == "DIRECT_VIDEO"
    assert norm["video_id"] == "dQw4w9WgXcQ"
    assert norm["is_playable"] is True

def test_youtube_normalization_short():
    url = "https://youtu.be/dQw4w9WgXcQ"
    norm = normalize_youtube_resource(url)
    assert norm["type"] == "DIRECT_VIDEO"
    assert norm["video_id"] == "dQw4w9WgXcQ"

def test_youtube_normalization_search():
    url = "https://www.youtube.com/results?search_query=NCERT+Class+6"
    norm = normalize_youtube_resource(url)
    assert norm["type"] == "DISCOVERY_SEARCH"
    assert norm["is_playable"] is False

def test_extract_video_id_invalid():
    assert extract_video_id("https://google.com") is None
    assert extract_video_id("https://youtube.com/results?q=test") is None

def test_is_search_url():
    assert is_search_url("https://www.youtube.com/results?search_query=test") is True
    assert is_search_url("https://www.youtube.com/watch?v=123") is False

@pytest.mark.asyncio
async def test_auth_user_class_derivation():
    try:
        from src.utils.auth import AuthUser
        user = AuthUser("uid123", "test@test.com", "student", "7")
        assert user.class_name == "class_7"

        user_no_class = AuthUser("uid456", "admin@test.com", "admin", "")
        assert user_no_class.class_name is None
    except ImportError:
        pytest.skip("Auth dependencies not available")

def test_config_paths_dynamic():
    from src.config.app_config import settings
    # Verify that the path is constructed using PROJECT_ROOT and not the hardcoded D: string from previous version
    assert "Multimedia" in settings.MULTIMEDIA_EXTERNAL_CATALOG_PATH
    # It should be an absolute path (calculated at runtime)
    assert os.path.isabs(settings.MULTIMEDIA_EXTERNAL_CATALOG_PATH)

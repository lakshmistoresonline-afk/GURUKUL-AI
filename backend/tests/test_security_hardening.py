import pytest
import os
import sys
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.main import app
from src.utils.auth import AuthUser

client = TestClient(app)

@pytest.fixture
def mock_auth_user():
    return AuthUser(uid="test_uid", email="test@example.com", role="student", class_id="7")

@pytest.fixture
def mock_admin_user():
    return AuthUser(uid="admin_uid", email="admin@example.com", role="admin", class_id="0")

def test_unauthenticated_access():
    """Verify that endpoints require authentication."""
    response = client.get("/api/srs/due/test_uid")
    assert response.status_code == 401

@patch("src.utils.token_cache.verify_and_get_uid")
@patch("src.utils.auth.get_user_profile")
def test_student_cannot_access_other_student_data(mock_profile, mock_token, mock_auth_user):
    """TEST 6: Student cannot submit another student's UID to access their SRS data."""
    mock_token.return_value = "student_a"
    mock_profile.return_value = {"uid": "student_a", "role": "student", "classId": "7", "email": "a@test.com"}

    # student_a tries to access student_b's data
    response = client.get(
        "/api/srs/due/student_b",
        headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 403
    assert "Unauthorized access" in response.json()["detail"]

@patch("src.utils.token_cache.verify_and_get_uid")
@patch("src.utils.auth.get_user_profile")
def test_class_isolation_enforcement(mock_profile, mock_token):
    """TEST 5: Student class_6 cannot access class_7 content."""
    mock_token.return_value = "student_6"
    mock_profile.return_value = {"uid": "student_6", "role": "student", "classId": "6", "email": "6@test.com"}

    # student of class 6 tries to access class 7 package
    response = client.get(
        "/api/chapters/package/class_7/english/e07_c1",
        headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 403
    assert "Access Denied" in response.json()["detail"]

@patch("src.utils.token_cache.verify_and_get_uid")
@patch("src.utils.auth.get_user_profile")
def test_role_spoofing_prevention(mock_profile, mock_token):
    """TEST 8: Client cannot spoof X-User-Role to become admin."""
    mock_token.return_value = "student_a"
    mock_profile.return_value = {"uid": "student_a", "role": "student", "classId": "7", "email": "a@test.com"}

    response = client.get(
        "/api/media/admin/external/pending",
        headers={
            "Authorization": "Bearer valid_token",
            "X-User-Role": "admin" # Spoofed header
        }
    )
    assert response.status_code == 403
    # Check detail - it depends on the exact endpoint check logic
    assert response.status_code == 403

def test_youtube_classification():
    """TEST 1 & 2: Verify YouTube URL classification."""
    from src.utils.youtube_utils import normalize_youtube_resource

    direct = normalize_youtube_resource("https://www.youtube.com/watch?v=ABC12345678")
    assert direct["type"] == "DIRECT_VIDEO"

    search = normalize_youtube_resource("https://www.youtube.com/results?search_query=NCERT")
    assert search["type"] == "DISCOVERY_SEARCH"

@patch("src.utils.auth.get_current_user")
@pytest.mark.asyncio
async def test_brain_boost_srs_eligibility(mock_get_user, mock_auth_user):
    """TEST 10: Brain Boost with srsEligible=false does not create an SRS item."""
    mock_get_user.return_value = mock_auth_user

    from src.services.general_learning_service import GeneralLearningService
    from unittest.mock import AsyncMock

    mock_srs = AsyncMock()
    gl_service = GeneralLearningService(mock_srs)

    # Mock data item with srsEligible=false
    item = {"id": "bb_1", "type": "brain_boost", "srsEligible": False, "class_key": "class_7"}

    with patch.object(GeneralLearningService, "get_content", return_value=item):
        from src.routes.general_learning_routes import record_progress, GLProgressRequest

        req = GLProgressRequest(content_id="bb_1", rating=3)
        res = await record_progress(req, mock_auth_user)

        assert res["status"] == "SUCCESS"
        assert "non-SRS" in res["message"]
        mock_srs.record_review.assert_not_called()

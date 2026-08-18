import pytest
import asyncio
import os
import sys
from sqlalchemy import select

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.services.external_media_service import ExternalMediaService
from src.services.mastery_service import MasteryService
from src.models.resource import ExternalMultimediaResource

@pytest.fixture
def mastery_service():
    return MasteryService()

@pytest.fixture
def external_media_service(mastery_service):
    # Use an in-memory or temporary database for testing
    from src.config.app_config import settings
    original_db = settings.DATABASE_URL
    settings.DATABASE_URL = "sqlite+aiosqlite:///./test_external.db"

    service = ExternalMediaService(mastery_service)
    yield service

    # Restore
    settings.DATABASE_URL = original_db
    if os.path.exists("test_external.db"):
        try:
            os.remove("test_external.db")
        except:
            pass

@pytest.mark.asyncio
async def test_reload_catalogs(external_media_service):
    await external_media_service.init_db()
    # Initial reload is done in init_db

    stats = await external_media_service.get_stats()
    assert stats["total_resources"] > 0
    # 163 chapters * 2 resources = 326. Some might fail to load.
    assert stats["total_resources"] > 150

@pytest.mark.asyncio
async def test_verification_workflow(external_media_service):
    await external_media_service.init_db()

    pending = await external_media_service.get_admin_pending_resources()
    if not pending:
        pytest.skip("No pending resources to test")

    target = pending[0]
    res_id = target["id"]

    # 1. Verify
    await external_media_service.verify_resource(res_id, "test_admin")

    # 2. Check visibility for student
    verified = await external_media_service.get_verified_resources(chapter_id=target["chapter_id"])
    assert any(r["id"] == res_id for r in verified)

    # 3. Reject
    await external_media_service.reject_resource(res_id)
    verified_after = await external_media_service.get_verified_resources(chapter_id=target["chapter_id"])
    assert not any(r["id"] == res_id for r in verified_after)

@pytest.mark.asyncio
async def test_no_youtube_duplication(external_media_service):
    await external_media_service.init_db()

    async with external_media_service.AsyncSession() as session:
        stmt = select(ExternalMultimediaResource).where(
            ExternalMultimediaResource.url.like("%youtube.com%") |
            ExternalMultimediaResource.url.like("%youtu.be%")
        )
        res = await session.execute(stmt)
        assert len(res.scalars().all()) == 0

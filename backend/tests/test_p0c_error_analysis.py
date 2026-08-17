import unittest
import os
import json
import sys
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.services.srs_service import SRSService
from src.services.resource_service import ResourceService
from src.orchestrator.ai_orchestrator import AIOrchestrator
from src.config.app_config import settings

class TestP0CErrorAnalysis(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.orchestrator = AIOrchestrator()
        self.resource_service = ResourceService(self.orchestrator)
        await self.resource_service.init_db()
        self.srs_service = SRSService(self.resource_service.AsyncSession)
        settings.ADAPTIVE_MASTERY_ERROR_ANALYSIS = "ACTIVE"

        # Cleanup
        async with self.resource_service.AsyncSession() as session:
            from src.models.srs import ErrorEvent
            from sqlalchemy import delete
            await session.execute(delete(ErrorEvent))
            await session.commit()

    async def test_record_error_event(self):
        student_id = "error_test_user"
        # 1. Record a CONCEPTUAL error
        res = await self.srs_service.record_error(
            student_id, "Q1", "class_6_mathematics_fegp101_patterns", "CONCEPTUAL", "fegp101"
        )
        self.assertEqual(res["status"], "SUCCESS")

        # 2. Verify persistence in SQLite
        async with self.resource_service.AsyncSession() as session:
            from src.models.srs import ErrorEvent
            from sqlalchemy import select
            stmt = select(ErrorEvent).where(ErrorEvent.student_id == student_id)
            db_res = await session.execute(stmt)
            events = db_res.scalars().all()
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].error_type, "CONCEPTUAL")

    async def test_error_analysis_off(self):
        settings.ADAPTIVE_MASTERY_ERROR_ANALYSIS = "OFF"
        res = await self.srs_service.record_error("U1", "Q1", "C1", "CARELESS", "CH1")
        self.assertIsNone(res)

if __name__ == "__main__":
    unittest.main()

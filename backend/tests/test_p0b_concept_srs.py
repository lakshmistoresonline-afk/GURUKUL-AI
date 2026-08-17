import unittest
import os
import json
import sys
import asyncio
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.services.srs_service import SRSService
from src.services.resource_service import ResourceService
from src.orchestrator.ai_orchestrator import AIOrchestrator
from src.config.app_config import settings

class TestP0BConceptSRS(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.orchestrator = AIOrchestrator()
        self.resource_service = ResourceService(self.orchestrator)
        await self.resource_service.init_db()
        self.srs_service = SRSService(self.resource_service.AsyncSession)

        # Enable SRS for testing
        settings.ADAPTIVE_MASTERY_CONCEPT_SRS = "ACTIVE"

        # Cleanup test data
        async with self.resource_service.AsyncSession() as session:
            from src.models.srs import SRSItem, SRSReview
            from sqlalchemy import delete
            await session.execute(delete(SRSReview))
            await session.execute(delete(SRSItem))
            await session.commit()

    async def test_concept_tracking_initialization(self):
        student_id = "test_student_1"
        concept_id = "class_6_mathematics_fegp101_patterns"
        chapter_id = "fegp101"

        await self.srs_service.ensure_concept_tracked(student_id, concept_id, chapter_id)

        due = await self.srs_service.get_due_items(student_id, content_type='concept')
        self.assertTrue(any(i['content_id'] == concept_id for i in due))

    async def test_reused_ids_distinct(self):
        student_id = "test_student_2"
        # Shared local ID english_1_c01 in different units
        c1 = "class_6_english_unit_01_english_1_c01"
        c2 = "class_6_english_unit_02_english_1_c01"

        await self.srs_service.ensure_concept_tracked(student_id, c1, "unit1")
        await self.srs_service.ensure_concept_tracked(student_id, c2, "unit2")

        items = await self.srs_service.get_due_items(student_id, content_type='concept', limit=100)
        c_ids = [i['content_id'] for i in items]
        self.assertIn(c1, c_ids)
        self.assertIn(c2, c_ids)
        self.assertNotEqual(c1, c2)

    async def test_successful_retrieval_updates_interval(self):
        student_id = "test_student_3"
        concept_id = "c3"

        # 1. First review (Rating 3: Good)
        res = await self.srs_service.record_review(student_id, concept_id, 'concept', 3)
        self.assertEqual(res['interval'], 1)
        self.assertEqual(res['repetitions'], 1)

        # 2. Second review (Rating 3)
        # Mocking repetitions for the same item by calling again
        res = await self.srs_service.record_review(student_id, concept_id, 'concept', 3)
        self.assertEqual(res['interval'], 3)
        self.assertEqual(res['repetitions'], 2)

    async def test_failed_retrieval_resets_interval(self):
        student_id = "test_student_4"
        concept_id = "c4"

        # Start with some repetitions
        await self.srs_service.record_review(student_id, concept_id, 'concept', 4) # rep 1
        await self.srs_service.record_review(student_id, concept_id, 'concept', 4) # rep 2

        # Fail (Rating 1: Again)
        res = await self.srs_service.record_review(student_id, concept_id, 'concept', 1)
        self.assertEqual(res['interval'], 1)
        self.assertEqual(res['repetitions'], 0)
        # EF should be lower than what it was after successful reviews
        self.assertLess(res['easiness_factor'], 2.7)

    async def test_shadow_mode_impact(self):
        settings.ADAPTIVE_MASTERY_CONCEPT_SRS = "SHADOW"
        student_id = "test_student_shadow"
        concept_id = "c_shadow"

        # In shadow mode, we still record but maybe we distinguish it?
        # The logic I implemented actually applies it to the DB if not OFF.
        # "calculate concept review schedules, store concept retention records"
        res = await self.srs_service.record_review(student_id, concept_id, 'concept', 3)
        self.assertIsNotNone(res)
        self.assertEqual(res['interval'], 1)

    async def test_off_mode_disabled(self):
        settings.ADAPTIVE_MASTERY_CONCEPT_SRS = "OFF"
        student_id = "test_student_off"
        concept_id = "c_off"

        res = await self.srs_service.record_review(student_id, concept_id, 'concept', 3)
        self.assertIsNone(res)

if __name__ == "__main__":
    unittest.main()

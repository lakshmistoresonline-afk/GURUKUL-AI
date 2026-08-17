import unittest
import os
import json
import sys
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.services.srs_service import SRSService
from src.services.resource_service import ResourceService
from src.orchestrator.ai_orchestrator import AIOrchestrator
from src.config.app_config import settings

class TestP0CInterleaving(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.orchestrator = AIOrchestrator()
        self.resource_service = ResourceService(self.orchestrator)
        await self.resource_service.init_db()
        self.srs_service = SRSService(self.resource_service.AsyncSession)
        settings.ADAPTIVE_MASTERY_INTERLEAVING = "ACTIVE"

    async def test_review_coordination_detection(self):
        # We test the internal _identify_review_overlaps helper
        from src.models.srs import SRSItem
        student_id = "coord_test_user"

        # Mock items: Chapter A and Concept A1 (from Chapter A)
        items = [
            SRSItem(content_id="eemm101", content_type="chapter", metadata_json={}),
            SRSItem(content_id="class_5_mathematics_eemm101_travellers", content_type="concept", metadata_json={"chapterId": "eemm101"})
        ]

        # Test detection
        # Re-using the logic from _identify_review_overlaps but checking return or log
        with self.assertLogs('src.services.srs_service', level='INFO') as cm:
            await self.srs_service._identify_review_overlaps(student_id, items)
            self.assertTrue(any("Overlap: Concept class_5_mathematics_eemm101_travellers and Chapter eemm101" in output for output in cm.output))

if __name__ == "__main__":
    unittest.main()

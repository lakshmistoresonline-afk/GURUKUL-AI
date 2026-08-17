import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .mastery_service import MasteryService
from .srs_service import SRSService

logger = logging.getLogger(__name__)

class LearningPlanService:
    def __init__(self, mastery_service: MasteryService, srs_service: SRSService):
        self.mastery_service = mastery_service
        self.srs_service = srs_service

    async def generate_daily_plan(self, student_id: str, class_name: str) -> Dict[str, Any]:
        """
        Generates a structured daily plan for the student.
        """
        # 1. Start with high-priority retention items
        due_reviews = await self.srs_service.get_due_items(student_id, limit=3)

        plan = {
            "summary": "Focus on consolidating recent knowledge while pushing into new topics.",
            "activities": []
        }

        for item in due_reviews:
            plan["activities"].append({
                "type": "RETENTION_REVIEW",
                "title": f"Refresh: {item['content_id']}",
                "estimated_time": 5,
                "context": item
            })

        # 2. Add in-progress chapters
        # (Mocked for now as we'd need to query all mastery records for this user)
        # In a real system, we'd fetch top 2 chapters with status != MASTERED

        return plan

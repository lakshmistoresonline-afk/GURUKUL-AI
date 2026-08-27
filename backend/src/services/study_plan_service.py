import logging
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.planner import StudyPlan, StudyTask, TaskType
from ..services.mastery_service import MasteryService

logger = logging.getLogger(__name__)

class StudyPlanService:
    def __init__(self, db_session: AsyncSession, mastery_service: MasteryService):
        self.db = db_session
        self.mastery = mastery_service

    async def generate_weekly_plan(self, student_id: str, class_name: str) -> StudyPlan:
        """Generates a personalized weekly study plan."""
        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=7)

        # 1. Identify weak concepts to focus on
        # mastery_records = await self.mastery.get_student_mastery(student_id)
        # weak_concepts = [m for m in mastery_records if m.status == "NEEDS_REVISION"]

        tasks = []
        # Mocking task generation for now
        for i in range(7):
            date = start_date + timedelta(days=i)
            tasks.append(StudyTask(
                id=str(uuid.uuid4()),
                title=f"Day {i+1} Study Session",
                type=TaskType.LEARN,
                estimated_time_minutes=45,
                scheduled_date=date
            ))

        plan = StudyPlan(
            id=str(uuid.uuid4()),
            student_id=student_id,
            tasks_json=[t.to_dict() for t in tasks],
            start_date=start_date,
            end_date=end_date
        )

        self.db.add(plan)
        await self.db.commit()
        return plan

    async def get_plan(self, student_id: str) -> Optional[StudyPlan]:
        result = await self.db.execute(
            select(StudyPlan).where(StudyPlan.student_id == student_id).order_by(StudyPlan.created_at.desc())
        )
        return result.scalars().first()

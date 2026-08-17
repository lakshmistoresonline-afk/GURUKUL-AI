import random
from typing import List, Dict, Any
from .mastery_service import MasteryService
from .srs_service import SRSService
from ..models.learning import LearningActivity
from sqlalchemy import select, and_, func
from datetime import datetime, time

class DailyMissionService:
    def __init__(self, mastery_service: MasteryService, srs_service: SRSService):
        self.mastery_service = mastery_service
        self.srs_service = srs_service
        self.AsyncSession = srs_service.AsyncSession

    async def generate_mission(self, student_id: str, student_mastery: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates a balanced daily learning mission for the student.
        """
        tasks = []

        # Determine today's boundaries for completion check
        today_start = datetime.combine(datetime.utcnow().date(), time.min)

        async with self.AsyncSession() as session:
            # Fetch today's completed activity types and targets
            stmt = select(LearningActivity.activity_type, LearningActivity.chapter_id, LearningActivity.concept_id).where(
                and_(
                    LearningActivity.student_id == student_id,
                    LearningActivity.started_at >= today_start,
                    LearningActivity.status == 'COMPLETED'
                )
            )
            res = await session.execute(stmt)
            completed_today = res.all()

            # Helper to check if a task is already completed today
            def is_done(activity_type, chapter_id=None, concept_id=None):
                for row in completed_today:
                    if row[0] == activity_type:
                        if chapter_id and row[1] != chapter_id: continue
                        if concept_id and row[2] != concept_id: continue
                        return True
                return False

            # 1. Critical Retention Review (Priority 1)
            due_items = await self.srs_service.get_due_items(student_id, content_type='concept', limit=2)
            for item in due_items:
                tasks.append({
                    "type": "RETRIEVE",
                    "target": item['content_id'],
                    "label": f"Review {item['content_id'].split('_')[-1]}",
                    "description": "Strengthen your memory of this concept.",
                    "priority": "HIGH",
                    "status": "COMPLETED" if is_done("RETENTION_REVIEW", concept_id=item['content_id']) else "PENDING"
                })

            # 2. Remediation (Priority 2)
            for record in student_mastery:
                if record.get("status") == "NEEDS_REMEDIATION":
                    tasks.append({
                        "type": "REMEDIATE",
                        "chapterId": record['chapterId'],
                        "label": "Neural Repair Session",
                        "description": f"Fix weak spots in {record.get('chapterId')}.",
                        "priority": "HIGH",
                        "status": "COMPLETED" if is_done("REMEDIATE", chapter_id=record['chapterId']) else "PENDING"
                    })
                    break

            # 3. Continue Current Learning (Priority 3)
            learning_chapters = [r for r in student_mastery if r.get("status") in ["LEARNING", "PRACTICING", "ASSESSMENT_READY"]]
            if learning_chapters:
                latest = sorted(learning_chapters, key=lambda x: x.get('lastAccessed', ''), reverse=True)[0]
                tasks.append({
                    "type": "LEARN",
                    "chapterId": latest['chapterId'],
                    "label": "Continue Journey",
                    "description": f"Move forward in your current chapter.",
                    "priority": "MEDIUM",
                    "status": "COMPLETED" if is_done("LEARN", chapter_id=latest['chapterId']) else "PENDING"
                })

            # 4. Final Mastery Check (Priority 4)
            ready_chapters = [r for r in student_mastery if r.get("status") == "ASSESSMENT_READY"]
            if ready_chapters:
                tasks.append({
                    "type": "MASTERY_CHECK",
                    "chapterId": ready_chapters[0]['chapterId'],
                    "label": "Final Milestone",
                    "description": "Complete the final check to master this chapter.",
                    "priority": "MEDIUM",
                    "status": "COMPLETED" if is_done("MASTERY_CHECK", chapter_id=ready_chapters[0]['chapterId']) else "PENDING"
                })

        # Final balancing: Return top 4 tasks
        balanced_tasks = tasks[:4]

        return {
            "date": "Today",
            "tasks": balanced_tasks,
            "estimated_time": f"{len([t for t in balanced_tasks if t['status'] == 'PENDING']) * 10} mins"
        }

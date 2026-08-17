from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.srs import SRSItem, SRSReview, ErrorEvent
from ..config.app_config import settings
from .retention_policy import RetentionPolicy
import logging

logger = logging.getLogger(__name__)

class SRSService:
    def __init__(self, session_factory):
        self.AsyncSession = session_factory

    async def get_due_items(self, student_id: str, content_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch items that are due for review."""
        async with self.AsyncSession() as session:
            now = datetime.now(timezone.utc).replace(tzinfo=None)

            filters = [
                SRSItem.student_id == student_id,
                SRSItem.next_review <= now
            ]
            if content_type:
                filters.append(SRSItem.content_type == content_type)

            stmt = select(SRSItem).where(and_(*filters)).order_by(SRSItem.next_review.asc()).limit(limit)

            res = await session.execute(stmt)
            items = res.scalars().all()

            # Review Coordination (SHADOW): Identify overlaps
            if settings.ADAPTIVE_MASTERY_REVIEW_COORDINATION != "OFF":
                await self._identify_review_overlaps(student_id, items)

            return [i.to_dict() for i in items]

    async def record_error(self,
                           student_id: str,
                           question_id: str,
                           concept_id: str,
                           error_type: str,
                           chapter_id: str,
                           attempt_id: Optional[str] = None):
        """Records a classified error event."""
        if settings.ADAPTIVE_MASTERY_ERROR_ANALYSIS == "OFF":
            return None

        async with self.AsyncSession() as session:
            event = ErrorEvent(
                student_id=student_id,
                question_id=question_id,
                concept_id=concept_id,
                error_type=error_type,
                chapter_id=chapter_id,
                attempt_id=attempt_id
            )
            session.add(event)
            await session.commit()
            logger.info(f"Recorded {error_type} error for student {student_id} on {concept_id}")
            return {"status": "SUCCESS"}

    async def _identify_review_overlaps(self, student_id: str, items: List[SRSItem]):
        """Detects if chapter and concept reviews for the same chapter are due."""
        chapter_ids = {i.content_id for i in items if i.content_type == 'chapter'}
        concept_items = [i for i in items if i.content_type == 'concept']

        overlaps = []
        for c_item in concept_items:
            # Concept GUID contains chapterId as per P0-A/B
            # class_6_math_fegp101_c1
            chap_ref = c_item.metadata_json.get("chapterId") if c_item.metadata_json else None
            if chap_ref in chapter_ids:
                overlaps.append(f"Overlap: Concept {c_item.content_id} and Chapter {chap_ref} both due.")

        if overlaps:
            logger.info(f"SRS Coordination (SHADOW) for {student_id}: {overlaps}")

    async def ensure_concept_tracked(self, student_id: str, concept_id: str, chapter_id: str):
        """Initializes an SRS tracking record for a concept if it doesn't exist."""
        item_id = f"{student_id}_{concept_id}"

        async with self.AsyncSession() as session:
            stmt = select(SRSItem).where(SRSItem.id == item_id)
            res = await session.execute(stmt)
            if res.scalars().first():
                return

            now = datetime.now(timezone.utc).replace(tzinfo=None)
            item = SRSItem(
                id=item_id,
                student_id=student_id,
                content_id=concept_id,
                content_type='concept',
                next_review=now,
                metadata_json={"chapterId": chapter_id}
            )
            session.add(item)
            await session.commit()
            logger.info(f"Started SRS tracking for concept {concept_id} for student {student_id}")

    async def record_review(self, student_id: str, content_id: str, content_type: str, rating: int):
        """
        Apply SM-2 algorithm based on student rating.
        Ratings: 1 (Again), 2 (Hard), 3 (Good), 4 (Easy)
        """
        is_off = settings.ADAPTIVE_MASTERY_CONCEPT_SRS == "OFF"
        if content_type == 'concept' and is_off:
            return None

        item_id = f"{student_id}_{content_id}"

        async with self.AsyncSession() as session:
            stmt = select(SRSItem).where(SRSItem.id == item_id)
            res = await session.execute(stmt)
            item = res.scalars().first()

            now = datetime.now(timezone.utc).replace(tzinfo=None)

            if not item:
                # Create new item if not exists
                item = SRSItem(
                    id=item_id,
                    student_id=student_id,
                    content_id=content_id,
                    content_type=content_type,
                    next_review=now,
                    repetitions=0,
                    easiness_factor=2.5,
                    interval=0
                )
                session.add(item)

            old_interval = item.interval

            # Use centralized policy
            result = RetentionPolicy.calculate_next_review(
                rating, item.repetitions, item.easiness_factor, item.interval
            )

            item.repetitions = result["repetitions"]
            item.interval = result["interval"]
            item.easiness_factor = result["easiness_factor"]
            item.last_reviewed = now
            item.next_review = now + result["next_review_delta"]

            # Log the review
            review = SRSReview(
                item_id=item_id,
                rating=rating,
                old_interval=old_interval,
                new_interval=item.interval
            )
            session.add(review)
            await session.commit()

            return item.to_dict()

    async def get_memory_stats(self, student_id: str) -> Dict[str, Any]:
        """Aggregate stats about the student's memory profile."""
        async with self.AsyncSession() as session:
            stmt = select(SRSItem).where(SRSItem.student_id == student_id)
            res = await session.execute(stmt)
            items = res.scalars().all()

            total = len(items)
            now = datetime.now(timezone.utc).replace(tzinfo=None)
            due = len([i for i in items if i.next_review <= now])
            mastered = len([i for i in items if i.repetitions > 5 and i.easiness_factor > 2.0])

            return {
                "total_tracked": total,
                "due_count": due,
                "mastered_count": mastered,
                "average_ef": sum(i.easiness_factor for i in items) / total if total > 0 else 0,
                "stability_profile": self._calculate_stability_profile(items)
            }

    def _calculate_stability_profile(self, items: List[SRSItem]) -> Dict[str, int]:
        profile = {"NEW": 0, "FRAGILE": 0, "STABILIZING": 0, "STABLE": 0}
        for item in items:
            stability = RetentionPolicy.get_retention_stability(item.repetitions, item.easiness_factor)
            profile[stability] += 1
        return profile

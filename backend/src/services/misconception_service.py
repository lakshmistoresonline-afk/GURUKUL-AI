import logging
from typing import Dict, Any, List, Optional
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.learning import MisconceptionRecord, MisconceptionStatus
from ..models.srs import ErrorEvent

logger = logging.getLogger(__name__)

class ErrorTaxonomy:
    CONCEPT_MISUNDERSTANDING = "CONCEPT_MISUNDERSTANDING"
    PROCEDURE_ERROR = "PROCEDURE_ERROR"
    CALCULATION_ERROR = "CALCULATION_ERROR"
    READING_ERROR = "READING_ERROR"
    UNIT_ERROR = "UNIT_ERROR"
    SIGN_ERROR = "SIGN_ERROR"
    RULE_CONFUSION = "RULE_CONFUSION"
    VOCABULARY_ERROR = "VOCABULARY_ERROR"
    INFERENCE_ERROR = "INFERENCE_ERROR"
    CARELESS_ERROR = "CARELESS_ERROR"
    PARTIAL_UNDERSTANDING = "PARTIAL_UNDERSTANDING"
    TRANSFER_FAILURE = "TRANSFER_FAILURE"
    RECALL_FAILURE = "RECALL_FAILURE"
    PREREQUISITE_GAP = "PREREQUISITE_GAP"
    OVERCONFIDENT_ERROR = "OVERCONFIDENT_ERROR"
    LOW_CONFIDENCE_CORRECT = "LOW_CONFIDENCE_CORRECT"

class MisconceptionService:
    def __init__(self, session_factory):
        self.AsyncSession = session_factory

    async def detect_misconceptions(self, student_id: str, concept_id: str) -> Optional[Dict[str, Any]]:
        """
        Analyzes error history for patterns to identify LIKELY_MISCONCEPTIONS.
        """
        async with self.AsyncSession() as session:
            # 1. Fetch recent errors for this concept
            stmt = select(ErrorEvent).where(
                and_(ErrorEvent.student_id == student_id, ErrorEvent.concept_id == concept_id)
            ).order_by(ErrorEvent.created_at.desc()).limit(10)

            res = await session.execute(stmt)
            errors = res.scalars().all()

            if len(errors) < 2:
                return None

            # 2. Pattern Recognition
            types = [e.error_type for e in errors]

            # If 2 consecutive errors are the same type, it's a suspected misconception
            if len(types) >= 2 and types[0] == types[1]:
                return await self._ensure_misconception_record(session, student_id, concept_id, f"LIKELY_{types[0]}")

            # Threshold based
            for t in set(types):
                if types.count(t) >= 3:
                    return await self._ensure_misconception_record(session, student_id, concept_id, f"PERSISTENT_{t}")

        return None

    async def _ensure_misconception_record(self, session: AsyncSession, student_id: str, concept_id: str, m_type: str):
        stmt = select(MisconceptionRecord).where(
            and_(
                MisconceptionRecord.student_id == student_id,
                MisconceptionRecord.concept_id == concept_id,
                MisconceptionRecord.status != MisconceptionStatus.RESOLVED
            )
        )
        res = await session.execute(stmt)
        record = res.scalars().first()

        if not record:
            record = MisconceptionRecord(
                student_id=student_id,
                concept_id=concept_id,
                misconception_type=m_type
            )
            session.add(record)
        else:
            record.evidence_count += 1
            record.last_detected_at = datetime.utcnow()

        await session.commit()
        return {"id": record.id, "type": m_type, "status": record.status.value}

import logging
import random
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from .mastery_service import MasteryService
from .srs_service import SRSService
from .adaptation_service import AdaptationService
from ..config.app_config import settings

logger = logging.getLogger(__name__)

class ActionType:
    LEARN_CONCEPT = "LEARN_CONCEPT"
    REVIEW_CONCEPT = "REVIEW_CONCEPT"
    PRACTICE_CONCEPT = "PRACTICE_CONCEPT"
    REMEDIATE_CONCEPT = "REMEDIATE_CONCEPT"
    REPAIR_PREREQUISITE = "REPAIR_PREREQUISITE"
    ANALYZE_ERROR = "ANALYZE_ERROR"
    TRANSFER_CONCEPT = "TRANSFER_CONCEPT"
    TEACH_CONCEPT = "TEACH_CONCEPT"
    RETENTION_REVIEW = "RETENTION_REVIEW"
    CONTINUE_CHAPTER = "CONTINUE_CHAPTER"
    RESOLVE_MISCONCEPTION = "RESOLVE_MISCONCEPTION"

class LearningPathService:
    def __init__(self,
                 mastery_service: MasteryService,
                 srs_service: SRSService,
                 adaptation_service: AdaptationService):
        self.mastery_service = mastery_service
        self.srs_service = srs_service
        self.adaptation_service = adaptation_service

    async def get_best_next_action(self, student_id: str, class_name: str, subject: str, chapter_id: str, student_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines the single most effective next step for the student.
        """
        # 0. Subject-Aware Weights
        subject = subject.lower()
        is_math = subject == "mathematics"
        is_lang = subject in ["english", "hindi"]
        is_evs = subject == "evs"

        # 1. Check for Active Misconceptions (Priority 1)
        async with self.srs_service.AsyncSession() as session:
            from ..models.learning import MisconceptionRecord, MisconceptionStatus
            from sqlalchemy import select, and_
            stmt = select(MisconceptionRecord).where(
                and_(
                    MisconceptionRecord.student_id == student_id,
                    MisconceptionRecord.status == MisconceptionStatus.CONFIRMED
                )
            ).limit(1)
            res = await session.execute(stmt)
            m_record = res.scalars().first()
            if m_record:
                return {
                    "action": ActionType.RESOLVE_MISCONCEPTION,
                    "target_id": m_record.concept_id,
                    "reason": "We've noticed a pattern in your answers. Let's look at this from a different angle.",
                    "context": "REMEDIATION"
                }

        # 2. Check for critical retention (SRS)
        due_items = await self.srs_service.get_due_items(student_id, content_type='concept', limit=1)
        if due_items:
            return {
                "action": ActionType.RETENTION_REVIEW,
                "target_id": due_items[0]['content_id'],
                "reason": "It's time to refresh your memory on this concept.",
                "context": "RETENTION"
            }

        # 2. Check current mastery state
        config = self.mastery_service.get_chapter_mastery_config(class_name, subject, chapter_id)
        if not config:
            return {"action": ActionType.CONTINUE_CHAPTER, "reason": "Continue your journey."}

        state = self.mastery_service.calculate_mastery_state(student_record, config)

        # 3. Handle Remediation Priority
        if state.get("remediation_needed"):
            weak_cid = state["remediation_needed"][0]
            # Check for prerequisite gaps in the graph
            gaps = self.adaptation_service.get_upstream_gaps(student_record, f"{class_name}_{weak_cid}")
            if gaps:
                return {
                    "action": ActionType.REPAIR_PREREQUISITE,
                    "target_id": gaps[0],
                    "reason": "Before moving forward, let's bridge a small gap from an earlier topic.",
                    "context": "PREREQUISITE"
                }

            return {
                "action": ActionType.REMEDIATE_CONCEPT,
                "target_id": weak_cid,
                "reason": "Let's strengthen your understanding of this core idea.",
                "context": "REMEDIATION"
            }

        # 4. Progression Logic (Understand -> Apply -> Analyze -> Transfer -> Teach)
        perf = student_record.get("conceptPerformance", {})
        concepts = config.get("concepts") or config.get("mappings") or []

        if not concepts:
            return {
                "action": ActionType.EXPLORE_LIBRARY,
                "target_id": "",
                "reason": "Explore the curriculum to start your journey.",
                "context": "INITIAL"
            }

        for concept in concepts:
            c_id = concept.get("conceptId") or concept.get("id")
            if not c_id: continue

            c_perf = perf.get(c_id, {})

            # Foundation check
            if c_perf.get("foundation", 0) < 0.7:
                return {
                    "action": ActionType.LEARN_CONCEPT,
                    "target_id": c_id,
                    "reason": "Let's start by understanding this new concept.",
                    "context": "LEARNING"
                }

            # Application check
            if c_perf.get("application", 0) < 0.6:
                return {
                    "action": ActionType.PRACTICE_CONCEPT,
                    "target_id": c_id,
                    "reason": "You've got the basics! Now let's try applying it.",
                    "context": "PRACTICE"
                }

        # 5. Advanced Competencies (If all concepts have basic application)
        if not state["evidence"]["analyze"]:
            target_id = concepts[0].get("conceptId") or concepts[0].get("id")
            return {
                "action": ActionType.ANALYZE_ERROR if random.random() > 0.5 else ActionType.PRACTICE_CONCEPT,
                "target_id": target_id, # Pick first or weakest
                "reason": "Time for a deeper challenge. Let's look at some complex cases.",
                "context": "ANALYSIS"
            }

        if not state["evidence"]["transfer"]:
            idx = random.randint(0, len(concepts)-1)
            target_id = concepts[idx].get("conceptId") or concepts[idx].get("id")
            return {
                "action": ActionType.TRANSFER_CONCEPT,
                "target_id": target_id,
                "reason": "Can you use this knowledge in a completely new way?",
                "context": "TRANSFER"
            }

        if not state["evidence"]["teach"]:
            target_id = concepts[0].get("conceptId") or concepts[0].get("id")
            return {
                "action": ActionType.TEACH_CONCEPT,
                "target_id": target_id,
                "reason": "Final boss! Can you explain this so well that someone else could learn it?",
                "context": "TEACH"
            }

        return {
            "action": ActionType.CONTINUE_CHAPTER,
            "reason": "You have mastered this chapter! Ready for the next one?",
            "context": "COMPLETED"
        }

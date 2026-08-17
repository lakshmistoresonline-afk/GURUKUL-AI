import logging
from typing import Dict, Any, List, Optional
from .mastery_service import MasteryService
from .srs_service import SRSService
from .adaptation_service import AdaptationService
from .learning_path_service import LearningPathService, ActionType
from .misconception_service import MisconceptionService
from .question_bank_service import QuestionBankService

logger = logging.getLogger(__name__)

class MasteryOrchestrator:
    def __init__(self,
                 mastery_service: MasteryService,
                 srs_service: SRSService,
                 adaptation_service: AdaptationService,
                 question_bank_service: QuestionBankService):
        self.mastery_service = mastery_service
        self.srs_service = srs_service
        self.adaptation_service = adaptation_service
        self.question_bank_service = question_bank_service

        self.learning_path_service = LearningPathService(
            mastery_service, srs_service, adaptation_service
        )
        self.misconception_service = MisconceptionService(srs_service.AsyncSession)

    async def get_next_step(self, student_id: str, class_name: str, subject: str, chapter_id: str, student_record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Public API for the adaptive engine to suggest the next activity.
        """
        action = await self.learning_path_service.get_best_next_action(
            student_id, class_name, subject, chapter_id, student_record
        )

        # Enrich action with specific content if needed
        if action["action"] in [ActionType.PRACTICE_CONCEPT, ActionType.REMEDIATE_CONCEPT]:
            levels = ["foundation"] if action["context"] == "REMEDIATION" else ["application"]
            questions = self.mastery_service.get_questions_for_concept(
                class_name, subject, chapter_id, action["target_id"], limit=3, levels=levels
            )
            action["questions"] = questions

            # Check for worked examples in the package
            config = self.mastery_service.get_chapter_mastery_config(class_name, subject, chapter_id)
            if config:
                concepts = config.get("concepts") or config.get("mappings") or []
                # Resilience: Support both 'conceptId' and 'id'
                target_id = action.get("target_id")
                target_concept = next(
                    (c for c in concepts if (c.get("conceptId") == target_id or c.get("id") == target_id)),
                    None
                )
                if target_concept and target_concept.get("examples"):
                    action["worked_example"] = target_concept["examples"][0]

        elif action["action"] == ActionType.TRANSFER_CONCEPT:
            questions = self.mastery_service.get_questions_for_concept(
                class_name, subject, chapter_id, action["target_id"], limit=2, levels=["challenge", "hots"]
            )
            action["questions"] = questions

        return action

    async def process_activity_result(self, student_id: str, activity_type: str, result_data: Dict[str, Any]):
        """
        Records the outcome of a recommended action and updates states.
        """
        # 1. Check for misconceptions on failure
        if result_data.get("is_failed"):
            await self.misconception_service.detect_misconceptions(
                student_id, result_data.get("concept_id")
            )

        # 2. Handle Retention Review Success
        if activity_type == ActionType.RETENTION_REVIEW and not result_data.get("is_failed"):
            # Mark concept as verified for stability
            # This would typically trigger a flag update in the student_record (Firestore)
            # The frontend should call progressService.updateStatus or similar
            pass

        # 3. Log activity for plan optimization
        async with self.srs_service.AsyncSession() as session:
            from ..models.learning import LearningActivity
            activity = LearningActivity(
                student_id=student_id,
                activity_type=activity_type,
                concept_id=result_data.get("concept_id"),
                chapter_id=result_data.get("chapter_id"),
                status="COMPLETED" if not result_data.get("is_failed") else "FAILED",
                score=result_data.get("score")
            )
            session.add(activity)
            await session.commit()

        return {"status": "SUCCESS", "retention_stability": "STABLE" if activity_type == ActionType.RETENTION_REVIEW and not result_data.get("is_failed") else None}

    async def process_feynman_result(self, student_id: str, class_name: str, subject: str, chapter_id: str, concept_name: str, score: int):
        """
        Processes a Feynman evaluation and updates the 'Teach' pillar.
        """
        config = self.mastery_service.get_chapter_mastery_config(class_name, subject, chapter_id)
        if not config: return

        concepts = config.get("concepts") or config.get("mappings") or []
        target_concept = next(
            (c for c in concepts if (c.get("conceptName", "").lower() == concept_name.lower() or c.get("concept", "").lower() == concept_name.lower())),
            None
        )
        if not target_concept: return

        c_id = target_concept.get("conceptId") or target_concept.get("id")

        return {
            "concept_id": c_id,
            "pillar": "TEACH",
            "score": score,
            "status": "PASS" if score >= 70 else "FAIL"
        }

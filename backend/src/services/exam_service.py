import logging
import uuid
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.assessment import ExamSession, QuestionPaper
from ..orchestrator.ai_orchestrator import AIOrchestrator

logger = logging.getLogger(__name__)

class ExamService:
    def __init__(self, db_session: AsyncSession, orchestrator: AIOrchestrator):
        self.db = db_session
        self.orchestrator = orchestrator

    async def start_session(self, student_id: str, paper_id: str) -> ExamSession:
        session = ExamSession(
            id=str(uuid.uuid4()),
            student_id=student_id,
            paper_id=paper_id,
            status="STARTED",
            started_at=datetime.utcnow()
        )
        self.db.add(session)
        await self.db.commit()
        return session

    async def submit_exam(self, session_id: str, responses: List[Dict[str, Any]]) -> ExamSession:
        result = await self.db.execute(select(ExamSession).where(ExamSession.id == session_id))
        session = result.scalar_one_or_none()

        if not session:
            raise ValueError("Session not found")

        session.responses_json = responses
        session.status = "SUBMITTED"
        session.completed_at = datetime.utcnow()

        await self.db.commit()
        return session

    async def evaluate_session(self, session_id: str) -> ExamSession:
        """Uses AI to evaluate the student's responses."""
        result = await self.db.execute(
            select(ExamSession, QuestionPaper).join(QuestionPaper).where(ExamSession.id == session_id)
        )
        data = result.one_or_none()
        if not data:
            raise ValueError("Session or Paper not found")

        session, paper = data
        responses = session.responses_json
        questions = paper.questions_json

        evaluation = []
        total_score = 0.0

        for resp in responses:
            q_id = resp.get("question_id")
            student_answer = resp.get("answer")

            # Find matching question in paper
            question = next((q for q in questions if q.get("id") == q_id), None)
            if not question: continue

            # AI Evaluation for subjective or complex answers
            eval_result = await self._ai_evaluate(question, student_answer)
            evaluation.append({
                "question_id": q_id,
                "score": eval_result.get("score", 0),
                "feedback": eval_result.get("feedback", ""),
                "correct_answer": question.get("correctAnswer")
            })
            total_score += eval_result.get("score", 0)

        session.evaluation_json = evaluation
        session.score = total_score
        session.status = "EVALUATED"

        await self.db.commit()
        return session

    async def _ai_evaluate(self, question: Dict[str, Any], student_answer: str) -> Dict[str, Any]:
        prompt = f"""
        Evaluate the following student answer for the given question.
        Question: {question.get('question')}
        Correct Answer/Model Answer: {question.get('correctAnswer')}
        Student Answer: {student_answer}

        Provide a score from 0 to {question.get('marks', 2)} and constructive feedback.
        Return in JSON: {{"score": float, "feedback": "string"}}
        """
        response = await self.orchestrator.request_structured_response(prompt, "EVALUATION")
        return response

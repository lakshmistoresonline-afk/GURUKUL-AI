import logging
import uuid
import random
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.assessment import QuestionPaper, PaperType
from .question_bank_service import QuestionBankService

logger = logging.getLogger(__name__)

class QuestionCenterService:
    def __init__(self, db_session: AsyncSession, question_bank: QuestionBankService):
        self.db = db_session
        self.bank = question_bank

    async def get_available_papers(self, class_level: int, subject: Optional[str] = None) -> List[QuestionPaper]:
        query = select(QuestionPaper).where(QuestionPaper.class_level == class_level)
        if subject:
            query = query.where(QuestionPaper.subject == subject)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def generate_model_paper(self,
                                   class_level: int,
                                   subject: str,
                                   paper_type: PaperType = PaperType.MODEL) -> QuestionPaper:
        """Generates a model paper by selecting questions from the bank."""
        title = f"Model Paper: {subject} Class {class_level}"

        # Select questions (mix of easy, medium, hard)
        easy = self.bank.get_questions(class_id=class_level, subject=subject, difficulty="easy", limit=10)
        medium = self.bank.get_questions(class_id=class_level, subject=subject, difficulty="medium", limit=15)
        hard = self.bank.get_questions(class_id=class_level, subject=subject, difficulty="hard", limit=5)

        all_qs = easy + medium + hard
        random.shuffle(all_qs)

        paper = QuestionPaper(
            id=str(uuid.uuid4()),
            title=title,
            subject=subject,
            class_level=class_level,
            paper_type=paper_type,
            total_marks=sum([int(q.get('marks', 2)) for q in all_qs]),
            duration_minutes=180 if paper_type == PaperType.ANNUAL else 90,
            questions_json=all_qs,
            created_at=datetime.utcnow()
        )

        self.db.add(paper)
        await self.db.commit()
        return paper

    async def get_paper_by_id(self, paper_id: str) -> Optional[QuestionPaper]:
        result = await self.db.execute(select(QuestionPaper).where(QuestionPaper.id == paper_id))
        return result.scalar_one_or_none()

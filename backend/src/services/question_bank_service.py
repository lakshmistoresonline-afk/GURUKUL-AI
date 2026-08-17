import os
import json
import random
import logging
from typing import List, Dict, Any, Optional

from ..config.app_config import settings

logger = logging.getLogger(__name__)

class QuestionBankService:
    def __init__(self, master_path: Optional[str] = None):
        self.master_path = master_path or os.path.join(settings.PROJECT_ROOT, "Question Bank", "QUESTION_BANK_MASTER.json")
        self.questions: List[Dict[str, Any]] = []
        self.chapter_index: Dict[str, List[int]] = {}
        self.concept_index: Dict[str, List[int]] = {}
        self.title_map = self._load_json(os.path.join(settings.STORAGE_PATH, "chapter_title_map.json"))
        self._load_bank()

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            logger.error(f"File not found: {path}")
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON from {path}: {e}")
            return {}

    def _load_bank(self):
        data = self._load_json(self.master_path)
        self.questions = data.get("questions", [])

        if not self.questions:
            logger.warning(f"QuestionBankService: Global bank at {self.master_path} is empty or missing.")

        # Build indexes for fast filtering
        for idx, q in enumerate(self.questions):
            # Resolve canonical Chapter ID (eesa101 etc)
            canonical_id = q.get("chapterId")

            # Try to resolve via title map if chapterId is missing
            if not canonical_id:
                chap_title = str(q.get("chapterTitle", "")).lower()
                if chap_title in self.title_map:
                    canonical_id = self.title_map[chap_title]["id"]

            if canonical_id:
                if canonical_id not in self.chapter_index:
                    self.chapter_index[canonical_id] = []
                self.chapter_index[canonical_id].append(idx)

            # Concept Index
            concept_id = str(q.get("conceptId", ""))
            if concept_id:
                if concept_id not in self.concept_index:
                    self.concept_index[concept_id] = []
                self.concept_index[concept_id].append(idx)

        logger.info(f"QuestionBankService: Initialized with {len(self.questions)} questions. {len(self.chapter_index)} chapters indexed.")

    def get_questions(self,
                      class_id: Optional[int] = None,
                      subject: Optional[str] = None,
                      chapter_id: Optional[str] = None,
                      concept_id: Optional[str] = None,
                      difficulty: Optional[str] = None,
                      q_type: Optional[str] = None,
                      limit: int = 10,
                      randomize: bool = True) -> List[Dict[str, Any]]:

        indices = []
        if concept_id:
            indices = self.concept_index.get(concept_id, [])
        elif chapter_id:
            indices = self.chapter_index.get(chapter_id, [])
        else:
            indices = range(len(self.questions))

        pool = [self.questions[i] for i in indices]

        # Filtering
        if class_id is not None:
            pool = [q for q in pool if q.get("class") == class_id]
        if subject:
            pool = [q for q in pool if q.get("subject", "").lower() == subject.lower()]
        if difficulty:
            pool = [q for q in pool if q.get("difficulty", "").lower() == difficulty.lower()]
        if q_type:
            pool = [q for q in pool if q.get("type", "").lower() == q_type.lower()]

        if randomize:
            random.shuffle(pool)

        return [self._normalize_question(q) for q in pool[:limit]]

    def _normalize_question(self, q: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes question for frontend compatibility."""
        q_copy = q.copy()

        raw_type = str(q.get("type", "mcq")).lower()
        q_type = raw_type.replace("-", "_")
        if q_type == "fill_blank": q_type = "fill_blanks"
        q_copy["type"] = q_type

        diff = str(q.get("difficulty", "medium")).capitalize()
        q_copy["difficulty"] = diff

        options = q.get("options", []) or []
        answer = str(q.get("answer", ""))

        if q_type == "mcq" and answer in ["A", "B", "C", "D"]:
            idx = ord(answer) - ord("A")
            if idx < len(options):
                q_copy["correctAnswer"] = options[idx]
        else:
            q_copy["correctAnswer"] = answer

        return q_copy

    def get_practice_session(self, chapter_id: str, count: int = 10, difficulty_mix: Dict[str, float] = None) -> List[Dict[str, Any]]:
        if not difficulty_mix:
            difficulty_mix = {"easy": 0.3, "medium": 0.5, "hard": 0.2}

        session = []
        for diff, ratio in difficulty_mix.items():
            limit = max(1, int(count * ratio))
            session.extend(self.get_questions(chapter_id=chapter_id, difficulty=diff, limit=limit))

        if len(session) < count:
            existing_ids = {q["id"] for q in session}
            remaining = self.get_questions(chapter_id=chapter_id, limit=count*2)
            for q in remaining:
                if q["id"] not in existing_ids:
                    session.append(q)
                    if len(session) >= count: break

        random.shuffle(session)
        return session[:count]

    def get_remediation_session(self, concept_id: str, count: int = 5) -> List[Dict[str, Any]]:
        indices = self.concept_index.get(concept_id, [])
        pool = [self.questions[i] for i in indices]
        remediation_pool = [q for q in pool if q.get("type", "").lower() in ["remediation", "error_analysis"]]
        if len(remediation_pool) < count:
            foundation = [q for q in pool if q.get("difficulty", "").lower() == "easy"]
            remediation_pool.extend(foundation)
        random.shuffle(remediation_pool)
        return [self._normalize_question(q) for q in remediation_pool[:count]]

    def get_stats(self) -> Dict[str, Any]:
        class_counts = {}
        for q in self.questions:
            c = str(q.get("class"))
            class_counts[c] = class_counts.get(c, 0) + 1

        return {
            "total_questions": len(self.questions),
            "chapters_covered": len(self.chapter_index),
            "concepts_covered": len(self.concept_index),
            "class_counts": class_counts
        }

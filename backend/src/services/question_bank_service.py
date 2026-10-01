import os
import json
import random
import logging
from typing import List, Dict, Any, Optional

try:
    from config.app_config import settings
except ImportError:
    try:
        from ..config.app_config import settings
    except ImportError:
        from backend.src.config.app_config import settings

logger = logging.getLogger(__name__)

class QuestionBankService:
    def __init__(self):
        self.questions: List[Dict[str, Any]] = []
        self.chapter_index: Dict[str, List[int]] = {}
        self.concept_index: Dict[str, List[int]] = {}
        self.title_map = self._load_json(settings.CHAPTER_TITLE_MAP_PATH)
        self._load_bank()

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON from {path}: {e}")
            return {}

    def _load_bank(self):
        processed_root = settings.MASTER_CONTENT_ROOT
        if os.path.exists(processed_root):
            for grade_dir in os.listdir(processed_root):
                g_path = os.path.join(processed_root, grade_dir)
                if not os.path.isdir(g_path):
                    continue
                for subj_dir in os.listdir(g_path):
                    s_path = os.path.join(g_path, subj_dir)
                    if not os.path.isdir(s_path):
                        continue
                    for ch_id in os.listdir(s_path):
                        ch_dir = os.path.join(s_path, ch_id)
                        qp_path = os.path.join(ch_dir, "question_papers.json")
                        if os.path.exists(qp_path):
                            qp_data = self._load_json(qp_path)
                            papers = qp_data.get("question_papers", []) or []
                            for p in papers:
                                for sec in p.get("sections", []):
                                    for q in sec.get("questions", []):
                                        q_item = {
                                            "class": int(grade_dir.replace("Class", "")),
                                            "subject": subj_dir,
                                            "chapterId": ch_id,
                                            "chapterTitle": p.get("paper_title", ch_id),
                                            "type": "mcq",
                                            "question": q.get("question_text") or q.get("question", ""),
                                            "options": q.get("options", []),
                                            "answer": q.get("correct_answer") or q.get("answer", "")
                                        }
                                        self.questions.append(q_item)

        qb_root = settings.QUESTION_BANK_SOURCE_ROOT
        if os.path.exists(qb_root):
            for root, dirs, files in os.walk(qb_root):
                for file in files:
                    if file.endswith(".json"):
                        fpath = os.path.join(root, file)
                        try:
                            data = self._load_json(fpath)
                            items = data.get("items", []) or data.get("chapters", []) or [data]
                            if isinstance(items, list):
                                for it in items:
                                    if not isinstance(it, dict):
                                        continue
                                    sub_items = it.get("items", []) or [it]
                                    for q in sub_items:
                                        if not isinstance(q, dict):
                                            continue
                                        q_text = q.get("question_text") or q.get("question") or q.get("statement") or ""
                                        if q_text:
                                            self.questions.append({
                                                "class": 7,
                                                "subject": "General",
                                                "chapterId": "QB-SOURCE",
                                                "chapterTitle": it.get("chapter_title", "Question Bank Item"),
                                                "type": q.get("type", "mcq"),
                                                "question": q_text,
                                                "options": q.get("options", []),
                                                "answer": q.get("correct_answer") or q.get("answer", "")
                                            })
                        except Exception:
                            pass

        for i, q in enumerate(self.questions):
            cid = q.get("chapterId")
            if cid:
                if cid not in self.chapter_index:
                    self.chapter_index[cid] = []
                self.chapter_index[cid].append(i)

        logger.info(f"QuestionBankService: Loaded {len(self.questions)} questions total.")

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
        if chapter_id:
            indices = self.chapter_index.get(chapter_id, [])
        else:
            indices = range(len(self.questions))

        pool = [self.questions[i] for i in indices]

        if class_id is not None:
            pool = [q for q in pool if q.get("class") == class_id]
        if subject:
            pool = [q for q in pool if q.get("subject", "").lower() == subject.lower()]
        if q_type:
            pool = [q for q in pool if q.get("type", "").lower() == q_type.lower()]

        if randomize:
            random.shuffle(pool)

        return [self._normalize_question(q) for q in pool[:limit]]

    def _normalize_question(self, q: Dict[str, Any]) -> Dict[str, Any]:
        q_copy = q.copy()
        raw_type = str(q.get("type", "mcq")).lower()
        q_type = raw_type.replace("-", "_")
        q_copy["type"] = q_type
        q_copy["difficulty"] = "Medium"
        q_copy["correctAnswer"] = str(q.get("answer", ""))
        return q_copy

    def get_practice_session(self, chapter_id: str, count: int = 10, difficulty_mix: Dict[str, float] = None) -> List[Dict[str, Any]]:
        pool = self.get_questions(chapter_id=chapter_id, limit=count, randomize=True)
        return pool

    def get_remediation_session(self, concept_id: str, count: int = 5) -> List[Dict[str, Any]]:
        return self.get_questions(limit=count)

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_questions": len(self.questions),
            "chapters_covered": len(self.chapter_index),
            "class_counts": {str(len(self.questions))}
        }

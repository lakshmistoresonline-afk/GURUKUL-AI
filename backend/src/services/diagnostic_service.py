import os
import json
import random
import logging
from typing import Dict, Any, List, Optional
from .mastery_service import MasteryService

from ..config.app_config import settings

logger = logging.getLogger(__name__)

class DiagnosticService:
    def __init__(self, mastery_service: MasteryService):
        self.mastery_service = mastery_service
        self.graph = self._load_json(os.path.join(settings.STORAGE_PATH, "concept_graph.json"))
        self.title_map = self._load_json(os.path.join(settings.STORAGE_PATH, "chapter_title_map.json"))

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path): return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"DiagnosticService: Error loading {path}: {e}")
            return {}

    def get_diagnostic_questions(self, class_name: str, subject: str, chapter_id: str) -> List[Dict[str, Any]]:
        """
        Selects 5-10 existing questions for a pre-chapter diagnostic.
        """
        # Resolve current chapter config from mastery service
        config = self.mastery_service.get_chapter_mastery_config(class_name, subject, chapter_id)
        if not config or "source" not in config: return []

        # Use canonical chapter identifier for question lookups
        chapter_title = config.get("source", {}).get("chapterTitle", "")
        if not chapter_title: return []

        # Load the full question bank for the current chapter
        curr_pkg = self._load_package_by_title(chapter_title)
        if not curr_pkg: return []

        # 1. Identify Related Chapters (Upstream Probes)
        related_chaps = []
        for rel in self.graph.get("chapterRelationships", []):
            if rel["toChapter"] == chapter_title:
                related_chaps.append(rel["fromChapter"])
            elif rel["fromChapter"] == chapter_title:
                related_chaps.append(rel["toChapter"])

        prereq_probes = []
        for r_title in list(set(related_chaps)):
            r_pkg = self._load_package_by_title(r_title)
            r_config = self.mastery_service.get_chapter_mastery_config(class_name, subject, r_title)
            if r_pkg and r_config:
                r_canonical_id = r_config['source'].get('slug') or r_config['source'].get('chapterTitle')
                q = self._pick_from_bank(r_pkg, "foundation", 1)
                if q: prereq_probes.extend([{**item, "is_prereq": True, "chapter_ref": r_canonical_id} for item in q])

        # 2. Core Chapter Concepts (Foundation)
        curr_foundation = [{**item, "chapter_ref": canonical_chapter_id} for item in self._pick_from_bank(curr_pkg, "foundation", 6)]

        # 3. Misconception/HOTS Probes
        curr_hots = [{**item, "chapter_ref": canonical_chapter_id} for item in self._pick_from_bank(curr_pkg, ["mastery", "challenge", "hots", "application"], 4)]

        # Assemble
        final_selection = []
        if prereq_probes:
            final_selection.extend(random.sample(prereq_probes, min(len(prereq_probes), 3)))
        final_selection.extend(curr_foundation)
        final_selection.extend(curr_hots)

        random.shuffle(final_selection)

        unique_selection = []
        seen_ids = set()
        for q in final_selection:
            if q["id"] not in seen_ids:
                formatted = self._format_q(q, class_name, q.get("chapter_ref", chapter_id))
                # Only include questions with valid concept mapping
                if formatted.get("concept_id"):
                    unique_selection.append(formatted)
                    seen_ids.add(q["id"])

        return unique_selection[:10]

    def _load_package_by_title(self, title: str) -> Optional[Dict[str, Any]]:
        info = self.title_map.get(title.lower())
        if not info: return None
        path = os.path.join(settings.STORAGE_PATH, "output", info['class'], info['subject'], info['id'], "package.json")
        if not os.path.exists(path): return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _pick_from_bank(self, pkg: Dict[str, Any], levels: Any, count: int) -> List[Dict[str, Any]]:
        if isinstance(levels, str): levels = [levels]
        levels = [l.lower() for l in levels]

        # Prioritize expandedQuestionBank because it has IDs and concept mappings
        bank = pkg.get("original_data", {}).get("assessment", {}).get("expandedQuestionBank", [])

        # Only use content.quiz as a last resort if it has IDs
        if not bank:
            bank = [q for q in pkg.get("content", {}).get("quiz", []) if q.get("id")]

        eligible = [q for q in bank if q.get("level", q.get("difficulty", "foundation")).lower() in levels]
        if not eligible:
            eligible = [q for q in bank if q.get("id")] # last resort: any with ID

        if not eligible: return []

        return random.sample(eligible, min(len(eligible), count))

    def _format_q(self, q: Dict[str, Any], class_name: str, chapter_id: str) -> Dict[str, Any]:
        mapping = self.mastery_service.get_concept_for_question(class_name, chapter_id, str(q.get("id")))

        q_type = q.get("type", "mcq").lower().replace("-", "_")
        if q_type == "fill_blank": q_type = "fill_blanks"

        return {
            "id": q.get("id"),
            "type": q_type,
            "question": q.get("question"),
            "options": q.get("options", []),
            "correctAnswer": str(q.get("answer", q.get("correctAnswer", ""))),
            "explanation": q.get("explanation", ""),
            "concept_id": mapping[0] if mapping else None,
            "is_prereq": q.get("is_prereq", False)
        }

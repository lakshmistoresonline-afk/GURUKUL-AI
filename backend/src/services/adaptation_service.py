import os
import json
import logging
from typing import Dict, Any, List, Optional

from ..config.app_config import settings

logger = logging.getLogger(__name__)

class AdaptationService:
    def __init__(self, graph_path: Optional[str] = None):
        self.graph_path = graph_path or os.path.join(settings.STORAGE_PATH, "concept_graph.json")
        self.graph = self._load_json(self.graph_path)

    def _load_json(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path): return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading graph: {e}")
            return {}

    def get_upstream_gaps(self, student_record: Dict[str, Any], global_concept_id: str) -> List[str]:
        """Identifies which prerequisite concepts (nodes) are not mastered."""
        gaps = []
        edges = self.graph.get("edges", [])
        nodes = self.graph.get("nodes", [])

        # 1. Check builds-on links
        dependencies = [e["from"] for e in edges if e["to"] == global_concept_id and e.get("relation") == "builds-on"]

        perf = student_record.get("conceptPerformance", {})

        for pid in dependencies:
            # Find the node to get more info if needed
            node = next((n for n in nodes if n["id"] == pid), None)

            # Use pid directly as the key in student_record if it's a global graph
            # Or try to extract a localId if the record is chapter-scoped
            local_id = pid
            if "_" in pid:
                 # e.g. c5_english_01_01 -> eesa101_c01?
                 # No, the IDs in the graph currently seem to be c5_english_01_01
                 pass

            p_perf = perf.get(local_id, {})
            if p_perf.get("foundation", 0) < 0.7:
                gaps.append(pid)
        return gaps

    def get_recommendation(self, chapter_id: str, diagnostic_signals: Dict[str, str]) -> Dict[str, Any]:
        """Returns personalization advice based on diagnostic signals."""
        strong_concepts = [c for c, s in diagnostic_signals.items() if s == "STRONG"]
        weak_concepts = [c for c, s in diagnostic_signals.items() if s in ["UNKNOWN", "PREREQUISITE_GAP"]]

        advice = []
        if strong_concepts:
            advice.append(f"You show strong understanding of {len(strong_concepts)} concepts. We'll focus on advanced applications.")
        if weak_concepts:
            advice.append(f"We've identified {len(weak_concepts)} areas for growth. We'll provide extra support here.")

        return {
            "skip_intro": len(strong_concepts) > 2,
            "focus_areas": weak_concepts,
            "message": " ".join(advice)
        }

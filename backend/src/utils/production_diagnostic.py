import os
import json
import logging
import sys
from typing import Dict, Any

# Add project root to path for direct execution
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

logger = logging.getLogger(__name__)

class ProductionDiagnostic:
    def __init__(self):
        from ..config.app_config import settings
        self.base_pkg = os.path.join(settings.STORAGE_PATH, "output")
        self.graph_path = os.path.join(settings.STORAGE_PATH, "concept_graph.json")

    def run_health_check(self) -> Dict[str, Any]:
        report = {
            "status": "HEALTHY",
            "checks": {
                "curriculum": self._check_curriculum(),
                "graph": self._check_graph(),
                "services": self._check_services()
            }
        }

        if any(c["status"] == "FAIL" for c in report["checks"].values()):
            report["status"] = "UNHEALTHY"

        return report

    def _check_curriculum(self) -> Dict[str, Any]:
        count = 0
        for root, _, files in os.walk(self.base_pkg):
            if 'package.json' in files: count += 1

        return {
            "status": "PASS" if count == 101 else "FAIL",
            "package_count": count,
            "expected": 101
        }

    def _check_graph(self) -> Dict[str, Any]:
        if not os.path.exists(self.graph_path):
            return {"status": "FAIL", "error": "Graph file missing"}

        with open(self.graph_path, 'r', encoding='utf-8') as f:
            graph = json.load(f)

        node_count = len(graph.get("concepts", {}))
        return {
            "status": "PASS" if node_count == 769 else "FAIL",
            "node_count": node_count,
            "expected": 769
        }

    def _check_services(self) -> Dict[str, Any]:
        try:
            from src.services.mastery_service import MasteryService
            ms = MasteryService()
            return {"status": "PASS"}
        except Exception as e:
            return {"status": "FAIL", "error": str(e)}

if __name__ == "__main__":
    diag = ProductionDiagnostic()
    print(json.dumps(diag.run_health_check(), indent=2))

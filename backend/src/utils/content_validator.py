import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ContentValidator:
    """
    Ensures generated chapter packages meet the Gurukul content contract.
    """

    REQUIRED_KEYS = [
        "objectives", "introduction", "teacher_explanation",
        "story_explanation", "concepts", "quiz", "flashcards", "summary"
    ]

    @staticmethod
    def validate_package(data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs full validation on a chapter package."""
        report = {
            "is_valid": True,
            "missing_keys": [],
            "errors": []
        }

        content = data.get("content", {})
        if not content:
            report["is_valid"] = False
            report["errors"].append("No content found in package.")
            return report

        for key in ContentValidator.REQUIRED_KEYS:
            val = content.get(key)
            if not val:
                report["missing_keys"].append(key)
                report["is_valid"] = False

            # Type specific checks
            if key == "quiz" and not isinstance(val, list):
                report["errors"].append("Quiz must be a list.")
                report["is_valid"] = False

            if key == "flashcards" and not isinstance(val, list):
                report["errors"].append("Flashcards must be a list.")
                report["is_valid"] = False

        return report

def audit_all_content(base_dir: str):
    """Scan and report on all generated chapters."""
    results = []
    for root, dirs, files in os.walk(base_dir):
        if "package.json" in files:
            path = os.path.join(root, "package.json")
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    val = ContentValidator.validate_package(data)
                    if not val["is_valid"]:
                        print(f"INVALID: {path} - Missing: {val['missing_keys']}")
                    results.append({"path": path, "status": val})
            except Exception as e:
                print(f"ERROR reading {path}: {e}")
    return results

if __name__ == "__main__":
    # Local test run
    audit_all_content("./storage/output")

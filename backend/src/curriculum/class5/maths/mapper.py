from typing import Dict, Any

class Class5MathsMapper:
    @staticmethod
    def map_to_sections(resolved_bundle: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "overview": resolved_bundle.get("overview"),
            "notes": resolved_bundle.get("notes"),
            "master": resolved_bundle.get("master"),
            "flashcards": resolved_bundle.get("flashcards", []),
            "mindmaps": resolved_bundle.get("mindmap", {}),
            "quiz": resolved_bundle.get("quiz", []),
            "question_papers": resolved_bundle.get("question_papers")
        }

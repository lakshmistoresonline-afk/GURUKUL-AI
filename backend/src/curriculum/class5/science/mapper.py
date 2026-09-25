from typing import Dict, Any

class Class5ScienceMapper:
    @staticmethod
    def map_to_sections(resolved_bundle: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "overview": None,
            "notes": resolved_bundle.get("notes"),
            "master": resolved_bundle.get("master"),
            "flashcards": resolved_bundle.get("flashcards", []),
            "mindmaps": resolved_bundle.get("mindmap", {}),
            "quiz": resolved_bundle.get("quiz", []),
            "question_papers": None
        }

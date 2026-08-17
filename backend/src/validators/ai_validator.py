import json
from typing import Dict, Any, List

class AIValidator:
    @staticmethod
    def validate_quiz(quiz: List[Dict[str, Any]]) -> bool:
        if not isinstance(quiz, list): return False
        for item in quiz:
            if not all(k in item for k in ["question", "options", "correctAnswer"]):
                return False
            if len(item["options"]) != 4:
                return False
            if item["correctAnswer"] not in item["options"]:
                return False
        return True

    @staticmethod
    def validate_lesson(lesson: Dict[str, Any]) -> bool:
        required = ["introduction", "teacher_explanation", "story_explanation"]
        return all(lesson.get(k) for k in required)

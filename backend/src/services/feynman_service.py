from typing import List, Dict, Any, Optional
import random
from ..orchestrator.ai_orchestrator import AIOrchestrator

class FeynmanLevel:
    SIMPLIFY = 1      # Explain in own words
    TEACH_YOUNGER = 2 # Explain to 8yo
    ANALOGY = 3       # Give an example
    CONTRAST = 4      # Give a non-example
    DEBUG = 5         # Explain a common mistake
    TRANSFER = 6      # Apply to new situation

class FeynmanService:
    def __init__(self, orchestrator: AIOrchestrator):
        self.orchestrator = orchestrator

    async def get_challenge(self, concept_name: str, level: int = 1) -> Dict[str, Any]:
        """Generates a challenge prompt based on the mastery level."""

        prompts = {
            FeynmanLevel.SIMPLIFY: f"Explain '{concept_name}' in your own words. Don't just repeat the textbook.",
            FeynmanLevel.TEACH_YOUNGER: f"Imagine you are teaching '{concept_name}' to an 8-year-old. How would you explain it so they understand?",
            FeynmanLevel.ANALOGY: f"Give me a real-world example or an analogy for '{concept_name}'.",
            FeynmanLevel.CONTRAST: f"Explain what '{concept_name}' is NOT. Give an example of something that might be confused with it, and explain the difference.",
            FeynmanLevel.DEBUG: f"What is a common mistake students make when learning about '{concept_name}'? Why do they make it?",
            FeynmanLevel.TRANSFER: f"How would you use the idea of '{concept_name}' in a completely different subject or a real-life problem?"
        }

        base_prompt = prompts.get(level, prompts[FeynmanLevel.SIMPLIFY])

        system_prompt = f"""
        You are a curious student. You want to learn about '{concept_name}'.
        Ask the user a question based on this: "{base_prompt}"
        Be encouraging and informal.
        """

        res = await self.orchestrator.generate(system_prompt, task_type="feynman_challenge")
        return {
            "level": level,
            "concept": concept_name,
            "question": res["response"]
        }

    async def evaluate(self, concept_name: str, explanation: str, context: str, level: int) -> Dict[str, Any]:
        """Evaluates the student's response."""

        prompt = f"""
        CONCEPT: {concept_name}
        CHALLENGE LEVEL: {level}
        TEXTBOOK CONTEXT: {context[:2000]}
        STUDENT EXPLANATION: "{explanation}"

        TASK:
        Evaluate the student's explanation.
        - Accuracy: Does it match the science/facts in the context?
        - Level Appropriateness: Did they meet the specific challenge (analogy, teaching a younger kid, etc.)?

        Return JSON:
        {{
            "feedback": "encouraging feedback",
            "score": 0-100,
            "is_accurate": true/false,
            "is_complete": true/false
        }}
        """

        schema = {
            "type": "object",
            "properties": {
                "feedback": {"type": "string"},
                "score": {"type": "integer"},
                "is_accurate": {"type": "boolean"},
                "is_complete": {"type": "boolean"}
            },
            "required": ["feedback", "score", "is_accurate", "is_complete"]
        }

        res = await self.orchestrator.generate_structured(prompt, schema, task_type="feynman_eval")
        return res["response"]

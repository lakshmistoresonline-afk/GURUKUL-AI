import os
import json
import logging
import subprocess
import re
from typing import Any, Dict, List, Optional
from ..orchestrator.ai_orchestrator import AIOrchestrator
from ..config.app_config import settings

logger = logging.getLogger(__name__)

class AnimationService:
    """
    Handles the educational animation pipeline:
    1. Plan Generation (AI)
    2. Scene Scripting (Template-based)
    3. Manim Rendering
    4. Post-processing (FFmpeg)
    """

    def __init__(self, orchestrator: AIOrchestrator):
        self.orchestrator = orchestrator

    async def generate_animation_plan(self, chapter_content: Dict[str, Any], subject: str) -> Dict[str, Any]:
        """Generate a structured animation plan using AI."""

        prompt = f"""
        You are an educational animator. Create an animation plan for a lesson on "{chapter_content.get('topic', 'this topic')}".
        Subject: {subject}

        CONTENT:
        Teacher Explanation: {chapter_content.get('teacher_explanation', '')[:2000]}
        Key Concepts: {chapter_content.get('concepts', '')[:1000]}

        TASK:
        Generate a JSON animation plan with exactly 3 scenes.
        Each scene must have:
        - title: Short title (max 5 words)
        - description: Visual description
        - primitives: List of objects (rect, circle, triangle, text, line, arrow)
        - actions: List of actions (show, move, rotate, transform, flash)
        - narration: Concise text for the voiceover
        - duration: Estimated seconds (3-7)

        Return ONLY valid JSON.
        """

        schema = {
            "type": "object",
            "properties": {
                "scenes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "primitives": {"type": "array", "items": {"type": "string"}},
                            "actions": {"type": "array", "items": {"type": "string"}},
                            "narration": {"type": "string"},
                            "duration": {"type": "integer"}
                        },
                        "required": ["title", "description", "primitives", "actions", "narration", "duration"]
                    },
                    "minItems": 3,
                    "maxItems": 3
                }
            },
            "required": ["scenes"]
        }

        result = await self.orchestrator.generate_structured(prompt, schema, task_type="animation_plan")
        if not result.get("success"):
             raise RuntimeError(f"Failed to generate animation plan: {result.get('error')}")

        return result.get("response")

    def create_manim_script(self, plan: Any, output_path: str) -> str:
        """
        Generate a Manim Python script from the plan using approved primitives.
        """

        script_content = [
            "from manim import *",
            "import numpy as np",
            "",
            "class EducationalAnimation(Scene):",
            "    def construct(self):",
            "        # Configuration",
            "        self.camera.background_color = '#0F172A' # Gurukul Dark Slate",
            "        primary_color = '#2563EB'",
            "        secondary_color = '#8B5CF6'",
            "        accent_color = '#10B981'",
            ""
        ]

        # Extract scenes robustly
        scenes = []
        if isinstance(plan, list):
            scenes = plan
        elif isinstance(plan, dict):
            scenes = plan.get('scenes', [])

        for i, scene in enumerate(scenes):
            if not isinstance(scene, dict): continue

            title_text = scene.get('title', f'Scene {i+1}').replace("'", "\\'")
            script_content.append(f"        # --- SCENE {i+1}: {title_text} ---")

            # 1. Show Scene Title
            script_content.append(f"        title = Text('{title_text}', color=primary_color).to_edge(UP)")
            script_content.append("        self.play(Write(title))")

            # 2. Process Primitives & Actions (Template based)
            prims = scene.get('primitives', [])
            actions = scene.get('actions', [])

            # Create a main object based on the first primitive
            main_obj_code = "None"
            if "rect" in str(prims).lower():
                main_obj_code = "Rectangle(height=2, width=3, color=secondary_color)"
            elif "circle" in str(prims).lower():
                main_obj_code = "Circle(radius=1.5, color=secondary_color)"
            elif "triangle" in str(prims).lower():
                main_obj_code = "Triangle(color=secondary_color).scale(2)"
            else:
                main_obj_code = "Square(side_length=2, color=secondary_color)"

            script_content.append(f"        obj = {main_obj_code}")
            script_content.append("        self.play(Create(obj))")

            # Symmetry specific action if mentioned
            if "rotate" in str(actions).lower() or "symmetry" in title_text.lower():
                script_content.append("        self.play(Rotate(obj, angle=PI))")

            if "move" in str(actions).lower():
                script_content.append("        self.play(obj.animate.shift(RIGHT * 2))")

            if "flash" in str(actions).lower():
                script_content.append("        self.play(Flash(obj))")

            # 3. Wait for duration
            script_content.append(f"        self.wait({min(scene.get('duration', 2), 5)})")

            # 4. Cleanup
            script_content.append("        self.play(FadeOut(obj), FadeOut(title))")
            script_content.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(script_content))

        return output_path

    async def render_animation(self, script_path: str, output_dir: str) -> str:
        """Render the script using Manim."""

        # Determine output filename
        # Manim by default outputs to media/videos/{script_name}/{quality}/{class_name}.mp4
        script_name = os.path.splitext(os.path.basename(script_path))[0]

        try:
            # We use low quality (-ql) for speed in this environment
            command = [
                "manim", "-ql", "--media_dir", output_dir,
                script_path, "EducationalAnimation"
            ]
            logger.info(f"Executing: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)

            # Find the rendered file
            # Typical path: {output_dir}/videos/{script_name}/480p15/EducationalAnimation.mp4
            rendered_path = os.path.join(output_dir, "videos", script_name, "480p15", "EducationalAnimation.mp4")

            if os.path.exists(rendered_path):
                return rendered_path
            else:
                logger.error(f"Render finished but file not found at {rendered_path}")
                raise FileNotFoundError("Render output missing")

        except Exception as e:
            logger.error(f"Manim render failed: {e}")
            if hasattr(e, 'stdout'): logger.error(f"STDOUT: {e.stdout}")
            if hasattr(e, 'stderr'): logger.error(f"STDERR: {e.stderr}")
            raise

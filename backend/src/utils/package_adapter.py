import logging
import json
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PackageAdapter:
    """
    Adapts various chapter package schemas to a unified interface.
    Optimized for Gurukul Omniscient V4 Unified Architecture.
    """

    @staticmethod
    def adapt(pkg: Dict[str, Any], base_path: Optional[str] = None) -> Dict[str, Any]:
        if not pkg or not isinstance(pkg, dict):
            return pkg if isinstance(pkg, dict) else {}

        if pkg.get("schema_type") in ["ADAPTED", "ADAPTED_OUTLINE"]:
            return pkg

        adapted = {
            "schema_type": "ADAPTED",
            "metadata": {},
            "content": {},
            "original_data": {"aiEnrichment": {}, "curriculum": {}},
            "components": pkg.get("components", {}),
            "mastery_architecture": pkg.get("mastery_architecture", "V1")
        }

        # --- COMPONENT RETRIEVAL ---
        def get_comp(name):
            # 1. Search in V4 Super Files
            v4_map = {
                "chapter_metadata": "super_foundation",
                "chapter_content": "super_foundation",
                "chapter_summary": "super_foundation",
                "learning_objectives": "super_foundation",
                "prerequisites": "super_foundation",
                "mastery_snapshot": "super_foundation",
                "teacher_explanation": "super_pedagogy",
                "student_explanation": "super_pedagogy",
                "story_mode": "super_pedagogy",
                "visual_logic": "super_pedagogy",
                "eq_pulse": "super_pedagogy",
                "activities": "super_experiential",
                "learning_sprints": "super_experiential",
                "assessment_pool": "super_assessment",
                "assessment_bank": "super_assessment",
                "concepts": "super_system",
                "flashcards": "super_system",
                "common_mistakes": "super_system"
            }

            super_key = v4_map.get(name)
            if super_key:
                super_data = pkg.get("components", {}).get(super_key)
                if isinstance(super_data, dict):
                    if name in super_data: return super_data[name]
                    shrt = name.replace("chapter_", "")
                    if shrt in super_data: return super_data[shrt]

            # 2. Search in direct components or root
            comp = pkg.get("components", {}).get(name) or pkg.get(name)
            if isinstance(comp, dict):
                if "content" in comp: return comp["content"]
                for k in ["items", "questions", "concepts", "cards", "sprints", "units"]:
                    if k in comp: return comp[k]
            return comp or {}

        # --- DATA BINDING ---
        meta = get_comp("chapter_metadata")
        alignment = pkg.get("curriculum_alignment") or {}

        name = alignment.get("chapter_title") or meta.get("title") or meta.get("chapter_title") or meta.get("chapter_name") or pkg.get("chapter", {}).get("chapter_title") or ""

        adapted["metadata"] = {
            "chapter_id": alignment.get("chapter_id") or meta.get("chapter_id") or meta.get("chapterId") or pkg.get("chapter", {}).get("chapter_id"),
            "chapter_name": name,
            "chapterTitle": name,
            "subject": alignment.get("subject") or meta.get("subject") or pkg.get("chapter", {}).get("subject"),
            "class_name": alignment.get("class") or meta.get("class_name") or pkg.get("chapter", {}).get("class")
        }

        content = get_comp("chapter_content")
        adapted["content"]["introduction"] = content.get("overview") or content.get("introduction") or ""

        summary = get_comp("chapter_summary")
        adapted["content"]["summary"] = summary.get("summary") or summary.get("chapter_summary") or ""

        adapted["content"]["teacher_explanation"] = get_comp("teacher_explanation")
        adapted["content"]["student_explanation"] = get_comp("student_explanation")

        concepts = get_comp("concepts")
        if isinstance(concepts, list):
            adapted["concepts"] = concepts
            adapted["original_data"]["aiEnrichment"]["concepts"] = concepts

        adapted["content"]["snapshot"] = get_comp("mastery_snapshot")
        adapted["content"]["visual_logic"] = get_comp("visual_logic")
        adapted["content"]["eq_pulse"] = get_comp("eq_pulse") or get_comp("emotional_intelligence")

        adapted["content"]["prerequisites"] = get_comp("prerequisites")
        adapted["content"]["learning_sprints"] = get_comp("learning_sprints")
        adapted["content"]["common_mistakes"] = get_comp("common_mistakes")

        adapted["content"]["quiz"] = get_comp("assessment_pool") or get_comp("assessment_bank") or get_comp("quiz")
        adapted["content"]["flashcards"] = get_comp("flashcards")

        return adapted

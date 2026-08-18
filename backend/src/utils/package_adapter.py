import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PackageAdapter:
    """
    Adapts various chapter package schemas to a unified interface.
    Specifically bridges the 1.0.0 (Legacy) and 2.1.0 (Fresh) schemas.
    """

    @staticmethod
    def adapt(pkg: Dict[str, Any]) -> Dict[str, Any]:
        if not pkg:
            return {}

        # If it's already the legacy flat structure, return it
        if "content" in pkg and "metadata" in pkg and "components" not in pkg:
            return pkg

        # If it's the new 'components' based structure
        if "components" in pkg:
            adapted = {
                "schema_type": "ADAPTED",
                "metadata": {},
                "content": {},
                "original_data": {
                    "aiEnrichment": {},
                    "curriculum": {}
                },
                "components": pkg["components"] # Keep original components
            }

            # Extract Chapter Info
            chapter_info = pkg.get("chapter", {})
            adapted["metadata"] = {
                "chapter_id": chapter_info.get("chapter_id"),
                "chapterTitle": chapter_info.get("chapter_title"),
                "chapter_name": chapter_info.get("chapter_title"),
                "subject": chapter_info.get("subject"),
                "class_name": f"class_{chapter_info.get('class')}" if chapter_info.get("class") else None,
                "chapter_number": chapter_info.get("chapter_number")
            }
            adapted["original_data"]["curriculum"]["displayName"] = chapter_info.get("chapter_title")

            # Extract Core Components into 'content' for legacy UI support
            comps = pkg["components"]

            # Metadata component might have more detail
            meta_comp = comps.get("chapter_metadata", {}).get("content", {})
            if meta_comp:
                adapted["metadata"].update(meta_comp)

            # Content
            content_comp = comps.get("chapter_content", {}).get("content", {})
            if content_comp:
                adapted["content"]["introduction"] = content_comp.get("introduction") or content_comp.get("overview")
                adapted["content"]["summary"] = content_comp.get("summary")

            # Story
            story_comp = comps.get("story_mode", {}).get("content", {})
            if story_comp:
                story_text = story_comp.get("story") or story_comp.get("narrative")
                adapted["content"]["story_explanation"] = story_text
                adapted["content"]["storyExplanation"] = story_text

            # Teacher Explanation
            teacher_comp = comps.get("teacher_explanation", {}).get("content", {})
            if teacher_comp:
                teacher_text = teacher_comp.get("explanation") or teacher_comp.get("guide")
                adapted["content"]["teacher_explanation"] = teacher_text
                adapted["content"]["teacherExplanation"] = teacher_text

            # Student Explanation
            student_comp = comps.get("student_explanation", {}).get("content", {})
            if student_comp:
                student_text = student_comp.get("explanation")
                adapted["content"]["student_explanation"] = student_text
                adapted["content"]["studentExplanation"] = student_text

            # Concepts
            concepts_comp = comps.get("concepts", {}).get("content", {})
            if concepts_comp:
                concepts_list = concepts_comp.get("concepts", [])
                # Map 'definition' to 'explanation' for frontend compatibility
                for c in concepts_list:
                    if "definition" in c and "explanation" not in c:
                        c["explanation"] = c["definition"]

                adapted["original_data"]["aiEnrichment"]["concepts"] = concepts_list
                # Format for legacy split string if needed
                adapted["content"]["concepts"] = "\n".join([c.get("name", "") for c in concepts_list])

            # Objectives
            obj_comp = comps.get("learning_objectives", {}).get("content", {})
            if obj_comp:
                objectives = obj_comp.get("objectives", [])
                adapted["original_data"]["aiEnrichment"]["learningObjectives"] = objectives
                # Also put in content.learning_goals
                adapted["content"]["learning_goals"] = objectives

            # Activities / Lab
            activities_list = []
            for comp_name in ["interactive_lab", "activities"]:
                comp_data = comps.get(comp_name, {}).get("content", {})
                if isinstance(comp_data, dict):
                    a_list = comp_data.get("activities") or comp_data.get("items") or []
                    if isinstance(a_list, list):
                        activities_list.extend(a_list)
                elif isinstance(comp_data, list):
                    activities_list.extend(comp_data)

            if activities_list:
                adapted["original_data"]["aiEnrichment"]["masteryLab"] = {
                    "activities": activities_list
                }
                adapted["content"]["activities"] = activities_list

            # Multimedia
            media_comp = comps.get("multimedia", {}).get("content", {})
            if media_comp:
                adapted["content"]["multimedia"] = media_comp.get("resources", [])
                adapted["original_data"]["aiEnrichment"]["multimedia_learning"] = media_comp # Storyboard style

            # Quiz / Assessment
            questions = []
            for comp_name in ["assessment_bank", "practice_bank", "adaptive_practice", "quiz"]:
                comp_data = comps.get(comp_name, {}).get("content", {})
                if isinstance(comp_data, dict):
                    q_list = comp_data.get("questions") or comp_data.get("items") or []
                    if isinstance(q_list, list):
                        questions.extend(q_list)

            if questions:
                adapted["content"]["quiz"] = questions
                adapted["original_data"]["assessment"] = {
                    "expandedQuestionBank": questions
                }

            # Flashcards
            flash_comp = comps.get("flashcards", {}).get("content", [])
            if flash_comp:
                adapted["content"]["flashcards"] = flash_comp

            return adapted

        return pkg

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
        if not pkg or not isinstance(pkg, dict):
            return pkg if isinstance(pkg, dict) else {}

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
                # Add key points to introduction if it's too short
                if content_comp.get("source_grounded_key_points") and len(adapted["content"].get("introduction", "")) < 100:
                    adapted["content"]["introduction"] = "\n".join(content_comp["source_grounded_key_points"])

            # Story
            story_comp = comps.get("story_mode", {}).get("content", {})
            if story_comp:
                story_text = story_comp.get("story") or story_comp.get("narrative")
                if not story_text and "scenes" in story_comp:
                    # Construct story from scenes
                    scenes = story_comp["scenes"]
                    story_text = (story_comp.get("opening", "") + "\n\n" +
                                 "\n\n".join([s.get("narration", "") for s in scenes]) + "\n\n" +
                                 story_comp.get("ending_reflection", ""))

                adapted["content"]["story_explanation"] = story_text
                adapted["content"]["storyExplanation"] = story_text

            # Teacher Explanation
            teacher_comp = comps.get("teacher_explanation", {}).get("content", {})
            if teacher_comp and isinstance(teacher_comp, dict):
                sections = teacher_comp.get("explanation_sections", [])
                if sections and isinstance(sections, list):
                    # Join sections into a structured markdown string
                    text_parts = []
                    for s in sections:
                        if not isinstance(s, dict): continue
                        title = s.get('title', '')
                        expl = s.get('explanation', '')
                        if title: text_parts.append(f"### {title}")
                        if expl: text_parts.append(expl)
                        # Add evidence if present
                        ev = s.get('source_evidence', [])
                        if ev and isinstance(ev, list):
                            text_parts.append("\n**Evidence from chapter:**")
                            for item in ev: text_parts.append(f"* {item}")
                    teacher_text = "\n\n".join(text_parts)
                else:
                    teacher_text = teacher_comp.get("explanation") or teacher_comp.get("guide") or ""

                # Fallback to chapter_content if teacher_explanation is still empty
                if not teacher_text:
                    content_comp = comps.get("chapter_content", {}).get("content", {})
                    teacher_text = content_comp.get("introduction") or content_comp.get("overview") or ""

                adapted["content"]["teacher_explanation"] = teacher_text
                adapted["content"]["teacherExplanation"] = teacher_text
            elif isinstance(teacher_comp, str):
                adapted["content"]["teacher_explanation"] = teacher_comp
                adapted["content"]["teacherExplanation"] = teacher_comp

            # Student Explanation
            student_comp = comps.get("student_explanation", {}).get("content", {})
            if student_comp and isinstance(student_comp, dict):
                student_text = student_comp.get("explanation") or student_comp.get("summary") or ""
                adapted["content"]["student_explanation"] = student_text
                adapted["content"]["studentExplanation"] = student_text
            elif isinstance(student_comp, str):
                adapted["content"]["student_explanation"] = student_comp
                adapted["content"]["studentExplanation"] = student_comp

            # Concepts
            concepts_comp = comps.get("concepts", {}).get("content", {})
            if concepts_comp:
                concepts_list = concepts_comp.get("concepts", [])
                # Map 'definition' to 'explanation' for frontend compatibility
                for c in concepts_list:
                    if "definition" in c and "explanation" not in c:
                        c["explanation"] = c["definition"]

                adapted["original_data"]["aiEnrichment"]["concepts"] = concepts_list
                # Format for legacy split string if needed by UI
                adapted["content"]["concepts"] = "\n".join([c.get("name", "") for c in concepts_list])
                # Provide list version for backend services
                adapted["concepts"] = concepts_list
                adapted["mappings"] = concepts_list
                adapted["concepts_list"] = concepts_list

            # Mind Map / Concept Graph -> Adapt to Frontend MindMap structure
            graph_comp = comps.get("concept_graph", {}).get("content", {})
            if graph_comp and isinstance(graph_comp, dict):
                # Store original for any component that can handle it
                adapted["content"]["concept_graph"] = graph_comp

                # Create MindMap format: { topic: string, branches: [{ label: string, details: string[] }] }
                nodes = graph_comp.get("nodes", [])
                edges = graph_comp.get("edges", [])

                if nodes and isinstance(nodes, list):
                    central_node = nodes[0]
                    mind_map = {
                        "topic": central_node.get("label", chapter_info.get("chapter_title")),
                        "branches": []
                    }

                    # Group branches (all nodes except the first one)
                    for node in nodes[1:]:
                        if isinstance(node, dict):
                            mind_map["branches"].append({
                                "label": node.get("label", "Concept"),
                                "details": [node.get("description", "")] if node.get("description") else []
                            })

                    adapted["content"]["mind_map"] = mind_map
                    adapted["content"]["mindMap"] = mind_map
                    adapted["original_data"]["aiEnrichment"]["mindMap"] = mind_map

            # Objectives
            obj_comp = comps.get("learning_objectives", {}).get("content", {})
            if obj_comp:
                objectives = obj_comp.get("objectives", [])
                adapted["original_data"]["aiEnrichment"]["learningObjectives"] = objectives
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
                resources = media_comp.get("resources", [])
                adapted["content"]["multimedia"] = resources
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
                adapted["quiz"] = questions
                adapted["original_data"]["assessment"] = {
                    "expandedQuestionBank": questions
                }

            # Flashcards
            flash_comp = comps.get("flashcards", {}).get("content", [])
            if flash_comp:
                adapted["content"]["flashcards"] = flash_comp

            return adapted

        return pkg

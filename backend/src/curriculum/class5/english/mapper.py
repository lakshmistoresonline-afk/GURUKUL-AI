from typing import Dict, Any

class Class5EnglishMapper:
    @staticmethod
    def map_to_sections(resolved_bundle: Dict[str, Any]) -> Dict[str, Any]:
        qp = resolved_bundle.get("question_papers")
        ov = resolved_bundle.get("overview", {}) or {}
        key_concepts = ov.get("key_concepts", [])
        key_terms = ov.get("key_terms", [])

        if qp and isinstance(qp, dict):
            papers = qp.get("question_papers", [])
            for paper in papers:
                for sec in paper.get("sections", []):
                    for qIdx, q in enumerate(sec.get("questions", [])):
                        q_text = q.get("question_text", "")
                        if "is tested in Set" in q_text:
                            if qIdx < len(key_concepts):
                                concept_str = key_concepts[qIdx].split(":")[0].strip()
                                q["question_text"] = f"In relation to '{concept_str}', which statement accurately describes the core learning objective?"
                            elif (qIdx - len(key_concepts)) < len(key_terms):
                                term_obj = key_terms[qIdx - len(key_concepts)]
                                term_name = term_obj.get("term") if isinstance(term_obj, dict) else str(term_obj)
                                q["question_text"] = f"What is the significance of '{term_name}' within the context of this chapter?"

        return {
            "overview": resolved_bundle.get("overview"),
            "notes": resolved_bundle.get("notes"),
            "master": resolved_bundle.get("master"),
            "flashcards": resolved_bundle.get("flashcards", []),
            "mindmaps": resolved_bundle.get("mindmap", {}),
            "quiz": resolved_bundle.get("quiz", []),
            "question_papers": qp
        }

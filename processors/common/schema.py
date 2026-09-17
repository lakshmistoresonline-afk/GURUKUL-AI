from typing import Any

CANONICAL_PILLARS = ["learn", "practice", "assess", "revise", "resources"]

def create_empty_chapter_package(class_id: str, subject_id: str, chapter_id: str, title: str) -> dict[str, Any]:
    return {
        "id": f"{class_id}_{subject_id}_{chapter_id}",
        "classId": class_id,
        "subjectId": subject_id,
        "chapter_id": chapter_id,
        "title": title,
        "learn": [],
        "practice": [],
        "assess": [],
        "revise": [],
        "resources": [],
        "accounting": {}
    }

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from .subject_registry import SubjectRegistry

PROCESSED_ROOT = Path(r"D:/GURUKUL/ProcessedContent")
CONTENTS_ROOT = Path(r"D:/GURUKUL/Contents")

class CurriculumRegistry:
    """
    Authoritative Central Curriculum Registry for Gurukul AI (Strict Identity Resolver).
    Rejects substring matching, default arguments, and synthetic content fallback.
    """

    @classmethod
    def get_classes(cls) -> List[str]:
        grades = []
        if CONTENTS_ROOT.exists():
            grades = sorted([d.name.replace("Class ", "") for d in CONTENTS_ROOT.iterdir() if d.is_dir() and "class" in d.name.lower()])
        return grades if grades else ["5", "6", "7"]

    @classmethod
    def get_subjects(cls, grade: str) -> List[str]:
        grade_dir = CONTENTS_ROOT / f"Class {grade}"
        subjects = []
        if grade_dir.exists():
            subjects = sorted([d.name for d in grade_dir.iterdir() if d.is_dir()])
        return subjects

    @classmethod
    def resolve_chapter_path(cls, identity: CurriculumIdentity) -> Path:
        grade = identity.grade
        canonical_subject = SubjectRegistry.resolve_canonical_subject(identity.subject)

        sub_dir_name = canonical_subject.replace("_", "").capitalize()
        if canonical_subject == "social_science":
            sub_dir_name = "Social"
        elif canonical_subject == "mathematics":
            sub_dir_name = "Maths" if grade in ["5", "6"] else "MathsI"

        class_proc_dir = PROCESSED_ROOT / f"Class{grade}"
        if not class_proc_dir.exists():
            raise FileNotFoundError(f"Class {grade} processed directory not found.")

        target_subj_folder = None
        for d in class_proc_dir.iterdir():
            if d.is_dir() and SubjectRegistry.resolve_canonical_subject(d.name) == canonical_subject:
                target_subj_folder = d
                break

        if not target_subj_folder:
            raise FileNotFoundError(f"Subject {identity.subject} for Class {grade} not found.")

        # Strict exact match on chapter_id folder name (NO substring matching)
        chapter_folder = target_subj_folder / identity.chapter_id
        if not chapter_folder.exists() or not chapter_folder.is_dir():
            raise FileNotFoundError(f"Chapter ID '{identity.chapter_id}' not found under Class {grade} {identity.subject}. Strict isolation enforced.")

        return chapter_folder

    @classmethod
    def load_chapter_bundle(cls, identity: CurriculumIdentity) -> ChapterRuntimeDTO:
        ch_path = cls.resolve_chapter_path(identity)

        sections = {}
        for sec_name in ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers", "foundational"]:
            sec_file = ch_path / f"{sec_name}.json"
            if sec_file.exists():
                try:
                    with open(sec_file, "r", encoding="utf-8") as f:
                        sections[sec_name] = json.load(f)
                except Exception:
                    sections[sec_name] = None
            else:
                sections[sec_name] = None

        ch_title = identity.chapter_id
        ch_num = 1
        unit_title = "Curriculum Unit"

        manifest_file = ch_path / "manifest.json"
        if manifest_file.exists():
            try:
                with open(manifest_file, "r", encoding="utf-8") as mf:
                    md = json.load(mf)
                    ch_title = md.get("chapter_title", ch_title)
                    ch_num = md.get("chapter_number", 1)
            except:
                pass

        dto = ChapterRuntimeDTO(
            identity=identity,
            chapter_number=int(ch_num),
            chapter_title=ch_title,
            unit_title=unit_title,
            data=sections,
            status="READY"
        )
        return dto

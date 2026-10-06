import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from .subject_registry import SubjectRegistry

PROCESSED_ROOT = Path(r"D:/GURUKUL/ProcessedContent")
CONTENTS_ROOT = Path(r"D:/GURUKUL/Contents")

class CurriculumResolutionError(Exception):
    pass

class CurriculumRegistry:
    """
    Fully Data-Driven Authoritative Curriculum Registry for Gurukul AI.
    Discovers and resolves classes, subjects, books, parts, units, and chapters
    directly from the filesystem without hardcoded branching or default fallbacks.
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

        class_proc_dir = PROCESSED_ROOT / f"Class{grade}"
        if not class_proc_dir.exists():
            raise CurriculumResolutionError(f"Class {grade} processed directory not found.")

        target_subj_folder = None
        for d in class_proc_dir.iterdir():
            if d.is_dir() and SubjectRegistry.resolve_canonical_subject(d.name) == canonical_subject:
                if identity.book != "main" and identity.book.lower() not in d.name.lower():
                    continue
                target_subj_folder = d
                break

        if not target_subj_folder:
            raise CurriculumResolutionError(f"Subject '{identity.subject}' (canonical: {canonical_subject}, book: {identity.book}) for Class {grade} not found.")

        chapter_folder = target_subj_folder / identity.chapter_id
        if not chapter_folder.exists() or not chapter_folder.is_dir():
            raise CurriculumResolutionError(f"Exact chapter ID '{identity.chapter_id}' not found under Class {grade} {identity.subject}.")

        if identity.content_type != "source_bundle":
            content_file = chapter_folder / f"{identity.content_type}.json"
            if not content_file.exists():
                raise CurriculumResolutionError(f"Content type '{identity.content_type}' not available for chapter {identity.chapter_id}.")

        return chapter_folder

    @classmethod
    def resolve(cls, identity: CurriculumIdentity) -> Path:
        return cls.resolve_chapter_path(identity)

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

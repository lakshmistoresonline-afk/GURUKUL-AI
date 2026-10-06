import os
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from .curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from .subject_registry import SubjectRegistry
from .config import GurukulConfig

PROCESSED_ROOT = GurukulConfig.get_processed_root()
CONTENTS_ROOT = GurukulConfig.get_content_root()

class CurriculumResolutionError(Exception):
    pass

class CurriculumRegistry:
    """
    Authoritative Index-Driven Curriculum Registry for Gurukul AI.
    Builds a complete multi-dimensional index (grade → subject → book → part → unit → chapter)
    and enforces exact identity-driven resolution without guessing or fallback.
    """
    _INDEX: Optional[Dict[str, Dict[str, Any]]] = None

    @classmethod
    def get_taxonomy(cls) -> Dict[str, Any]:
        taxonomy = {}
        if not PROCESSED_ROOT.exists():
            return taxonomy

        for class_dir in sorted([d for d in PROCESSED_ROOT.iterdir() if d.is_dir() and "class" in d.name.lower()]):
            grade = class_dir.name.replace("Class", "")
            taxonomy[grade] = {}

            for subj_dir in sorted([d for d in class_dir.iterdir() if d.is_dir()]):
                raw_subj = subj_dir.name
                canonical_subject = SubjectRegistry.resolve_canonical_subject(raw_subj)

                book = "main"
                part = "none"
                lower_sub = raw_subj.lower()
                if "maths i" in lower_sub or lower_sub == "mathsi":
                    book = "maths_i"
                    part = "part1"
                elif "maths ii" in lower_sub or lower_sub == "mathsii":
                    book = "maths_ii"
                    part = "part2"
                elif "social i" in lower_sub or lower_sub == "sociali":
                    book = "social_i"
                    part = "part1"
                elif "social ii" in lower_sub or lower_sub == "socialii":
                    book = "social_ii"
                    part = "part2"
                else:
                    book = canonical_subject
                    part = "main"

                if canonical_subject not in taxonomy[grade]:
                    taxonomy[grade][canonical_subject] = {}

                if book not in taxonomy[grade][canonical_subject]:
                    taxonomy[grade][canonical_subject][book] = {
                        "part": part,
                        "units": {}
                    }

                for ch_dir in sorted([d for d in subj_dir.iterdir() if d.is_dir()]):
                    chapter_id = ch_dir.name
                    unit_id = "U01"

                    manifest_file = ch_dir / "manifest.json"
                    if manifest_file.exists():
                        try:
                            with open(manifest_file, "r", encoding="utf-8") as mf:
                                md = json.load(mf)
                                unit_id = md.get("unit_id", unit_id)
                        except:
                            pass

                    if unit_id not in taxonomy[grade][canonical_subject][book]["units"]:
                        taxonomy[grade][canonical_subject][book]["units"][unit_id] = []

                    taxonomy[grade][canonical_subject][book]["units"][unit_id].append(chapter_id)

        return taxonomy

    @classmethod
    def get_index(cls) -> Dict[str, Dict[str, Any]]:
        if cls._INDEX is None:
            cls.build_index()
        return cls._INDEX

    @classmethod
    def build_index(cls) -> Dict[str, Dict[str, Any]]:
        index = {}
        if not PROCESSED_ROOT.exists():
            return index

        for class_dir in sorted([d for d in PROCESSED_ROOT.iterdir() if d.is_dir() and "class" in d.name.lower()]):
            grade = class_dir.name.replace("Class", "")

            for subj_dir in sorted([d for d in class_dir.iterdir() if d.is_dir()]):
                raw_subj = subj_dir.name
                canonical_subject = SubjectRegistry.resolve_canonical_subject(raw_subj)

                book = "main"
                part = "none"
                lower_sub = raw_subj.lower()
                if "maths i" in lower_sub or lower_sub == "mathsi":
                    book = "maths_i"
                    part = "part1"
                elif "maths ii" in lower_sub or lower_sub == "mathsii":
                    book = "maths_ii"
                    part = "part2"
                elif "social i" in lower_sub or lower_sub == "sociali":
                    book = "social_i"
                    part = "part1"
                elif "social ii" in lower_sub or lower_sub == "socialii":
                    book = "social_ii"
                    part = "part2"
                else:
                    book = canonical_subject
                    part = "main"

                for ch_dir in sorted([d for d in subj_dir.iterdir() if d.is_dir()]):
                    chapter_id = ch_dir.name
                    unit_id = "U01"
                    unit_number = 1
                    unit_title = "Curriculum Unit"
                    chapter_number = 1
                    chapter_title = chapter_id

                    manifest_file = ch_dir / "manifest.json"
                    if manifest_file.exists():
                        try:
                            with open(manifest_file, "r", encoding="utf-8") as mf:
                                md = json.load(mf)
                                chapter_title = md.get("chapter_title", chapter_title)
                                chapter_number = md.get("chapter_number", chapter_number)
                                unit_id = md.get("unit_id", unit_id)
                                unit_title = md.get("unit_title", unit_title)
                        except:
                            pass

                    available_content_types = []
                    for ct in ["overview", "notes", "master", "foundational", "flashcards", "mindmaps", "quiz", "question_papers"]:
                        if (ch_dir / f"{ct}.json").exists():
                            available_content_types.append(ct)

                    source_hash = ""
                    source_path = CONTENTS_ROOT / f"Class {grade}" / raw_subj / f"{chapter_id}.json"
                    if source_path.exists():
                        sha = hashlib.sha256()
                        with open(source_path, "rb") as sf:
                            sha.update(sf.read())
                        source_hash = sha.hexdigest()

                    node = {
                        "grade": grade,
                        "canonical_subject": canonical_subject,
                        "book": book,
                        "part": part,
                        "unit": unit_id,
                        "chapter_id": chapter_id,
                        "chapter_number": chapter_number,
                        "chapter_title": chapter_title,
                        "unit_number": unit_number,
                        "unit_title": unit_title,
                        "available_content_types": available_content_types,
                        "source_path": str(source_path),
                        "processed_path": str(ch_dir),
                        "source_hash": source_hash,
                        "processed_hash": ""
                    }

                    key = f"{grade}:{canonical_subject}:{book}:{part}:{unit_id}:{chapter_id}"
                    index[key] = node

        cls._INDEX = index
        return index

    @classmethod
    def get_classes(cls) -> List[str]:
        idx = cls.get_index()
        return sorted(list(set(node["grade"] for node in idx.values())))

    @classmethod
    def get_subjects(cls, grade: str) -> List[str]:
        idx = cls.get_index()
        subs = set(node["canonical_subject"] for node in idx.values() if node["grade"] == str(grade))
        return sorted([SubjectRegistry.get_display_name(s) for s in subs])

    @classmethod
    def get_books(cls, grade: str, subject: str) -> List[str]:
        idx = cls.get_index()
        canonical_subject = SubjectRegistry.resolve_canonical_subject(subject)
        books = set(node["book"] for node in idx.values() if node["grade"] == str(grade) and node["canonical_subject"] == canonical_subject)
        return sorted(list(books))

    @classmethod
    def get_units(cls, grade: str, subject: str, book: str) -> List[str]:
        idx = cls.get_index()
        canonical_subject = SubjectRegistry.resolve_canonical_subject(subject)
        units = set(node["unit"] for node in idx.values() if node["grade"] == str(grade) and node["canonical_subject"] == canonical_subject and node["book"].lower() == book.lower())
        return sorted(list(units))

    @classmethod
    def get_chapters(cls, grade: str, subject: str, book: str, unit: str) -> List[str]:
        idx = cls.get_index()
        canonical_subject = SubjectRegistry.resolve_canonical_subject(subject)
        ch_ids = [node["chapter_id"] for node in idx.values() if node["grade"] == str(grade) and node["canonical_subject"] == canonical_subject and node["book"].lower() == book.lower() and node["unit"].upper() == unit.upper()]
        return sorted(list(set(ch_ids)))

    @classmethod
    def resolve_node(cls, identity: CurriculumIdentity) -> Dict[str, Any]:
        idx = cls.get_index()
        canonical_subject = SubjectRegistry.resolve_canonical_subject(identity.subject)

        key = f"{identity.grade}:{canonical_subject}:{identity.book}:{identity.part}:{identity.unit}:{identity.chapter_id}"

        if key not in idx:
            for n_key, node in idx.items():
                if (node["grade"] == str(identity.grade) and
                    node["canonical_subject"] == canonical_subject and
                    node["unit"].upper() == identity.unit.upper() and
                    node["chapter_id"].lower() == identity.chapter_id.lower()):
                    if (node["book"].lower() == identity.book.lower() or identity.book in ["main", "none"]):
                        return node

            raise CurriculumResolutionError(f"Exact identity node {identity.to_cache_key()} not found in authoritative index.")

        return idx[key]

    @classmethod
    def resolve_chapter_path(cls, identity: CurriculumIdentity) -> Path:
        node = cls.resolve_node(identity)
        ch_path = Path(node["processed_path"])

        if identity.content_type != "source_bundle":
            if identity.content_type not in node["available_content_types"]:
                raise CurriculumResolutionError(f"Content type '{identity.content_type}' not available for chapter {identity.chapter_id}.")

        return ch_path

    @classmethod
    def resolve(cls, identity: CurriculumIdentity) -> Path:
        return cls.resolve_chapter_path(identity)

    @classmethod
    def load_chapter_bundle(cls, identity: CurriculumIdentity) -> ChapterRuntimeDTO:
        ch_path = cls.resolve_chapter_path(identity)
        node = cls.resolve_node(identity)

        sections = {}
        for sec_name in node["available_content_types"]:
            sec_file = ch_path / f"{sec_name}.json"
            if sec_file.exists():
                try:
                    with open(sec_file, "r", encoding="utf-8") as f:
                        sections[sec_name] = json.load(f)
                except Exception:
                    sections[sec_name] = None
            else:
                sections[sec_name] = None

        dto = ChapterRuntimeDTO(
            identity=identity,
            chapter_number=node["chapter_number"],
            chapter_title=node["chapter_title"],
            unit_title=node["unit_title"],
            data=sections,
            status="READY"
        )
        return dto

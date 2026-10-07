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

class ManifestMissingError(CurriculumResolutionError):
    """Raised when mandatory manifest.json is missing."""
    pass

class ManifestMalformedError(CurriculumResolutionError):
    """Raised when manifest.json contains malformed JSON or schema violation."""
    pass

class IdentityConflictError(CurriculumResolutionError):
    """Raised when identity dimensions conflict."""
    pass

class ChapterNotFoundError(CurriculumResolutionError):
    """Raised when chapter cannot be resolved."""
    pass

class ContentMissingError(CurriculumResolutionError):
    """Raised when a mandatory content section file is missing."""
    pass

class ContentNotFoundError(CurriculumResolutionError):
    """Raised when requested content type is not found."""
    pass

class ContentSchemaError(CurriculumResolutionError):
    """Raised when content JSON has malformed syntax or schema violation."""
    pass

class ContentCorruptError(CurriculumResolutionError):
    """Raised when content JSON is null, empty, or structurally corrupt."""
    pass

class RegistryDuplicateKeyError(CurriculumResolutionError):
    """Raised when duplicate index keys are detected."""
    pass

class SourceMismatchError(CurriculumResolutionError):
    """Raised when source hash mismatch occurs."""
    pass


class CurriculumRegistry:
    """
    Production-grade Authoritative Index-Driven Curriculum Registry for Gurukul AI.
    Enforces strict exact-identity resolution without synthetic defaults, guesswork, or fallbacks.
    """
    _INDEX: Optional[Dict[str, Dict[str, Any]]] = None

    @classmethod
    def get_taxonomy(cls) -> Dict[str, Any]:
        idx = cls.get_index()
        taxonomy = {}
        for node in idx.values():
            grade = node["grade"]
            subj = node["canonical_subject"]
            book = node["book"]
            part = node["part"]
            unit = node["unit"]
            ch_id = node["chapter_id"]

            if grade not in taxonomy:
                taxonomy[grade] = {}
            if subj not in taxonomy[grade]:
                taxonomy[grade][subj] = {}
            if book not in taxonomy[grade][subj]:
                taxonomy[grade][subj][book] = {
                    "part": part,
                    "units": {}
                }
            if unit not in taxonomy[grade][subj][book]["units"]:
                taxonomy[grade][subj][book]["units"][unit] = []
            if ch_id not in taxonomy[grade][subj][book]["units"][unit]:
                taxonomy[grade][subj][book]["units"][unit].append(ch_id)

        return taxonomy

    @classmethod
    def get_index(cls) -> Dict[str, Dict[str, Any]]:
        if cls._INDEX is None:
            cls.build_index()
        return cls._INDEX

    @classmethod
    def build_index(cls) -> Dict[str, Dict[str, Any]]:
        index = {}
        seen_keys = set()

        if not PROCESSED_ROOT.exists():
            cls._INDEX = index
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
                    manifest_file = ch_dir / "manifest.json"
                    if not manifest_file.exists():
                        raise ManifestMissingError(f"Mandatory manifest.json missing in chapter directory: {ch_dir}")

                    try:
                        with open(manifest_file, "r", encoding="utf-8") as mf:
                            md = json.load(mf)
                    except json.JSONDecodeError as jde:
                        raise ManifestMalformedError(f"Malformed JSON in manifest.json at {manifest_file}: {str(jde)}")
                    except Exception as e:
                        raise ManifestMalformedError(f"Failed to read manifest.json at {manifest_file}: {str(e)}")

                    m_grade = str(md.get("grade") or md.get("class") or grade)
                    m_subject = SubjectRegistry.resolve_canonical_subject(str(md.get("subject") or canonical_subject))
                    m_book = str(md.get("book") or book)
                    m_part = str(md.get("part") or part)
                    m_unit = str(md.get("unit_id") or md.get("unit") or ("U" + chapter_id.split("-U")[-1].split("-")[0] if "-U" in chapter_id else "U01"))
                    m_chapter_id = str(md.get("chapter_id") or md.get("id") or chapter_id)

                    if "chapter_number" not in md or "chapter_title" not in md:
                        raise ManifestMalformedError(f"Required chapter_number or chapter_title missing in manifest: {manifest_file}")

                    m_chapter_number = int(md["chapter_number"])
                    m_chapter_title = str(md["chapter_title"])
                    m_unit_number = int(md.get("unit_number") or (int(m_unit.replace("U", "")) if m_unit.startswith("U") else 1))
                    m_unit_title = str(md.get("unit_title") or f"Unit {m_unit}")
                    m_source_hash = str(md.get("source_hash") or "")

                    available_content_types = []
                    for ct in ["overview", "notes", "master", "foundational", "flashcards", "mindmaps", "quiz", "question_papers"]:
                        if (ch_dir / f"{ct}.json").exists():
                            available_content_types.append(ct)

                    source_path = CONTENTS_ROOT / f"Class {m_grade}" / raw_subj / f"{m_chapter_id}.json"
                    node = {
                        "grade": m_grade,
                        "canonical_subject": m_subject,
                        "book": m_book,
                        "part": m_part,
                        "unit": m_unit,
                        "chapter_id": m_chapter_id,
                        "chapter_number": m_chapter_number,
                        "chapter_title": m_chapter_title,
                        "unit_number": m_unit_number,
                        "unit_title": m_unit_title,
                        "available_content_types": available_content_types,
                        "source_path": str(source_path),
                        "processed_path": str(ch_dir),
                        "source_hash": m_source_hash,
                        "processed_hash": ""
                    }

                    key = f"{m_grade}:{m_subject}:{m_book}:{m_part}:{m_unit}:{m_chapter_id}"
                    if key in seen_keys:
                        raise RegistryDuplicateKeyError(f"Duplicate index key detected in CurriculumRegistry: {key}")
                    seen_keys.add(key)
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
            raise ChapterNotFoundError(f"Exact identity node {identity.to_cache_key()} not found in authoritative index.")

        return idx[key]

    @classmethod
    def resolve_chapter_path(cls, identity: CurriculumIdentity) -> Path:
        node = cls.resolve_node(identity)
        ch_path = Path(node["processed_path"])

        if identity.content_type != "source_bundle":
            if identity.content_type not in node["available_content_types"]:
                raise ContentNotFoundError(f"Content type '{identity.content_type}' not available for chapter {identity.chapter_id}.")

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
            if not sec_file.exists():
                raise ContentMissingError(f"Mandatory content section file '{sec_name}.json' missing for chapter {identity.chapter_id}.")
            try:
                with open(sec_file, "r", encoding="utf-8") as f:
                    content_json = json.load(f)
                    if content_json is None:
                        raise ContentCorruptError(f"Content section '{sec_name}.json' evaluated to null/None for chapter {identity.chapter_id}.")
                    sections[sec_name] = content_json
            except json.JSONDecodeError as jde:
                raise ContentSchemaError(f"Corrupt or malformed JSON in content section '{sec_name}.json' for chapter {identity.chapter_id}: {str(jde)}")
            except (ContentMissingError, ContentCorruptError, ContentSchemaError):
                raise
            except Exception as e:
                raise ContentCorruptError(f"Unexpected error loading content section '{sec_name}.json' for chapter {identity.chapter_id}: {str(e)}")

        dto = ChapterRuntimeDTO(
            identity=identity,
            chapter_number=node["chapter_number"],
            chapter_title=node["chapter_title"],
            unit_title=node["unit_title"],
            data=sections,
            status="READY"
        )
        return dto

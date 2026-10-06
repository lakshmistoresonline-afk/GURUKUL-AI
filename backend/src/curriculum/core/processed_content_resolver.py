import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from .subject_registry import SubjectRegistry
from .config import GurukulConfig
from .content_validator import ContentValidator, ContentNotFoundError, ContentSchemaError, IdentityConflictError

PROCESSED_ROOT = GurukulConfig.get_processed_root()

class ContentIntegrityError(Exception):
    """Raised when a processed content file contains malformed JSON or schema issues (HTTP 500/422)."""
    pass

class ChapterNotFoundError(Exception):
    """Raised when the target chapter folder does not exist (HTTP 404)."""
    pass

class ProcessedContentResolver:
    """
    Hardened Authoritative ProcessedContent Resolver for Gurukul AI.
    Replaces silent failures with explicit schema validation and precise error statuses (404, 409, 422, 500).
    """

    @classmethod
    def resolve_content(cls, identity: CurriculumIdentity) -> Dict[str, Any]:
        if not identity.grade or not identity.subject or not identity.book or not identity.unit or not identity.chapter_id or not identity.content_type:
            raise ValueError("All identity dimensions (grade, subject, book, part, unit, chapter_id, content_type) are strictly required.")

        canonical_subject = SubjectRegistry.resolve_canonical_subject(identity.subject)
        class_dir = PROCESSED_ROOT / f"Class{identity.grade}"
        if not class_dir.exists():
            raise ChapterNotFoundError(f"Class {identity.grade} processed directory not found.")

        target_subj_dir = None
        for sub_d in class_dir.iterdir():
            if sub_d.is_dir() and SubjectRegistry.resolve_canonical_subject(sub_d.name) == canonical_subject:
                if identity.book != "main" and identity.book != "none" and identity.book.lower() not in sub_d.name.lower():
                    continue
                target_subj_dir = sub_d
                break

        if not target_subj_dir:
            raise ChapterNotFoundError(f"Subject '{identity.subject}' (book: {identity.book}) not found in Class {identity.grade}.")

        chapter_dir = target_subj_dir / identity.chapter_id
        if not chapter_dir.exists() or not chapter_dir.is_dir():
            raise ChapterNotFoundError(f"Chapter '{identity.chapter_id}' not found under Class {identity.grade} {identity.subject}.")

        # Validate manifest metadata against request identity (raises 409 IdentityConflictError if mismatch)
        ContentValidator.validate_manifest(chapter_dir, identity)

        if identity.content_type == "source_bundle":
            sections = {}
            for sec_name in ["overview", "notes", "master", "flashcards", "mindmaps", "quiz", "question_papers", "foundational"]:
                sec_file = chapter_dir / f"{sec_name}.json"
                if sec_file.exists():
                    try:
                        sections[sec_name] = ContentValidator.validate_content_file(sec_file, identity)
                    except Exception as e:
                        raise ContentIntegrityError(str(e))
                else:
                    sections[sec_name] = None
            return sections

        content_file = chapter_dir / f"{identity.content_type}.json"
        try:
            return ContentValidator.validate_content_file(content_file, identity)
        except (ContentNotFoundError, ContentSchemaError):
            raise
        except Exception as e:
            raise ContentIntegrityError(str(e))

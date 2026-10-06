import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .curriculum_identity import CurriculumIdentity, ChapterRuntimeDTO
from .subject_registry import SubjectRegistry

PROCESSED_ROOT = Path(r"D:/GURUKUL/ProcessedContent")

class ContentIntegrityError(Exception):
    """Raised when a processed content file contains malformed JSON (HTTP 500)."""
    pass

class ContentNotFoundError(Exception):
    """Raised when a specific content type file does not exist (HTTP 404)."""
    pass

class ChapterNotFoundError(Exception):
    """Raised when the target chapter folder does not exist (HTTP 404)."""
    pass

class ProcessedContentResolver:
    """
    Single Authoritative ProcessedContent Resolver for Gurukul AI.
    Enforces exact identity resolution without filesystem guessing,
    subject folder special cases, or default fallbacks.
    """

    @classmethod
    def resolve_content(cls, identity: CurriculumIdentity) -> Dict[str, Any]:
        if not identity.grade or not identity.subject or not identity.book or not identity.unit or not identity.chapter_id or not identity.content_type:
            raise ValueError("All identity dimensions (grade, subject, book, part, unit, chapter_id, content_type) are strictly required.")

        canonical_subject = SubjectRegistry.resolve_canonical_subject(identity.subject)
        class_dir = PROCESSED_ROOT / f"Class{identity.grade}"
        if not class_dir.exists():
            raise ChapterNotFoundError(f"Class {identity.grade} directory not found.")

        # Locate exact subject folder without guessing
        target_subj_dir = None
        for sub_d in class_dir.iterdir():
            if sub_d.is_dir() and SubjectRegistry.resolve_canonical_subject(sub_d.name) == canonical_subject:
                # If book/part is specified and is not 'main' or 'none', require match in folder name
                if identity.book != "main" and identity.book != "none" and identity.book.lower() not in sub_d.name.lower():
                    continue
                target_subj_dir = sub_d
                break

        if not target_subj_dir:
            raise ChapterNotFoundError(f"Subject '{identity.subject}' (book: {identity.book}) not found in Class {identity.grade}.")

        chapter_dir = target_subj_dir / identity.chapter_id
        if not chapter_dir.exists() or not chapter_dir.is_dir():
            raise ChapterNotFoundError(f"Chapter '{identity.chapter_id}' not found under Class {identity.grade} {identity.subject}.")

        content_file = chapter_dir / f"{identity.content_type}.json"
        if not content_file.exists():
            raise ContentNotFoundError(f"Content type '{identity.content_type}' not available for chapter {identity.chapter_id}.")

        try:
            with open(content_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError as jde:
            raise ContentIntegrityError(f"Malformed JSON in content file {content_file}: {str(jde)}")
        except Exception as e:
            raise ContentIntegrityError(f"Unexpected error reading content file {content_file}: {str(e)}")

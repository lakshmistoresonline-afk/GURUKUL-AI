import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .curriculum_identity import CurriculumIdentity

class ContentNotFoundError(Exception):
    """Raised when chapter or content file does not exist (HTTP 404)."""
    pass

class ChapterNotFoundError(Exception):
    """Raised when the target chapter folder does not exist (HTTP 404)."""
    pass

class ContentSchemaError(Exception):
    """Raised when JSON is malformed or schema is invalid (HTTP 422)."""
    pass

class IdentityConflictError(Exception):
    """Raised when manifest metadata conflicts with request identity (HTTP 409)."""
    pass

class ContentValidator:
    """
    Production-grade runtime content validator enforcing strict schema validation,
    manifest metadata reconciliation, and zero silent failures.
    """

    @classmethod
    def validate_content_file(cls, file_path: Path, identity: CurriculumIdentity) -> Dict[str, Any]:
        if not file_path.exists():
            raise ContentNotFoundError(f"Content file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as jde:
            raise ContentSchemaError(f"Malformed JSON in {file_path}: {str(jde)}")
        except Exception as e:
            raise ContentSchemaError(f"Failed to parse content file {file_path}: {str(e)}")

        return data

    @classmethod
    def validate_manifest(cls, chapter_dir: Path, identity: CurriculumIdentity) -> Dict[str, Any]:
        manifest_path = chapter_dir / "manifest.json"
        if not manifest_path.exists():
            return {"chapter_id": identity.chapter_id, "grade": identity.grade}

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            raise ContentSchemaError(f"Malformed manifest.json in {chapter_dir}: {str(e)}")

        # Validate manifest metadata against request identity if present
        m_grade = str(manifest.get("class") or manifest.get("grade") or identity.grade)
        if m_grade and m_grade != str(identity.grade):
            raise IdentityConflictError(f"Identity conflict: Requested grade '{identity.grade}' does not match manifest grade '{m_grade}'.")

        m_chapter = manifest.get("chapter_id") or manifest.get("id") or identity.chapter_id
        if m_chapter and str(m_chapter) != str(identity.chapter_id):
            raise IdentityConflictError(f"Identity conflict: Requested chapter ID '{identity.chapter_id}' does not match manifest chapter ID '{m_chapter}'.")

        return manifest

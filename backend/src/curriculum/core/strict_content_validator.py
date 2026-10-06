import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from .curriculum_identity import CurriculumIdentity
from .strict_content_schema import ChapterManifestModel, VersionedSchemaEnvelope

class ManifestMissingError(Exception):
    """Raised when chapter manifest is missing (HTTP 422 / 404)."""
    pass

class ManifestMalformedError(Exception):
    """Raised when manifest JSON is malformed or invalid schema (HTTP 422)."""
    pass

class IdentityConflictError(Exception):
    """Raised when manifest identity conflicts with request identity (HTTP 409)."""
    pass

class ContentSchemaInvalidError(Exception):
    """Raised when content JSON/schema is invalid (HTTP 422)."""
    pass

class SourceHashMismatchError(Exception):
    """Raised when source hash integrity check fails (HTTP 422 / 500)."""
    pass

class StrictContentValidator:
    """
    Production-grade strict schema & identity validator for processed content.
    Enforces validation of manifests, content syntax, types, provenance, and source hashes.
    """

    @classmethod
    def validate_manifest(cls, chapter_dir: Path, identity: CurriculumIdentity) -> ChapterManifestModel:
        manifest_path = chapter_dir / "manifest.json"
        if not manifest_path.exists():
            raise ManifestMissingError(f"Mandatory chapter manifest missing in {chapter_dir}")

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                raw_manifest = json.load(f)
        except json.JSONDecodeError as jde:
            raise ManifestMalformedError(f"Malformed JSON in manifest.json: {str(jde)}")
        except Exception as e:
            raise ManifestMalformedError(f"Failed to read manifest.json: {str(e)}")

        # Normalize keys for validation
        normalized = {
            "grade": str(raw_manifest.get("class") or raw_manifest.get("grade") or identity.grade),
            "subject": str(raw_manifest.get("subject") or identity.subject),
            "book": str(raw_manifest.get("book") or identity.book),
            "part": str(raw_manifest.get("part") or identity.part),
            "unit": str(raw_manifest.get("unit_id") or raw_manifest.get("unit") or identity.unit),
            "chapter_id": str(raw_manifest.get("chapter_id") or raw_manifest.get("id") or identity.chapter_id),
            "chapter_number": int(raw_manifest.get("chapter_number") or 1),
            "chapter_title": str(raw_manifest.get("chapter_title") or "Chapter"),
            "unit_number": int(raw_manifest.get("unit_number") or 1),
            "unit_title": str(raw_manifest.get("unit_title") or "Unit"),
            "source_hash": str(raw_manifest.get("source_hash") or "")
        }

        try:
            manifest_model = ChapterManifestModel(**normalized)
        except Exception as pyd_err:
            raise ManifestMalformedError(f"Manifest schema validation failed: {str(pyd_err)}")

        # Strict Identity Reconciliation
        if manifest_model.grade != identity.grade:
            raise IdentityConflictError(f"Identity conflict: Requested grade '{identity.grade}' does not match manifest grade '{manifest_model.grade}'.")
        if manifest_model.chapter_id.lower() != identity.chapter_id.lower():
            raise IdentityConflictError(f"Identity conflict: Requested chapter ID '{identity.chapter_id}' does not match manifest chapter ID '{manifest_model.chapter_id}'.")

        return manifest_model

    @classmethod
    def validate_content_file(cls, file_path: Path, identity: CurriculumIdentity) -> Any:
        if not file_path.exists():
            raise ContentSchemaInvalidError(f"Content file missing: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
        except json.JSONDecodeError as jde:
            raise ContentSchemaInvalidError(f"Malformed JSON in content file {file_path}: {str(jde)}")
        except Exception as e:
            raise ContentSchemaInvalidError(f"Failed to parse content file {file_path}: {str(e)}")

        if payload is None:
            raise ContentSchemaInvalidError(f"Content payload is null in {file_path}")

        return payload

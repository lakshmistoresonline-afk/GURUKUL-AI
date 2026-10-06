import os
import sys
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Tuple
from ..core.config import GurukulConfig

CONTENTS_ROOT = GurukulConfig.get_content_root()
PROCESSED_ROOT = GurukulConfig.get_processed_root()
INTEGRITY_DIR = GurukulConfig.get_reports_root() / "content-integrity"
INTEGRITY_DIR.mkdir(parents=True, exist_ok=True)

BASELINE_PATH = INTEGRITY_DIR / "production_contents_baseline.json"
REPRODUCIBILITY_PATH = INTEGRITY_DIR / "processed_reproducibility_manifest.json"

class ImmutabilityViolationError(Exception):
    """Raised when Contents/ has been modified, deleted, or appended."""
    pass

class MissingBaselineError(Exception):
    """Raised when the immutable baseline manifest is missing (must fail, never auto-create)."""
    pass

class ProductionImmutabilityManager:
    """
    Production-grade immutability verifier for Contents/ and reproducibility manifest for ProcessedContent/.
    Never creates a baseline automatically during verification.
    """

    @classmethod
    def compute_file_metadata(cls, f_abs: Path, root_dir: Path) -> Dict[str, Any]:
        rel_path = str(f_abs.relative_to(root_dir))
        file_size = f_abs.stat().st_size
        file_type = f_abs.suffix.lower()
        sha = hashlib.sha256()
        with open(f_abs, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                sha.update(chunk)
        return {
            "relative_path": rel_path,
            "file_size": file_size,
            "file_type": file_type,
            "sha256": sha.hexdigest()
        }

    @classmethod
    def create_source_baseline(cls) -> Dict[str, Any]:
        """
        Explicit command: create_source_baseline.
        Run intentionally by administrator/developer to record the trusted immutable source state.
        """
        manifest = {
            "created_at": datetime.now().isoformat(),
            "root": "Contents",
            "files": {}
        }
        if CONTENTS_ROOT.exists():
            for root, dirs, files in os.walk(CONTENTS_ROOT):
                for file in files:
                    if file.endswith((".json", ".pdf", ".txt", ".md")):
                        f_abs = Path(root) / file
                        meta = cls.compute_file_metadata(f_abs, CONTENTS_ROOT)
                        manifest["files"][meta["relative_path"]] = meta

        with open(BASELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        return manifest

    @classmethod
    def verify_contents_immutability(cls) -> Tuple[bool, str]:
        """
        Normal CI/runtime verification command.
        NEVER creates or replaces the baseline. Fails if missing, modified, deleted, or added.
        """
        if not BASELINE_PATH.exists():
            return False, "FAIL: Baseline missing. Normal verification must never auto-create baseline."

        with open(BASELINE_PATH, "r", encoding="utf-8") as f:
            baseline = json.load(f)

        baseline_files = baseline.get("files", {})

        current_files = {}
        if CONTENTS_ROOT.exists():
            for root, dirs, files in os.walk(CONTENTS_ROOT):
                for file in files:
                    if file.endswith((".json", ".pdf", ".txt", ".md")):
                        f_abs = Path(root) / file
                        meta = cls.compute_file_metadata(f_abs, CONTENTS_ROOT)
                        current_files[meta["relative_path"]] = meta

        b_keys = set(baseline_files.keys())
        c_keys = set(current_files.keys())

        deleted = b_keys - c_keys
        if deleted:
            return False, f"FAIL: Protected files deleted: {list(deleted)}"

        added = c_keys - b_keys
        if added:
            return False, f"FAIL: New unverified files added to protected Contents/: {list(added)}"

        for path in b_keys:
            b_meta = baseline_files[path]
            c_meta = current_files[path]
            if b_meta["sha256"] != c_meta["sha256"] or b_meta["file_size"] != c_meta["file_size"]:
                return False, f"FAIL: Protected file modified: {path}"

        return True, "PASS: Contents/ is 100% immutable and unchanged."

    @classmethod
    def generate_reproducibility_manifest(cls) -> Dict[str, Any]:
        source_hashes_combined = hashlib.sha256()
        if BASELINE_PATH.exists():
            with open(BASELINE_PATH, "rb") as f:
                source_hashes_combined.update(f.read())

        manifest = {
            "timestamp": datetime.now().isoformat(),
            "source_hash": source_hashes_combined.hexdigest(),
            "processor_version": "V14-STRICT",
            "schema_version": "3.0.0",
            "output_hash": cls.compute_output_hash()
        }

        with open(REPRODUCIBILITY_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        return manifest

    @classmethod
    def compute_output_hash(cls) -> str:
        sha = hashlib.sha256()
        if PROCESSED_ROOT.exists():
            for root, dirs, files in os.walk(PROCESSED_ROOT):
                for file in files:
                    if file.endswith(".json"):
                        f_abs = Path(root) / file
                        with open(f_abs, "rb") as f:
                            sha.update(f.read())
        return sha.hexdigest()

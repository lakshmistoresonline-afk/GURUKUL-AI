import os
import json
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from ..config.app_config import settings

logger = logging.getLogger(__name__)

class StagingManager:
    """
    Manages the separate generation output / staging area.
    Ensures all newly generated content is isolated from production files.
    """

    def __init__(self, run_id: Optional[str] = None):
        self.run_id = run_id or settings.GENERATION_RUN_ID
        self.run_dir = os.path.join(settings.STAGING_PATH, self.run_id)
        self.manifest_path = os.path.join(self.run_dir, "GENERATION_MANIFEST.json")
        self.progress_path = os.path.join(self.run_dir, "GENERATION_PROGRESS.json")

        # Ensure run directory exists
        os.makedirs(self.run_dir, exist_ok=True)
        self._init_metadata()

    def _init_metadata(self):
        """Initializes manifest and progress files if they don't exist."""
        git_commit = "unknown"
        try:
            import subprocess
            git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        except:
            pass

        if not os.path.exists(self.manifest_path):
            manifest = {
                "run_id": self.run_id,
                "timestamp": datetime.utcnow().isoformat(),
                "git_commit": git_commit,
                "orchestrator_version": "1.0.0",
                "generated_files": []
            }
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)

        if not os.path.exists(self.progress_path):
            progress = {
                "run_id": self.run_id,
                "status": "STARTED",
                "completed_chapters": [],
                "failed_chapters": []
            }
            with open(self.progress_path, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2)

    def get_chapter_staging_dir(self, class_name: str, subject: str, chapter_id: str) -> str:
        """Returns the isolated staging path for a specific chapter."""
        def sanitize(s: str) -> str:
            if not s: return "unknown"
            return "".join([c for c in s if c.isalnum() or c in (" ", "-", "_")]).strip().replace(" ", "_")

        path = os.path.join(
            self.run_dir,
            sanitize(class_name),
            sanitize(subject),
            sanitize(chapter_id)
        )
        os.makedirs(path, exist_ok=True)
        return path

    def record_generated_file(self, metadata: Dict[str, Any]):
        """Records a new generated file in the manifest."""
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        manifest["generated_files"].append({
            **metadata,
            "recorded_at": datetime.utcnow().isoformat()
        })

        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)

    def update_progress(self, chapter_id: str, success: bool, error: Optional[str] = None):
        """Updates the generation progress."""
        with open(self.progress_path, 'r', encoding='utf-8') as f:
            progress = json.load(f)

        if success:
            if chapter_id not in progress["completed_chapters"]:
                progress["completed_chapters"].append(chapter_id)
            progress["failed_chapters"] = [c for c in progress["failed_chapters"] if c["id"] != chapter_id]
        else:
            progress["failed_chapters"].append({
                "id": chapter_id,
                "error": error,
                "timestamp": datetime.utcnow().isoformat()
            })

        with open(self.progress_path, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2)

    @staticmethod
    def calculate_hash(file_path: str) -> str:
        """Calculates SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def audit_production_content(self) -> Dict[str, Any]:
        """
        Scans production content and returns metadata for comparison.
        Does NOT modify any files.
        """
        production_root = settings.MASTER_CONTENT_ROOT
        audit_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "root": production_root,
            "files": []
        }

        for root, _, files in os.walk(production_root):
            for file in files:
                if file.endswith('.json'):
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, production_root)
                    audit_report["files"].append({
                        "rel_path": rel_path,
                        "hash": self.calculate_hash(abs_path),
                        "modified_at": os.path.getmtime(abs_path),
                        "size": os.path.getsize(abs_path)
                    })

        audit_file = os.path.join(self.run_dir, "PRODUCTION_AUDIT_PRE_GEN.json")
        with open(audit_file, 'w', encoding='utf-8') as f:
            json.dump(audit_report, f, indent=2)

        return audit_report

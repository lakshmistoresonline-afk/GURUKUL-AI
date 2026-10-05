import os
import hashlib
import json
from typing import Dict, str

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")

class ContentImmutabilityAuditor:
    """
    Enforces the Absolute Requirement: Authoritative source content in Contents/
    must remain 100% immutable (SHA-256 hash BEFORE == AFTER).
    """

    @classmethod
    def compute_directory_hashes(cls, root_dir: str) -> Dict[str, str]:
        hashes = {}
        if not os.path.exists(root_dir):
            return hashes
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".json") or file.endswith(".pdf"):
                    f_abs = os.path.join(root, file)
                    rel_path = os.path.relpath(f_abs, root_dir)
                    sha = hashlib.sha256()
                    try:
                        with open(f_abs, "rb") as f:
                            while True:
                                chunk = f.read(8192)
                                if not chunk:
                                    break
                                sha.update(chunk)
                        hashes[rel_path] = sha.hexdigest()
                    except Exception as e:
                        hashes[rel_path] = f"ERROR: {e}"
        return hashes

    @classmethod
    def verify_immutability(cls, baseline_hashes: Dict[str, str]) -> bool:
        current_hashes = cls.compute_directory_hashes(CONTENTS_ROOT)
        if len(baseline_hashes) != len(current_hashes):
            return False
        for path, baseline_sha in baseline_hashes.items():
            if current_hashes.get(path) != baseline_sha:
                return False
        return True

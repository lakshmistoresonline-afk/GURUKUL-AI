import os
import json
import logging
import re
from typing import Optional, Dict, Any, List
from functools import lru_cache

from ..config.app_config import settings

logger = logging.getLogger(__name__)


class PathResolver:
    """
    Resolves canonical curriculum identifiers to filesystem paths
    in the FINAL MASTER CONTENT package.

    Canonical examples:
      class_6 + english + unit_01
      class_6 + mathematics + chapter_01
    """

    @staticmethod
    @lru_cache(maxsize=4)
    def _get_master_index(class_id: str) -> Optional[Dict[str, Any]]:
        # Pad class_id to 2 digits for folder name (e.g. class_05)
        padded_id = class_id.zfill(2)
        possible_folders = [f"class_{padded_id}", f"Class {class_id}", f"class_{class_id}", str(class_id)]

        for folder in possible_folders:
            folder_path = os.path.join(settings.MASTER_CONTENT_ROOT, folder)
            if not os.path.exists(folder_path):
                continue

            # Look for index in subject subfolders or root
            index_file = os.path.join(folder_path, "master_index.json")
            if not os.path.exists(index_file):
                 index_file = os.path.join(folder_path, f"Class_{class_id}_Master_Index.json")

            if os.path.exists(index_file):
                try:
                    with open(index_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        return data
                except Exception as e:
                    logger.error(f"PathResolver: Error loading index {index_file}: {e}")

        logger.warning(f"PathResolver: Master index not found for class_id {class_id} in {settings.MASTER_CONTENT_ROOT}")
        return None

    @staticmethod
    def extract_class_id(class_name: str) -> str:
        """Return numeric class ID from class_5, Class 5, or 5."""
        if class_name is None:
             return ""

        val = str(class_name).strip().lower()
        if not val:
            return ""

        match = re.search(r"(\d+)", val)
        if match:
            return match.group(1)

        val = val.replace("class", "").replace("_", " ").strip()
        val = val.split()[0] if val else ""

        if not val.isdigit():
             # Only log warning if class_name was actually something non-empty but unrecognizable
             if val:
                  logger.warning(f"PathResolver: Could not extract class ID from {class_name}")
             return ""

        return val

    @staticmethod
    def normalize_chapter_id(class_name: str, chapter_id: str, subject: Optional[str] = None) -> str:
        """
        Maps legacy IDs (e.g. fepr101, eesa101) to canonical IDs (e.g. unit_01, e05_c1).
        """
        cid = str(chapter_id).strip().lower()
        class_id = PathResolver.extract_class_id(class_name)

        if class_id == "5":
            # eesa101 -> e05_c1
            if cid.startswith('eesa') and len(cid) >= 7: return f"e05_c{int(cid[-3:])%100}"
            if cid.startswith('eeev') and len(cid) >= 7: return f"evs05_c{int(cid[-3:])%100}"
            if cid.startswith('ehve') and len(cid) >= 7: return f"h05_c{int(cid[-3:])%100}"
            if cid.startswith('eemm') and len(cid) >= 7: return f"m05_c{int(cid[-3:])%100}"

        if class_id == "6":
            # Class 6 English: fepr101 -> unit_01
            if (cid.startswith('fepr') or (subject and subject.lower() == 'english' and cid.startswith('fe'))) and len(cid) >= 7:
                num_part = cid[-2:]
                if num_part.isdigit(): return f"unit_{num_part}"

            # Class 6 Others: fegp101, fesc101 -> chapter_01
            if cid.startswith('fe') and len(cid) >= 7:
                num_part = cid[-2:]
                if num_part.isdigit(): return f"chapter_{num_part}"

        if class_id == "7":
            # c7_english_001 -> e07_c1
            if cid.startswith('c7_') and len(cid) >= 12:
                parts = cid.split('_')
                if len(parts) == 3 and parts[2].isdigit():
                    num = int(parts[2])
                    subj = parts[1].lower()
                    prefix = {"english": "e", "hindi": "h", "mathematics": "m", "science": "s", "social_science": "ss"}.get(subj, "x")
                    return f"{prefix}07_c{num}"

        return cid

    @staticmethod
    def get_chapter_path(
        class_name: str,
        chapter_id: str,
        subject: Optional[str] = None,
    ) -> Optional[str]:
        """
        Resolve a chapter directory from the master index.

        If subject is supplied, chapter ID must belong to that subject.
        This is essential because IDs such as chapter_01 can occur in
        multiple subjects within the same class.
        """
        class_id = PathResolver.extract_class_id(class_name)
        index = PathResolver._get_master_index(class_id)

        if not index:
            return None

        normalized_subject = subject.strip().lower() if subject else None

        # Apply normalization to the requested chapter_id
        canonical_chapter = PathResolver.normalize_chapter_id(class_name, chapter_id, subject=subject)
        normalized_chapter = canonical_chapter.strip().lower()

        for chapter in index.get("chapters", []):
            indexed_id = str(chapter.get("chapterId", "")).strip().lower()
            indexed_subject = str(chapter.get("subject", "")).strip().lower()

            if indexed_id == normalized_chapter:
                if not normalized_subject or indexed_subject == normalized_subject:
                    rel_path = chapter.get("path")
                    if rel_path:
                        # Join with the class-specific directory
                        padded_id = class_id.zfill(2)
                        class_folder = f"class_{padded_id}"
                        resolved_path = os.path.join(settings.MASTER_CONTENT_ROOT, class_folder, os.path.dirname(rel_path))
                        return resolved_path

        logger.warning(f"PathResolver: Could not resolve chapter path for {chapter_id} (normalized as {normalized_chapter}) in Class {class_id} {subject or ''}")
        return None

    @staticmethod
    def get_class_hierarchy(
        class_name: str,
    ) -> Dict[str, List[Dict[str, Any]]]:
        class_id = PathResolver.extract_class_id(class_name)
        index = PathResolver._get_master_index(class_id)

        if not index:
            return {}

        hierarchy: Dict[str, List[Dict[str, Any]]] = {}

        for chapter in index.get("chapters", []):
            subj = str(chapter.get("subject", "unknown")).strip().lower()

            if subj not in hierarchy:
                hierarchy[subj] = []

            hierarchy[subj].append(
                {
                    "id": chapter.get("chapterId"),
                    "name": chapter.get("chapterName"),
                    "part": chapter.get("part"),
                    "number": chapter.get("chapterNumber"),
                }
            )

        for subj in hierarchy:
            hierarchy[subj].sort(
                key=lambda x: (
                    str(x.get("part") or ""),
                    int(x.get("number") or 0),
                )
            )

        return hierarchy

    @staticmethod
    def get_subject_list(class_name: str) -> List[str]:
        class_id = PathResolver.extract_class_id(class_name)
        index = PathResolver._get_master_index(class_id)

        if not index:
            return []

        return index.get("subjects", [])

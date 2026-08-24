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
        Maps IDs to canonical IDs used in the Master Index.
        With V3 content, we prefer the IDs supplied in the packages (e.g. fepr101).
        """
        cid = str(chapter_id).strip().lower()
        return cid

    @staticmethod
    def get_chapter_path(
        class_name: str,
        chapter_id: str,
        subject: Optional[str] = None,
    ) -> Optional[str]:
        """Returns the directory of a chapter."""
        pkg_path = PathResolver.get_chapter_package_path(class_name, chapter_id, subject=subject)
        if pkg_path:
            return os.path.dirname(pkg_path)
        return None

    @staticmethod
    def get_chapter_package_path(
        class_name: str,
        chapter_id: str,
        subject: Optional[str] = None,
    ) -> Optional[str]:
        """
        Resolve the full absolute path to the chapter's package.json or chapter_package.json.
        """
        class_id = PathResolver.extract_class_id(class_name)
        index = PathResolver._get_master_index(class_id)

        if not index:
            return None

        normalized_subject = subject.strip().lower().replace("_", " ") if subject else None
        canonical_chapter = PathResolver.normalize_chapter_id(class_name, chapter_id, subject=subject)
        normalized_chapter = canonical_chapter.strip().lower()

        for chapter in index.get("chapters", []):
            indexed_id = str(chapter.get("chapterId", "")).strip().lower()
            indexed_subject = str(chapter.get("subject", "")).strip().lower().replace("_", " ")

            if indexed_id == normalized_chapter:
                if not normalized_subject or indexed_subject == normalized_subject:
                    rel_path = chapter.get("path")
                    if rel_path:
                        padded_id = class_id.zfill(2)
                        class_folder = f"class_{padded_id}"
                        resolved_path = os.path.normpath(os.path.join(settings.MASTER_CONTENT_ROOT, class_folder, rel_path))

                        # Detect potential ambiguity/duplicate folders
                        parent_dir = os.path.dirname(resolved_path)
                        subject_dir = os.path.dirname(parent_dir)
                        if os.path.exists(subject_dir):
                            tech_id_folder = os.path.join(subject_dir, indexed_id)
                            if os.path.exists(tech_id_folder) and os.path.abspath(tech_id_folder) != os.path.abspath(parent_dir):
                                logger.warning(f"PathResolver: Detected ambiguity for {indexed_id}. "
                                             f"Index points to '{parent_dir}', but a legacy folder '{tech_id_folder}' also exists. "
                                             f"Strictly adhering to Index.")

                        if os.path.exists(resolved_path):
                            return resolved_path

                        # Fallback: try different filenames if the index path is slightly off
                        base_dir = os.path.dirname(resolved_path)
                        for fname in ["chapter_package.json", "package.json"]:
                            alt_path = os.path.join(base_dir, fname)
                            if os.path.exists(alt_path):
                                logger.info(f"PathResolver: Found package at alternate location: {alt_path}")
                                return alt_path

        logger.error(f"PathResolver: Could not resolve package for {chapter_id} (Subject: {subject}) in Class {class_name}")
        return None

    @staticmethod
    def get_class_hierarchy(
        class_name: str,
    ) -> Dict[str, List[Dict[str, Any]]]:
        class_id = PathResolver.extract_class_id(class_name)
        index = PathResolver._get_master_index(class_id)

        if not index:
            logger.error(f"PathResolver: Master index not found for Class {class_id} (input: {class_name})")
            return {}

        hierarchy: Dict[str, List[Dict[str, Any]]] = {}

        chapters = index.get("chapters", [])
        if not chapters:
            logger.warning(f"PathResolver: Index found but contains no chapters for Class {class_id}")

        for chapter in chapters:
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

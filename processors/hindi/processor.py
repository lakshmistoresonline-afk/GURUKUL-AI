import json
import re
from pathlib import Path
from typing import Any
from ..common.pipeline import BaseSubjectProcessor
from ..common.json_utils import read_json_utf8, write_json_utf8
from ..common.hashing import calculate_text_hash
from ..common.logging import get_pipeline_logger

logger = get_pipeline_logger("HindiSubjectProcessor")

class HindiSubjectProcessor(BaseSubjectProcessor):
    def __init__(self, context=None, profile=None):
        super().__init__("Hindi", context, profile)

    def process_package(self, package_dir: Path, output_dir: Path) -> dict[str, Any]:
        if not self.context:
            raise ValueError("HindiSubjectProcessor requires a ProcessingContext.")
        if not self.profile:
            raise ValueError("HindiSubjectProcessor requires a SourceProfile.")

        logger.info(f"Processing Hindi package for Class {self.context.class_level} ({self.profile.book}) (Devanagari Unicode Safe) at: {package_dir}")
        chapters_processed = []

        class_id = f"class_{self.context.class_level}"
        subject_id = self.context.subject.lower()
        source_pkg = self.context.source_package

        for chap_folder in sorted(package_dir.glob("*")):
            if chap_folder.is_dir() and not chap_folder.name.startswith("."):
                chap_data = self._process_hindi_chapter(chap_folder, class_id, subject_id, source_pkg)
                if chap_data:
                    chap_id = chap_data["chapter_id"]
                    out_file = output_dir / "Hindi" / f"{chap_id}.json"
                    write_json_utf8(out_file, chap_data)
                    chapters_processed.append(chap_data["id"])

        return {
            "subject": "Hindi",
            "class_level": self.context.class_level,
            "book": self.profile.book,
            "unicode_safe": True,
            "chapters_count": len(chapters_processed),
            "chapters": chapters_processed,
            "status": "SUCCESS"
        }

    def _process_hindi_chapter(self, folder: Path, class_id: str, subject_id: str, source_pkg: str) -> dict[str, Any]:
        info_file = folder / "00_CHAPTER_INFO" / "CHAPTER_INFO.json"
        if not info_file.exists():
            raise FileNotFoundError(f"Missing CHAPTER_INFO.json in chapter folder: {folder}")

        info = read_json_utf8(info_file)
        chap_id = info.get("chapter_id")
        if not chap_id or str(chap_id).strip() == "":
            raise ValueError(f"Missing or invalid chapter_id in CHAPTER_INFO.json at {info_file}")

        chap_id = str(chap_id).strip()
        title = info.get("title", folder.name)

        learn_recs = []
        source_pages = folder / "01_LEARN" / "04_SOURCE_DERIVED" / "SOURCE_PAGES.json"
        if source_pages.exists():
            p_data = read_json_utf8(source_pages)
            for p in p_data.get("pages", []):
                txt = p.get("text", "").strip()
                if txt:
                    learn_recs.append({
                        "record_id": f"{class_id}_{subject_id}_{chap_id}_learn_01_LESSONS_{p.get('source_page', 1)}_{calculate_text_hash(txt)}",
                        "type": "lesson",
                        "text": txt,
                        "status": "SOURCE_PRESERVED",
                        "student_facing": True,
                        "source_file": str(folder),
                        "source_page": p.get("source_page", 1),
                        "content_origin": "SOURCE_DERIVED"
                    })

        return {
            "id": f"{class_id}_{subject_id}_{chap_id}",
            "classId": class_id,
            "subjectId": subject_id,
            "chapter_id": chap_id,
            "title": title,
            "learn": learn_recs,
            "practice": [],
            "assess": [],
            "revise": [],
            "resources": []
        }

HindiProcessor = HindiSubjectProcessor

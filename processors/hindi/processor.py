import json
import re
from pathlib import Path
from typing import Any
from ..common.pipeline import BaseSubjectProcessor
from ..common.json_utils import read_json_utf8, write_json_utf8
from ..common.hashing import calculate_text_hash
from ..common.logging import get_pipeline_logger

logger = get_pipeline_logger("HindiProcessor")

class HindiProcessor(BaseSubjectProcessor):
    def __init__(self):
        super().__init__("Hindi", "5")

    def process_package(self, package_dir: Path, output_dir: Path) -> dict[str, Any]:
        logger.info(f"Processing Hindi package (Devanagari Unicode Safe) at: {package_dir}")
        chapters_processed = []

        for chap_folder in sorted(package_dir.glob("*")):
            if chap_folder.is_dir() and not chap_folder.name.startswith("."):
                chap_data = self._process_hindi_chapter(chap_folder)
                if chap_data:
                    chap_id = chap_data["chapter_id"]
                    out_file = output_dir / "Hindi" / f"{chap_id}.json"
                    write_json_utf8(out_file, chap_data)
                    chapters_processed.append(chap_data["id"])

        return {
            "subject": "Hindi",
            "unicode_safe": True,
            "chapters_count": len(chapters_processed),
            "chapters": chapters_processed,
            "status": "SUCCESS"
        }

    def _process_hindi_chapter(self, folder: Path) -> dict[str, Any] | None:
        info_file = folder / "00_CHAPTER_INFO" / "CHAPTER_INFO.json"
        title = folder.name
        chap_id = "101"
        if info_file.exists():
            info = read_json_utf8(info_file)
            title = info.get("title", title)
            chap_id = str(info.get("chapter_id", chap_id))

        learn_recs = []
        source_pages = folder / "01_LEARN" / "04_SOURCE_DERIVED" / "SOURCE_PAGES.json"
        if source_pages.exists():
            p_data = read_json_utf8(source_pages)
            for p in p_data.get("pages", []):
                txt = p.get("text", "").strip()
                if txt:
                    learn_recs.append({
                        "record_id": f"class_5_02_hindi_complete_{chap_id}_learn_01_LESSONS_{p.get('source_page', 1)}_{calculate_text_hash(txt)}",
                        "type": "lesson",
                        "text": txt,
                        "status": "SOURCE_PRESERVED",
                        "student_facing": True
                    })

        return {
            "id": f"class_5_02_hindi_complete_{chap_id}",
            "classId": "class_5",
            "subjectId": "02_hindi_complete",
            "chapter_id": chap_id,
            "title": title,
            "learn": learn_recs,
            "practice": [],
            "assess": [],
            "revise": [],
            "resources": []
        }

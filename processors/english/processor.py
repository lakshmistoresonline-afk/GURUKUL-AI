import json
import re
from pathlib import Path
from typing import Any
from ..common.pipeline import BaseSubjectProcessor
from ..common.json_utils import read_json_utf8, write_json_utf8
from ..common.hashing import calculate_text_hash
from ..common.logging import get_pipeline_logger

logger = get_pipeline_logger("EnglishSubjectProcessor")

class EnglishSubjectProcessor(BaseSubjectProcessor):
    def __init__(self, context=None, profile=None):
        super().__init__("English", context, profile)

    def process_package(self, package_dir: Path, output_dir: Path) -> dict[str, Any]:
        if not self.context:
            raise ValueError("EnglishSubjectProcessor requires a ProcessingContext.")
        if not self.profile:
            raise ValueError("EnglishSubjectProcessor requires a SourceProfile.")

        logger.info(f"Processing English package for Class {self.context.class_level} ({self.profile.book}) at: {package_dir}")
        chapters_processed = []

        class_id = f"class_{self.context.class_level}"
        subject_id = self.context.subject.lower()
        source_pkg = self.context.source_package

        for chap_folder in sorted(package_dir.glob("*")):
            if chap_folder.is_dir() and not chap_folder.name.startswith("."):
                chap_data = self._process_english_chapter(chap_folder, class_id, subject_id, source_pkg)
                if chap_data:
                    chap_id = chap_data["chapter_id"]
                    out_dir = output_dir / "English"
                    out_dir.mkdir(parents=True, exist_ok=True)
                    out_file = out_dir / f"{chap_id}.json"
                    write_json_utf8(out_file, chap_data)
                    chapters_processed.append(chap_data["id"])

        return {
            "subject": "English",
            "class_level": self.context.class_level,
            "book": self.profile.book,
            "chapters_count": len(chapters_processed),
            "chapters": chapters_processed,
            "status": "SUCCESS"
        }

    def _process_english_chapter(self, folder: Path, class_id: str, subject_id: str, source_pkg: str) -> dict[str, Any]:
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
        practice_recs = []
        assess_recs = []
        revise_recs = []
        resource_recs = []
        traceability_recs = []

        order_counter = 1

        def make_block(pillar_type: str, item_id: str, title_val: str | None, text_val: str | None, structured: Any, jf: Path) -> dict[str, Any]:
            nonlocal order_counter
            block = {
                "id": f"{class_id}_{subject_id}_{chap_id}_{pillar_type}_{item_id}",
                "type": pillar_type,
                "title": title_val,
                "text": text_val,
                "structuredData": structured,
                "source": {
                    "file": str(jf.relative_to(folder.parent.parent)) if folder in jf.parents else str(jf),
                    "page": None  # source_page_provenance = NOT_AVAILABLE
                },
                "content_origin": "CANONICAL_JSON",
                "order": order_counter
            }
            order_counter += 1
            return block

        # 1. LEARN Pillar
        learn_dir = folder / "01_LEARN"
        if learn_dir.exists():
            for sub in sorted(learn_dir.iterdir()):
                if sub.is_dir():
                    for jf in sorted(sub.glob("*.json")):
                        data = read_json_utf8(jf)
                        if isinstance(data, dict):
                            for k, v in data.items():
                                if isinstance(v, str):
                                    learn_recs.append(make_block(sub.name.lower(), k, k, v, None, jf))
                                elif isinstance(v, dict):
                                    learn_recs.append(make_block(sub.name.lower(), k, v.get("title", k), v.get("text", str(v)), v, jf))
                                elif isinstance(v, list):
                                    for idx, item in enumerate(v):
                                        if isinstance(item, dict):
                                            t = item.get("title") or item.get("text") or f"{k} {idx+1}"
                                            txt = item.get("text") or str(item)
                                            learn_recs.append(make_block(sub.name.lower(), f"{k}_{idx}", t, txt, item, jf))
                                        else:
                                            txt = str(item)
                                            learn_recs.append(make_block(sub.name.lower(), f"{k}_{idx}", f"{k} {idx+1}", txt, None, jf))
                        elif isinstance(data, list):
                            for idx, item in enumerate(data):
                                if isinstance(item, dict):
                                    t = item.get("title") or item.get("text") or f"Item {idx+1}"
                                    txt = item.get("text") or str(item)
                                    learn_recs.append(make_block(sub.name.lower(), f"item_{idx}", t, txt, item, jf))
                                else:
                                    txt = str(item)
                                    learn_recs.append(make_block(sub.name.lower(), f"item_{idx}", f"Item {idx+1}", txt, None, jf))

        # 2. PRACTICE Pillar
        practice_dir = folder / "02_PRACTICE"
        if practice_dir.exists():
            for sub in sorted(practice_dir.iterdir()):
                if sub.is_dir():
                    for jf in sorted(sub.glob("*.json")):
                        data = read_json_utf8(jf)
                        if isinstance(data, list):
                            for idx, item in enumerate(data):
                                if isinstance(item, dict):
                                    item_id = item.get("activity_id") or item.get("id") or f"item_{idx}"
                                    t = item.get("title") or item.get("question") or f"Activity {idx+1}"
                                    txt = item.get("instructions") or item.get("question") or str(item)
                                    practice_recs.append(make_block(sub.name.lower(), str(item_id), t, txt, item, jf))
                                else:
                                    txt = str(item)
                                    practice_recs.append(make_block(sub.name.lower(), f"item_{idx}", f"Item {idx+1}", txt, None, jf))
                        elif isinstance(data, dict):
                            for k, v in data.items():
                                if isinstance(v, list):
                                    for idx, item in enumerate(v):
                                        if isinstance(item, dict):
                                            item_id = item.get("id") or f"{k}_{idx}"
                                            t = item.get("title") or item.get("question") or f"{k} {idx+1}"
                                            txt = item.get("instructions") or item.get("question") or str(item)
                                            practice_recs.append(make_block(sub.name.lower(), str(item_id), t, txt, item, jf))
                                        else:
                                            txt = str(item)
                                            practice_recs.append(make_block(sub.name.lower(), f"{k}_{idx}", f"{k} {idx+1}", txt, None, jf))
                                else:
                                    practice_recs.append(make_block(sub.name.lower(), k, k, str(v), v, jf))

        # 3. ASSESS Pillar
        assess_dir = folder / "03_ASSESS"
        if assess_dir.exists():
            for jf in sorted(assess_dir.rglob("*.json")):
                data = read_json_utf8(jf)
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, list):
                            for idx, item in enumerate(v):
                                if isinstance(item, dict):
                                    item_id = item.get("id") or f"{k}_{idx}"
                                    t = item.get("title") or item.get("question") or f"{k} {idx+1}"
                                    txt = item.get("question") or str(item)
                                    assess_recs.append(make_block(jf.stem.lower(), str(item_id), t, txt, item, jf))
                                else:
                                    txt = str(item)
                                    assess_recs.append(make_block(jf.stem.lower(), f"{k}_{idx}", f"{k} {idx+1}", txt, None, jf))
                        else:
                            assess_recs.append(make_block(jf.stem.lower(), k, k, str(v), v, jf))

        # 4. REVISE Pillar
        revise_dir = folder / "04_REVISE"
        if revise_dir.exists():
            for jf in sorted(revise_dir.rglob("*.json")):
                data = read_json_utf8(jf)
                if isinstance(data, dict):
                    for k, v in data.items():
                        if isinstance(v, list):
                            for idx, item in enumerate(v):
                                if isinstance(item, dict):
                                    item_id = item.get("id") or f"{k}_{idx}"
                                    t = item.get("title") or f"{k} {idx+1}"
                                    txt = item.get("text") or str(item)
                                    revise_recs.append(make_block(jf.stem.lower(), str(item_id), t, txt, item, jf))
                                else:
                                    txt = str(item)
                                    revise_recs.append(make_block(jf.stem.lower(), f"{k}_{idx}", f"{k} {idx+1}", txt, None, jf))
                        else:
                            revise_recs.append(make_block(jf.stem.lower(), k, k, str(v), v, jf))

        # 5. RESOURCES & MULTIMEDIA Pillar
        for res_folder_name in ["05_MULTIMEDIA", "05_RESOURCES"]:
            res_dir = folder / res_folder_name
            if res_dir.exists():
                for jf in sorted(res_dir.rglob("*.json")):
                    data = read_json_utf8(jf)
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(v, list):
                                for idx, item in enumerate(v):
                                    if isinstance(item, dict):
                                        item_id = item.get("id") or f"{k}_{idx}"
                                        t = item.get("title") or f"{k} {idx+1}"
                                        txt = item.get("url") or item.get("description") or str(item)
                                        resource_recs.append(make_block(jf.stem.lower(), str(item_id), t, txt, item, jf))
                                    else:
                                        txt = str(item)
                                        resource_recs.append(make_block(jf.stem.lower(), f"{k}_{idx}", f"{k} {idx+1}", txt, None, jf))
                            else:
                                resource_recs.append(make_block(jf.stem.lower(), k, k, str(v), v, jf))

        # 6. TRACEABILITY / MASTERY
        for extra_folder in ["06_MASTERY", "99_INTERNAL_TRACEABILITY"]:
            extra_dir = folder / extra_folder
            if extra_dir.exists():
                for jf in sorted(extra_dir.rglob("*.json")):
                    data = read_json_utf8(jf)
                    if isinstance(data, dict):
                        for k, v in data.items():
                            traceability_recs.append({
                                "key": k,
                                "data": v,
                                "source_file": str(jf)
                            })

        return {
            "id": f"{class_id}_{subject_id}_{chap_id}",
            "classId": class_id,
            "subjectId": subject_id,
            "chapter_id": chap_id,
            "title": title,
            "learn": learn_recs,
            "practice": practice_recs,
            "assess": assess_recs,
            "revise": revise_recs,
            "resources": resource_recs,
            "traceability": traceability_recs
        }

EnglishProcessor = EnglishSubjectProcessor

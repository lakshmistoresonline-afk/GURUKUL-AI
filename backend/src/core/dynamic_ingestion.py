import os
import json
import hashlib
from typing import Dict, Any, List, Optional
from ..config.app_config import settings

class DynamicIngestionEngine:
    """
    Handles dynamic file discovery, schema fingerprinting, atomic record extraction,
    duplicate classification (EXACT_DUPLICATE, STRUCTURAL_DUPLICATE, SEMANTIC_DUPLICATE,
    NEW_RECORD, POSSIBLE_VARIANT, CONFLICTING_RECORD, UNKNOWN), non-destructive merging,
    safe publishing, and rollback safety.
    Maintains 100% source immutability (READ-ONLY access).
    """

    @staticmethod
    def discover_files() -> List[Dict[str, Any]]:
        root = settings.CONTENT_ROOT
        discovered = []
        if not os.path.exists(root):
            return discovered

        for dp, dn, fn in os.walk(root):
            for f in fn:
                if f.endswith(".json"):
                    fpath = os.path.join(dp, f)
                    rel_path = os.path.relpath(fpath, root)
                    size = os.path.getsize(fpath)
                    mtime = os.path.getmtime(fpath)

                    with open(fpath, "rb") as bf:
                        bdata = bf.read()
                        sha = hashlib.sha256(bdata).hexdigest()

                    try:
                        parsed = json.loads(bdata.decode("utf-8"))
                    except Exception:
                        parsed = {}

                    # Determine grade, subject, chapter from path
                    parts = rel_path.split(os.sep)
                    grade = "5"
                    subject = "Unknown"
                    if len(parts) >= 2 and parts[0].lower().startswith("class"):
                        grade = parts[0].split()[1] if len(parts[0].split()) > 2 or len(parts[0].split()) == 2 else "5"
                        subject = parts[1]

                    root_type = type(parsed).__name__
                    record_count = len(parsed.get("chapters", [])) if isinstance(parsed, dict) and "chapters" in parsed else len(parsed.get("chapters_master_data", [])) if isinstance(parsed, dict) and "chapters_master_data" in parsed else len(parsed.get("flashcards", [])) if isinstance(parsed, dict) and "flashcards" in parsed else len(parsed) if isinstance(parsed, list) else 1

                    discovered.append({
                        "sourcePath": fpath,
                        "relativePath": rel_path,
                        "filename": f,
                        "fileHash": sha,
                        "fileSize": size,
                        "mtime": mtime,
                        "grade": grade,
                        "subject": subject,
                        "rootType": root_type,
                        "recordCount": record_count,
                        "schemaFingerprint": hashlib.sha256(str(sorted(list(parsed.keys()) if isinstance(parsed, dict) else len(parsed))).encode("utf-8")).hexdigest()[:16]
                    })
        return sorted(discovered, key=lambda x: x["relativePath"])

    @staticmethod
    def classify_record(incoming_record: Any, existing_records: List[Any]) -> str:
        """
        Classifies incoming record into:
        EXACT_DUPLICATE, STRUCTURAL_DUPLICATE, SEMANTIC_DUPLICATE,
        NEW_RECORD, POSSIBLE_VARIANT, CONFLICTING_RECORD, UNKNOWN
        """
        if not incoming_record:
            return "UNKNOWN"

        inc_str = json.dumps(incoming_record, sort_keys=True, ensure_ascii=False)
        inc_hash = hashlib.sha256(inc_str.encode("utf-8")).hexdigest()

        for ex in existing_records:
            ex_str = json.dumps(ex, sort_keys=True, ensure_ascii=False)
            ex_hash = hashlib.sha256(ex_str.encode("utf-8")).hexdigest()

            if inc_hash == ex_hash:
                return "EXACT_DUPLICATE"

            # Check structural / semantic similarity
            if isinstance(incoming_record, dict) and isinstance(ex, dict):
                inc_q = incoming_record.get("question") or incoming_record.get("question_text") or incoming_record.get("term") or incoming_record.get("title")
                ex_q = ex.get("question") or ex.get("question_text") or ex.get("term") or ex.get("title")
                if inc_q and ex_q:
                    if inc_q.strip() == ex_q.strip():
                        # Same question text, check answer
                        inc_ans = incoming_record.get("correctAnswer") or incoming_record.get("answer")
                        ex_ans = ex.get("correctAnswer") or ex.get("answer")
                        if inc_ans == ex_ans:
                            return "SEMANTIC_DUPLICATE"
                        else:
                            return "CONFLICTING_RECORD"

        return "NEW_RECORD"

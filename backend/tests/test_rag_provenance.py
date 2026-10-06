import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.rag.provenance_model import RagProvenance

def test_rag_provenance_completeness():
    prov = RagProvenance(
        grade="6",
        subject="mathematics",
        book="main",
        part="none",
        unit="U01",
        chapter_id="G6-MAT-U01-C03",
        content_type="notes",
        content_id="chunk-001",
        source_path="Contents/Class 6/Maths/Notes.json",
        source_hash="abc123sha256hash",
        processed_path="ProcessedContent/Class6/Maths/G6-MAT-U01-C03/notes.json",
        processor_version="V14-STRICT",
        schema_version="3.0.0"
    )
    assert prov.verify_completeness() is True
    assert prov.grade == "6"
    assert prov.subject == "mathematics"
    assert prov.source_hash == "abc123sha256hash"

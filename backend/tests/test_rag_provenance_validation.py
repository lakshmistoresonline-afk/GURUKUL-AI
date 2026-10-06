import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.rag.provenance_model import RagProvenance, ProvenanceInconsistencyError

def test_rag_provenance_validation_success():
    identity = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_i",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    prov = RagProvenance(
        grade="7",
        subject="mathematics",
        book="maths_i",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview",
        content_id="chunk-101",
        source_path="Contents/Class 7/MathsI/G7-MAT-U01-C01.json",
        source_sha256="deadbeefsha256source",
        processed_path="ProcessedContent/Class7/MathsI/G7-MAT-U01-C01/overview.json",
        processed_sha256="deadbeefsha256processed",
        processor_version="V14-STRICT",
        schema_version="3.0.0",
        chunk_id="chunk-101"
    )

    validated = RagProvenance.validate_against_identity(identity, prov)
    assert validated.grade == "7"

def test_rag_provenance_validation_inconsistency_failure():
    identity = CurriculumIdentity(
        grade="7",
        subject="mathematics",
        book="maths_i",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview"
    )
    # Tampered grade
    prov = RagProvenance(
        grade="6",
        subject="mathematics",
        book="maths_i",
        part="part1",
        unit="U01",
        chapter_id="G7-MAT-U01-C01",
        content_type="overview",
        content_id="chunk-101",
        source_path="Contents/Class 7/MathsI/G7-MAT-U01-C01.json",
        source_sha256="deadbeefsha256source",
        processed_path="ProcessedContent/Class7/MathsI/G7-MAT-U01-C01/overview.json",
        processed_sha256="deadbeefsha256processed",
        processor_version="V14-STRICT",
        schema_version="3.0.0",
        chunk_id="chunk-101"
    )

    with pytest.raises(ProvenanceInconsistencyError):
        RagProvenance.validate_against_identity(identity, prov)

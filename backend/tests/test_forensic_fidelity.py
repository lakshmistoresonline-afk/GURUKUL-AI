import os
import sys
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.forensic_fidelity_verifier import ForensicFidelityVerifier
from src.curriculum.core.strict_content_validator import StrictContentValidator, ContentSchemaInvalidError

def test_forensic_verifier_block_extraction():
    sample = {"heading": "Forensic Verification", "paragraphs": ["Traceability is absolute."]}
    blocks = ForensicFidelityVerifier.extract_text_blocks(sample)
    assert "Forensic Verification" in blocks
    assert "Traceability is absolute." in blocks

def test_failing_fixture_corrupted_json(tmp_path):
    bad_file = tmp_path / "corrupted.json"
    bad_file.write_text("{ unclosed json dictionary ", encoding="utf-8")

    from src.curriculum.core.curriculum_identity import CurriculumIdentity
    identity = CurriculumIdentity(
        grade="5",
        subject="english",
        book="main",
        part="none",
        unit="U01",
        chapter_id="C01",
        content_type="overview"
    )
    with pytest.raises(ContentSchemaInvalidError):
        StrictContentValidator.validate_content_file(bad_file, identity)

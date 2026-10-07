import os
import sys
import pytest
from pathlib import Path

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.verification.forensic_fidelity_verifier import ForensicFidelityVerifier

def test_adversarial_block_extraction_ignores_metadata():
    sample = {
        "id": "meta-123",
        "timestamp": "2026-10-07",
        "hash": "abc",
        "schema_version": "3.0.0",
        "title": "Authoritative Educational Text"
    }
    blocks = ForensicFidelityVerifier.extract_structured_blocks(sample)
    assert len(blocks) == 1
    assert blocks[0][1] == "Authoritative Educational Text"

def test_adversarial_normalization():
    raw = "  Authoritative   NCERT\nTextbook "
    normalized = ForensicFidelityVerifier.normalize_text(raw)
    assert normalized == "authoritative ncert textbook"

def test_adversarial_parse_source_identity():
    rel = Path("Class 7/Maths I/G7-MAT-U01-C01.json")
    identity = ForensicFidelityVerifier.parse_source_identity(rel)
    assert identity["grade"] == "7"
    assert identity["subject"] == "mathematics"
    assert identity["book"] == "maths_i"
    assert identity["part"] == "part1"
    assert identity["chapter_id"] == "G7-MAT-U01-C01"

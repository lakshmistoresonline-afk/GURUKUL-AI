import os
import sys
import pytest

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.curriculum.core.curriculum_identity import CurriculumIdentity
from src.curriculum.processors.registry import ProcessorRegistry, ProcessorNotFoundError, ProcessorIdentityMismatchError

def test_all_registered_processors_contracts():
    introspection = ProcessorRegistry.introspect()
    assert len(introspection) == 16, f"Expected exactly 16 registered processors, found {len(introspection)}"

    for entry in introspection:
        key = entry["key"]
        parts = key.split(":")
        grade = parts[0]
        subject = parts[1]
        book = parts[2]
        part = parts[3] if len(parts) > 3 else "main"

        # 1. Test valid resolution and processing
        identity = CurriculumIdentity(
            grade=grade,
            subject=subject,
            book=book,
            part=part,
            unit="U01",
            chapter_id=f"G{grade}-{subject[:3].upper()}-U01-C01",
            content_type="overview"
        )
        proc = ProcessorRegistry.resolve(identity)
        assert proc is not None

        output = proc.process(identity, {"title": "Test Chapter Content", "paragraphs": ["Authoritative text"]})
        assert isinstance(output, dict)
        assert output.get("schema_version") == "3.0.0"
        assert output.get("processor_version") == "V14-STRICT"

        # 2. Test negative identity rejections (wrong grade)
        wrong_grade_identity = CurriculumIdentity(
            grade="99",
            subject=subject,
            book=book,
            part=part,
            unit="U01",
            chapter_id="X",
            content_type="overview"
        )
        with pytest.raises((ProcessorNotFoundError, ValueError, ProcessorIdentityMismatchError)):
            ProcessorRegistry.resolve(wrong_grade_identity)

        # 3. Test malformed input validation rejection
        with pytest.raises(ValueError):
            proc.process(identity, None)

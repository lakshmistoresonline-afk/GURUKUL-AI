import os
import sys
import pytest
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1]
src_dir = backend_dir / "src"

def test_no_hardcoded_developer_paths_in_production_code():
    forbidden_patterns = [
        "D:/GURUKUL",
        "D:\\GURUKUL",
        "C:/Users/",
        "C:\\Users\\"
    ]

    violations = []
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".py"):
                f_path = Path(root) / file
                content = f_path.read_text(encoding="utf-8", errors="ignore")
                for pat in forbidden_patterns:
                    if pat.lower() in content.lower():
                        violations.append(f"{f_path.relative_to(backend_dir)} contains forbidden hardcoded path '{pat}'")

    assert not violations, f"Portability violations detected in production source code:\n" + "\n".join(violations)

from pathlib import Path
from typing import Any

def create_provenance_record(source_file: Path, page: int | None = None, method: str = "canonical_ingestion") -> dict[str, Any]:
    return {
        "source_file": str(source_file),
        "source_page": page,
        "method": method
    }

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class ProcessingContext:
    job_id: str
    class_level: int | str
    subject: str
    source_package: str
    source_profile: Any = None
    output_dir: Path = field(default_factory=lambda: Path("Processed"))
    book: str = ""
    part: str = ""
    language: str = "English"

    def __post_init__(self):
        if self.job_id is None or str(self.job_id).strip() == "":
            raise ValueError("ProcessingContext requires a valid job_id.")
        if self.class_level is None or str(self.class_level).strip() == "":
            raise ValueError("ProcessingContext requires a valid class_level (no default allowed).")
        if self.subject is None or str(self.subject).strip() == "":
            raise ValueError("ProcessingContext requires a valid subject.")
        if self.source_package is None or str(self.source_package).strip() == "":
            raise ValueError("ProcessingContext requires a valid source_package.")

        self.class_level = str(self.class_level).strip()
        self.subject = str(self.subject).strip()
        self.source_package = str(self.source_package).strip()
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)

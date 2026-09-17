from pathlib import Path
from typing import Any

class BaseSubjectProcessor:
    def __init__(self, subject_name: str, class_level: str = "5"):
        self.subject_name = subject_name
        self.class_level = class_level

    def process_package(self, package_path: Path, output_dir: Path) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement process_package")

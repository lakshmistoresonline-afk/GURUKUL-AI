from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass
class SourceProfile:
    class_level: int | str
    subject: str
    book: str
    source_package: str
    source_files: list[str] = field(default_factory=list)
    language: str = "English"
    part: str = ""
    section_mapping: dict[str, list[str]] = field(default_factory=dict)
    rules: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.class_level is None or str(self.class_level).strip() == "":
            raise ValueError("SourceProfile requires class_level.")
        if self.subject is None or str(self.subject).strip() == "":
            raise ValueError("SourceProfile requires subject.")
        if self.book is None or str(self.book).strip() == "":
            raise ValueError("SourceProfile requires book name.")
        if self.source_package is None or str(self.source_package).strip() == "":
            raise ValueError("SourceProfile requires source_package identifier.")

        self.class_level = str(self.class_level).strip()
        self.subject = str(self.subject).strip()
        self.book = str(self.book).strip()
        self.source_package = str(self.source_package).strip()

    def validate_compatibility(self, context: Any) -> None:
        if str(context.class_level) != str(self.class_level):
            raise ValueError(
                f"Class level mismatch: ProcessingContext specifies class '{context.class_level}', "
                f"but SourceProfile specifies class '{self.class_level}'."
            )
        if context.subject.lower() != self.subject.lower():
            raise ValueError(
                f"Subject mismatch: ProcessingContext specifies subject '{context.subject}', "
                f"but SourceProfile specifies subject '{self.subject}'."
            )
        if context.source_package and context.source_package != self.source_package:
            raise ValueError(
                f"Source package mismatch: ProcessingContext specifies package '{context.source_package}', "
                f"but SourceProfile specifies package '{self.source_package}'."
            )

from pathlib import Path
from typing import Any
from .source.context import ProcessingContext
from .source.profile import SourceProfile

class BaseSubjectProcessor:
    def __init__(self, subject_name: str, context: ProcessingContext | None = None, profile: SourceProfile | None = None):
        self.subject_name = subject_name
        self.context = context
        self.profile = profile

        if context and profile:
            profile.validate_compatibility(context)
        elif context and not profile and context.source_profile:
            self.profile = context.source_profile
            self.profile.validate_compatibility(context)

    def process_package(self, package_path: Path, output_dir: Path) -> dict[str, Any]:
        raise NotImplementedError("Subclasses must implement process_package")

    def process(self, context: ProcessingContext, package_path: Path) -> dict[str, Any]:
        if context is None:
            raise ValueError("ProcessingContext is required for job execution.")
        self.context = context
        if context.source_profile:
            self.profile = context.source_profile
            self.profile.validate_compatibility(context)
        elif self.profile:
            self.profile.validate_compatibility(context)
        else:
            raise ValueError(f"Processor '{self.subject_name}' requires a valid SourceProfile in context or processor init.")

        return self.process_package(package_path, context.output_dir)

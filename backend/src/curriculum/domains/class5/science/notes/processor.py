from .extractor import Class5ScienceNotesExtractor
from .normalizer import Class5ScienceNotesNormalizer
from .validator import Class5ScienceNotesValidator
from .mapper import Class5ScienceNotesMapper

class Class5ScienceNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceNotesExtractor.extract(source_path)
        if not Class5ScienceNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class5ScienceNotesNormalizer.normalize(raw)
        return Class5ScienceNotesMapper.map_to_runtime(normalized)

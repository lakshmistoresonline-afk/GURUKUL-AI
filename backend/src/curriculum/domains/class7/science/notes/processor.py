from .extractor import Class7ScienceNotesExtractor
from .normalizer import Class7ScienceNotesNormalizer
from .validator import Class7ScienceNotesValidator
from .mapper import Class7ScienceNotesMapper

class Class7ScienceNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceNotesExtractor.extract(source_path)
        if not Class7ScienceNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class7ScienceNotesNormalizer.normalize(raw)
        return Class7ScienceNotesMapper.map_to_runtime(normalized)

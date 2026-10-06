from .extractor import Class6ScienceNotesExtractor
from .normalizer import Class6ScienceNotesNormalizer
from .validator import Class6ScienceNotesValidator
from .mapper import Class6ScienceNotesMapper

class Class6ScienceNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceNotesExtractor.extract(source_path)
        if not Class6ScienceNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class6ScienceNotesNormalizer.normalize(raw)
        return Class6ScienceNotesMapper.map_to_runtime(normalized)

from .extractor import Class6HindiNotesExtractor
from .normalizer import Class6HindiNotesNormalizer
from .validator import Class6HindiNotesValidator
from .mapper import Class6HindiNotesMapper

class Class6HindiNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiNotesExtractor.extract(source_path)
        if not Class6HindiNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class6HindiNotesNormalizer.normalize(raw)
        return Class6HindiNotesMapper.map_to_runtime(normalized)

from .extractor import Class6EnglishNotesExtractor
from .normalizer import Class6EnglishNotesNormalizer
from .validator import Class6EnglishNotesValidator
from .mapper import Class6EnglishNotesMapper

class Class6EnglishNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishNotesExtractor.extract(source_path)
        if not Class6EnglishNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class6EnglishNotesNormalizer.normalize(raw)
        return Class6EnglishNotesMapper.map_to_runtime(normalized)

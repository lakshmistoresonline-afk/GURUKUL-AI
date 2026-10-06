from .extractor import Class5EnglishNotesExtractor
from .normalizer import Class5EnglishNotesNormalizer
from .validator import Class5EnglishNotesValidator
from .mapper import Class5EnglishNotesMapper

class Class5EnglishNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishNotesExtractor.extract(source_path)
        if not Class5EnglishNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class5EnglishNotesNormalizer.normalize(raw)
        return Class5EnglishNotesMapper.map_to_runtime(normalized)

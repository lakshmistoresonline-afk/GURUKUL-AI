from .extractor import Class7EnglishNotesExtractor
from .normalizer import Class7EnglishNotesNormalizer
from .validator import Class7EnglishNotesValidator
from .mapper import Class7EnglishNotesMapper

class Class7EnglishNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishNotesExtractor.extract(source_path)
        if not Class7EnglishNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class7EnglishNotesNormalizer.normalize(raw)
        return Class7EnglishNotesMapper.map_to_runtime(normalized)

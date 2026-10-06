from .extractor import Class7EnglishFlashcardsExtractor
from .normalizer import Class7EnglishFlashcardsNormalizer
from .validator import Class7EnglishFlashcardsValidator
from .mapper import Class7EnglishFlashcardsMapper

class Class7EnglishFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7EnglishFlashcardsExtractor.extract(source_path)
        if not Class7EnglishFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class7EnglishFlashcardsNormalizer.normalize(raw)
        return Class7EnglishFlashcardsMapper.map_to_runtime(normalized)

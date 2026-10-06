from .extractor import Class5EnglishFlashcardsExtractor
from .normalizer import Class5EnglishFlashcardsNormalizer
from .validator import Class5EnglishFlashcardsValidator
from .mapper import Class5EnglishFlashcardsMapper

class Class5EnglishFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5EnglishFlashcardsExtractor.extract(source_path)
        if not Class5EnglishFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class5EnglishFlashcardsNormalizer.normalize(raw)
        return Class5EnglishFlashcardsMapper.map_to_runtime(normalized)

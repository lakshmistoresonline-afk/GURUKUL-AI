from .extractor import Class6EnglishFlashcardsExtractor
from .normalizer import Class6EnglishFlashcardsNormalizer
from .validator import Class6EnglishFlashcardsValidator
from .mapper import Class6EnglishFlashcardsMapper

class Class6EnglishFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6EnglishFlashcardsExtractor.extract(source_path)
        if not Class6EnglishFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class6EnglishFlashcardsNormalizer.normalize(raw)
        return Class6EnglishFlashcardsMapper.map_to_runtime(normalized)

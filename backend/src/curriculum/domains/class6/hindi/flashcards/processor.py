from .extractor import Class6HindiFlashcardsExtractor
from .normalizer import Class6HindiFlashcardsNormalizer
from .validator import Class6HindiFlashcardsValidator
from .mapper import Class6HindiFlashcardsMapper

class Class6HindiFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6HindiFlashcardsExtractor.extract(source_path)
        if not Class6HindiFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class6HindiFlashcardsNormalizer.normalize(raw)
        return Class6HindiFlashcardsMapper.map_to_runtime(normalized)

from .extractor import Class5HindiFlashcardsExtractor
from .normalizer import Class5HindiFlashcardsNormalizer
from .validator import Class5HindiFlashcardsValidator
from .mapper import Class5HindiFlashcardsMapper

class Class5HindiFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiFlashcardsExtractor.extract(source_path)
        if not Class5HindiFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class5HindiFlashcardsNormalizer.normalize(raw)
        return Class5HindiFlashcardsMapper.map_to_runtime(normalized)

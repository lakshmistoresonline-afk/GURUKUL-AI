from .extractor import Class7HindiFlashcardsExtractor
from .normalizer import Class7HindiFlashcardsNormalizer
from .validator import Class7HindiFlashcardsValidator
from .mapper import Class7HindiFlashcardsMapper

class Class7HindiFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiFlashcardsExtractor.extract(source_path)
        if not Class7HindiFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class7HindiFlashcardsNormalizer.normalize(raw)
        return Class7HindiFlashcardsMapper.map_to_runtime(normalized)

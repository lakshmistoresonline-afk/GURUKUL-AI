from .extractor import Class7MathematicsiFlashcardsExtractor
from .normalizer import Class7MathematicsiFlashcardsNormalizer
from .validator import Class7MathematicsiFlashcardsValidator
from .mapper import Class7MathematicsiFlashcardsMapper

class Class7MathematicsiFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiFlashcardsExtractor.extract(source_path)
        if not Class7MathematicsiFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class7MathematicsiFlashcardsNormalizer.normalize(raw)
        return Class7MathematicsiFlashcardsMapper.map_to_runtime(normalized)

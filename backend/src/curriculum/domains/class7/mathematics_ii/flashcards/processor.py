from .extractor import Class7MathematicsiiFlashcardsExtractor
from .normalizer import Class7MathematicsiiFlashcardsNormalizer
from .validator import Class7MathematicsiiFlashcardsValidator
from .mapper import Class7MathematicsiiFlashcardsMapper

class Class7MathematicsiiFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiFlashcardsExtractor.extract(source_path)
        if not Class7MathematicsiiFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class7MathematicsiiFlashcardsNormalizer.normalize(raw)
        return Class7MathematicsiiFlashcardsMapper.map_to_runtime(normalized)

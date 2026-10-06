from .extractor import Class5MathematicsFlashcardsExtractor
from .normalizer import Class5MathematicsFlashcardsNormalizer
from .validator import Class5MathematicsFlashcardsValidator
from .mapper import Class5MathematicsFlashcardsMapper

class Class5MathematicsFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5MathematicsFlashcardsExtractor.extract(source_path)
        if not Class5MathematicsFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class5MathematicsFlashcardsNormalizer.normalize(raw)
        return Class5MathematicsFlashcardsMapper.map_to_runtime(normalized)

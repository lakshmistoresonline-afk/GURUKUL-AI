from .extractor import Class6MathematicsFlashcardsExtractor
from .normalizer import Class6MathematicsFlashcardsNormalizer
from .validator import Class6MathematicsFlashcardsValidator
from .mapper import Class6MathematicsFlashcardsMapper

class Class6MathematicsFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6MathematicsFlashcardsExtractor.extract(source_path)
        if not Class6MathematicsFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class6MathematicsFlashcardsNormalizer.normalize(raw)
        return Class6MathematicsFlashcardsMapper.map_to_runtime(normalized)

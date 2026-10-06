from .extractor import Class6ScienceFlashcardsExtractor
from .normalizer import Class6ScienceFlashcardsNormalizer
from .validator import Class6ScienceFlashcardsValidator
from .mapper import Class6ScienceFlashcardsMapper

class Class6ScienceFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6ScienceFlashcardsExtractor.extract(source_path)
        if not Class6ScienceFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class6ScienceFlashcardsNormalizer.normalize(raw)
        return Class6ScienceFlashcardsMapper.map_to_runtime(normalized)

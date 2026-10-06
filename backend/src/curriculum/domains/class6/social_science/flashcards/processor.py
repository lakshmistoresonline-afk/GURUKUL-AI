from .extractor import Class6SocialscienceFlashcardsExtractor
from .normalizer import Class6SocialscienceFlashcardsNormalizer
from .validator import Class6SocialscienceFlashcardsValidator
from .mapper import Class6SocialscienceFlashcardsMapper

class Class6SocialscienceFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceFlashcardsExtractor.extract(source_path)
        if not Class6SocialscienceFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class6SocialscienceFlashcardsNormalizer.normalize(raw)
        return Class6SocialscienceFlashcardsMapper.map_to_runtime(normalized)

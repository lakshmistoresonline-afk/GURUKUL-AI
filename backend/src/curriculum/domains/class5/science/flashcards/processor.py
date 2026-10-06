from .extractor import Class5ScienceFlashcardsExtractor
from .normalizer import Class5ScienceFlashcardsNormalizer
from .validator import Class5ScienceFlashcardsValidator
from .mapper import Class5ScienceFlashcardsMapper

class Class5ScienceFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5ScienceFlashcardsExtractor.extract(source_path)
        if not Class5ScienceFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class5ScienceFlashcardsNormalizer.normalize(raw)
        return Class5ScienceFlashcardsMapper.map_to_runtime(normalized)

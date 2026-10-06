from .extractor import Class7ScienceFlashcardsExtractor
from .normalizer import Class7ScienceFlashcardsNormalizer
from .validator import Class7ScienceFlashcardsValidator
from .mapper import Class7ScienceFlashcardsMapper

class Class7ScienceFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7ScienceFlashcardsExtractor.extract(source_path)
        if not Class7ScienceFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class7ScienceFlashcardsNormalizer.normalize(raw)
        return Class7ScienceFlashcardsMapper.map_to_runtime(normalized)

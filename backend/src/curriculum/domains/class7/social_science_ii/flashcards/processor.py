from .extractor import Class7SocialscienceiiFlashcardsExtractor
from .normalizer import Class7SocialscienceiiFlashcardsNormalizer
from .validator import Class7SocialscienceiiFlashcardsValidator
from .mapper import Class7SocialscienceiiFlashcardsMapper

class Class7SocialscienceiiFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiFlashcardsExtractor.extract(source_path)
        if not Class7SocialscienceiiFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class7SocialscienceiiFlashcardsNormalizer.normalize(raw)
        return Class7SocialscienceiiFlashcardsMapper.map_to_runtime(normalized)

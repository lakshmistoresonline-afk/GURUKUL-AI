from .extractor import Class7SocialscienceiFlashcardsExtractor
from .normalizer import Class7SocialscienceiFlashcardsNormalizer
from .validator import Class7SocialscienceiFlashcardsValidator
from .mapper import Class7SocialscienceiFlashcardsMapper

class Class7SocialscienceiFlashcardsProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiFlashcardsExtractor.extract(source_path)
        if not Class7SocialscienceiFlashcardsValidator.validate(raw):
            raise ValueError("Validation failed for Flashcards")
        normalized = Class7SocialscienceiFlashcardsNormalizer.normalize(raw)
        return Class7SocialscienceiFlashcardsMapper.map_to_runtime(normalized)

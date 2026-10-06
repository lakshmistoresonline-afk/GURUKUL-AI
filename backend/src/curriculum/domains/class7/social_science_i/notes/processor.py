from .extractor import Class7SocialscienceiNotesExtractor
from .normalizer import Class7SocialscienceiNotesNormalizer
from .validator import Class7SocialscienceiNotesValidator
from .mapper import Class7SocialscienceiNotesMapper

class Class7SocialscienceiNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiNotesExtractor.extract(source_path)
        if not Class7SocialscienceiNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class7SocialscienceiNotesNormalizer.normalize(raw)
        return Class7SocialscienceiNotesMapper.map_to_runtime(normalized)

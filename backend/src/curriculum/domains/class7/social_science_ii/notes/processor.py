from .extractor import Class7SocialscienceiiNotesExtractor
from .normalizer import Class7SocialscienceiiNotesNormalizer
from .validator import Class7SocialscienceiiNotesValidator
from .mapper import Class7SocialscienceiiNotesMapper

class Class7SocialscienceiiNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7SocialscienceiiNotesExtractor.extract(source_path)
        if not Class7SocialscienceiiNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class7SocialscienceiiNotesNormalizer.normalize(raw)
        return Class7SocialscienceiiNotesMapper.map_to_runtime(normalized)

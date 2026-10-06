from .extractor import Class6SocialscienceNotesExtractor
from .normalizer import Class6SocialscienceNotesNormalizer
from .validator import Class6SocialscienceNotesValidator
from .mapper import Class6SocialscienceNotesMapper

class Class6SocialscienceNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class6SocialscienceNotesExtractor.extract(source_path)
        if not Class6SocialscienceNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class6SocialscienceNotesNormalizer.normalize(raw)
        return Class6SocialscienceNotesMapper.map_to_runtime(normalized)

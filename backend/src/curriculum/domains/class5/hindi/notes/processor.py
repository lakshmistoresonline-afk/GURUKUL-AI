from .extractor import Class5HindiNotesExtractor
from .normalizer import Class5HindiNotesNormalizer
from .validator import Class5HindiNotesValidator
from .mapper import Class5HindiNotesMapper

class Class5HindiNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class5HindiNotesExtractor.extract(source_path)
        if not Class5HindiNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class5HindiNotesNormalizer.normalize(raw)
        return Class5HindiNotesMapper.map_to_runtime(normalized)

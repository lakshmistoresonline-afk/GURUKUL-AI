from .extractor import Class7HindiNotesExtractor
from .normalizer import Class7HindiNotesNormalizer
from .validator import Class7HindiNotesValidator
from .mapper import Class7HindiNotesMapper

class Class7HindiNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7HindiNotesExtractor.extract(source_path)
        if not Class7HindiNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class7HindiNotesNormalizer.normalize(raw)
        return Class7HindiNotesMapper.map_to_runtime(normalized)

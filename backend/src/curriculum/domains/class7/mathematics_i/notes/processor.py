from .extractor import Class7MathematicsiNotesExtractor
from .normalizer import Class7MathematicsiNotesNormalizer
from .validator import Class7MathematicsiNotesValidator
from .mapper import Class7MathematicsiNotesMapper

class Class7MathematicsiNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiNotesExtractor.extract(source_path)
        if not Class7MathematicsiNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class7MathematicsiNotesNormalizer.normalize(raw)
        return Class7MathematicsiNotesMapper.map_to_runtime(normalized)

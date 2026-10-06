from .extractor import Class7MathematicsiiNotesExtractor
from .normalizer import Class7MathematicsiiNotesNormalizer
from .validator import Class7MathematicsiiNotesValidator
from .mapper import Class7MathematicsiiNotesMapper

class Class7MathematicsiiNotesProcessor:
    @classmethod
    def process(cls, source_path) -> dict:
        raw = Class7MathematicsiiNotesExtractor.extract(source_path)
        if not Class7MathematicsiiNotesValidator.validate(raw):
            raise ValueError("Validation failed for Notes")
        normalized = Class7MathematicsiiNotesNormalizer.normalize(raw)
        return Class7MathematicsiiNotesMapper.map_to_runtime(normalized)
